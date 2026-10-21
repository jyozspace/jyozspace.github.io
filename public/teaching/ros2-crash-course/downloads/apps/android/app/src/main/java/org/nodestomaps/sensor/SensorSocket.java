package org.nodestomaps.sensor;

import java.io.*;
import java.net.*;
import java.nio.charset.StandardCharsets;
import java.security.*;
import java.security.cert.X509Certificate;
import java.util.*;
import java.util.concurrent.*;
import javax.net.ssl.*;

/** Small bounded RFC 6455 text client over a pinned TLS connection. No external libraries. */
final class SensorSocket implements AutoCloseable {
    interface Listener { void opened(); void text(String message); void failed(String message); }
    private final URI endpoint;
    private final String pin;
    private final Listener listener;
    private final BlockingQueue<byte[]> outgoing = new ArrayBlockingQueue<>(16);
    private final SecureRandom random = new SecureRandom();
    private volatile boolean closed;
    private volatile SSLSocket socket;
    private DataOutputStream output;
    private double sensorTokens=10;
    private long budgetTime=System.nanoTime();
    private final Object budgetLock=new Object();

    SensorSocket(String address, String fingerprint, Listener listener) {
        endpoint = URI.create(address.trim());
        pin = fingerprint.replace(":", "").replace(" ", "").toLowerCase(Locale.ROOT);
        if (!"wss".equals(endpoint.getScheme()) || endpoint.getHost() == null
                || !"/ws/android".equals(endpoint.getPath()) || endpoint.getUserInfo() != null
                || endpoint.getQuery() != null || endpoint.getFragment() != null)
            throw new IllegalArgumentException("Use wss://LAPTOP:8443/ws/android");
        if (!pin.matches("[a-f0-9]{64}")) throw new IllegalArgumentException("Paste the 64-digit certificate SHA-256 from the laptop.");
        this.listener = listener;
    }

    void connect() { new Thread(this::run, "sensor-tls-reader").start(); }
    boolean send(String message) {
        byte[] bytes = message.getBytes(StandardCharsets.UTF_8);
        return !closed && bytes.length <= 950_000 && outgoing.offer(bytes);
    }
    boolean congested() { return closed || outgoing.size() >= 3; }
    boolean sendSensor(String message) {
        synchronized(budgetLock) {
            long now=System.nanoTime();
            sensorTokens=Math.min(10,sensorTokens+(now-budgetTime)*120.0/1e9);budgetTime=now;
            if(sensorTokens<1)return false;
            sensorTokens-=1;
            return send(message);
        }
    }

    private void run() {
        try {
            TrustManager[] trust = {new X509TrustManager() {
                public X509Certificate[] getAcceptedIssuers() { return new X509Certificate[0]; }
                public void checkClientTrusted(X509Certificate[] c, String a) throws java.security.cert.CertificateException { throw new java.security.cert.CertificateException("Client authentication unsupported"); }
                public void checkServerTrusted(X509Certificate[] chain, String auth) throws java.security.cert.CertificateException {
                    try {
                        if (chain.length == 0) throw new GeneralSecurityException("Missing certificate");
                        chain[0].checkValidity();
                        byte[] digest = MessageDigest.getInstance("SHA-256").digest(chain[0].getEncoded());
                        StringBuilder actual = new StringBuilder();
                        for (byte b : digest) actual.append(String.format(Locale.ROOT, "%02x", b & 255));
                        if (!MessageDigest.isEqual(actual.toString().getBytes(StandardCharsets.US_ASCII), pin.getBytes(StandardCharsets.US_ASCII)))
                            throw new GeneralSecurityException("Server certificate pin mismatch");
                    } catch (GeneralSecurityException ex) { throw new java.security.cert.CertificateException(ex); }
                }
            }};
            SSLContext tls = SSLContext.getInstance("TLS"); tls.init(null, trust, random);
            SSLSocket connection = (SSLSocket) tls.getSocketFactory().createSocket();
            socket = connection;
            if (closed) { connection.close(); return; }
            int port = endpoint.getPort() < 0 ? 443 : endpoint.getPort();
            connection.connect(new InetSocketAddress(endpoint.getHost(), port), 10_000);
            connection.setSoTimeout(35_000);
            // The exact leaf pin is the server identity. No global trust-store changes.
            connection.startHandshake();
            InputStream input = connection.getInputStream();
            output = new DataOutputStream(connection.getOutputStream());
            byte[] nonce = new byte[16]; random.nextBytes(nonce);
            String key = Base64.getEncoder().encodeToString(nonce);
            String host = endpoint.getHost().contains(":") ? "[" + endpoint.getHost() + "]" : endpoint.getHost();
            String request = "GET /ws/android HTTP/1.1\r\nHost: " + host + ":" + port
                    + "\r\nUpgrade: websocket\r\nConnection: Upgrade\r\nSec-WebSocket-Version: 13\r\nSec-WebSocket-Key: " + key + "\r\n\r\n";
            output.write(request.getBytes(StandardCharsets.US_ASCII)); output.flush();
            ByteArrayOutputStream header = new ByteArrayOutputStream(); int suffix = 0;
            while (suffix != 0x0d0a0d0a) {
                int ch = input.read(); if (ch < 0 || header.size() > 16_384) throw new IOException("Invalid HTTP upgrade");
                header.write(ch); suffix = (suffix << 8) | ch;
            }
            String[] lines = header.toString("US-ASCII").split("\r\n");
            if (!lines[0].matches("HTTP/1\\.[01] 101(?: .*)?")) throw new IOException("Receiver upgrade failed: " + lines[0]);
            Map<String,String> headers = new HashMap<>();
            for (int i=1;i<lines.length;i++) { int colon=lines[i].indexOf(':'); if(colon>0) headers.put(lines[i].substring(0,colon).toLowerCase(Locale.ROOT),lines[i].substring(colon+1).trim()); }
            String accept=Base64.getEncoder().encodeToString(MessageDigest.getInstance("SHA-1").digest((key+"258EAFA5-E914-47DA-95CA-C5AB0DC85B11").getBytes(StandardCharsets.US_ASCII)));
            if (!accept.equals(headers.get("sec-websocket-accept")) || !"websocket".equalsIgnoreCase(headers.get("upgrade"))
                    || !Arrays.asList(headers.getOrDefault("connection", "").toLowerCase(Locale.ROOT).split("\\s*,\\s*")).contains("upgrade"))
                throw new IOException("Invalid WebSocket upgrade response");
            new Thread(() -> { try {
                long lastPing=System.nanoTime();
                while(!closed) {
                    byte[] packet=outgoing.poll(2,TimeUnit.SECONDS);
                    if(closed)break;
                    if(packet!=null)writeFrame(1,packet);
                    if(System.nanoTime()-lastPing>10_000_000_000L){writeFrame(9,new byte[0]);lastPing=System.nanoTime();}
                }
            }
                catch(InterruptedException ex) { Thread.currentThread().interrupt(); }
                catch(Exception ex) { if(!closed) listener.failed("Send failed: "+ex.getMessage()); close(); }
            },"sensor-tls-writer").start();
            listener.opened();
            DataInputStream data = new DataInputStream(input);
            ByteArrayOutputStream fragmented = null;
            while(!closed) {
                int first=data.readUnsignedByte(), second=data.readUnsignedByte(), opcode=first&15;
                boolean fin=(first&128)!=0;
                if((first&112)!=0 || (second&128)!=0) throw new IOException("Unsupported server frame flags");
                long length=second&127;
                if(length==126) length=data.readUnsignedShort(); else if(length==127) length=data.readLong();
                if(length<0 || length>1_000_000 || (opcode>=8 && (!fin || length>125))) throw new IOException("Server frame exceeds limits");
                byte[] payload=new byte[(int)length]; data.readFully(payload);
                if(opcode==8) throw new IOException("Receiver closed the session");
                if(opcode==9) { writeFrame(10,payload); continue; }
                if(opcode==10) continue;
                if(opcode==1 && fragmented==null) {
                    if(fin) listener.text(new String(payload,StandardCharsets.UTF_8));
                    else { fragmented=new ByteArrayOutputStream(); fragmented.write(payload); }
                } else if(opcode==0 && fragmented!=null) {
                    fragmented.write(payload); if(fragmented.size()>1_000_000) throw new IOException("Message too large");
                    if(fin) { listener.text(fragmented.toString("UTF-8")); fragmented=null; }
                } else throw new IOException("Expected text message");
            }
        } catch(Exception ex) { if(!closed) listener.failed(ex.getMessage()==null?ex.getClass().getSimpleName():ex.getMessage()); }
        finally { close(); }
    }

    private synchronized void writeFrame(int opcode, byte[] payload) throws IOException {
        if(closed) throw new IOException("Session closed");
        output.writeByte(0x80|opcode);
        if(payload.length<126) output.writeByte(0x80|payload.length);
        else if(payload.length<=65535) {output.writeByte(0x80|126);output.writeShort(payload.length);}
        else {output.writeByte(0x80|127);output.writeLong(payload.length);}
        byte[] mask=new byte[4]; random.nextBytes(mask); output.write(mask);
        byte[] masked=payload.clone(); for(int i=0;i<masked.length;i++) masked[i]^=mask[i%4];
        output.write(masked); output.flush();
    }
    public void close() {
        closed=true; outgoing.clear();
        SSLSocket connection=socket; if(connection!=null) try {connection.close();} catch(IOException ignored) {}
        // Wake a waiting writer; it exits after the closed check in writeFrame.
        outgoing.offer(new byte[0]);
    }
}
