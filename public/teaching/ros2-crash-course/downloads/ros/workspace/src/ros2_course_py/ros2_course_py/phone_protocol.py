"""ROS-independent validation for the Android v2 sensor protocol (Apache-2.0)."""
import base64
import math

MAX_JPEG = 700_000


def number(value, name, low=-1e15, high=1e15):
    if isinstance(value, bool) or not isinstance(value, (float, int)):
        raise ValueError(name + ' must be numeric')
    if not math.isfinite(value) or not low <= value <= high:
        raise ValueError(name + ' is outside the finite accepted range')
    return float(value)


def vector(value, name, limit):
    if not isinstance(value, list) or len(value) != 3:
        raise ValueError(name + ' must contain three numbers')
    return [number(v, name, -limit, limit) for v in value]


class Session:
    def __init__(self):
        self.offset_ms = None
        self.last_stamp = {}
        self.last_sequence = {}

    def set_clock(self, message):
        self.offset_ms = number(message.get('offset_ms'), 'offset_ms')
        return number(message.get('rtt_ms'), 'rtt_ms', 0, 2000)

    def sensor(self, message, now_ns):
        if self.offset_ms is None:
            raise ValueError('Clock handshake is required before sensors')
        kind = message.get('type')
        if kind not in ('image', 'accel', 'gyro'):
            raise ValueError('Unknown sensor type')
        seq = message.get('seq')
        if type(seq) is not int or not 0 <= seq < 2**53 or seq <= self.last_sequence.get(kind, -1):
            raise ValueError('Sequence must increase within each stream')
        phone_ms = number(message.get('t_ms'), 't_ms', 0, 1e12)
        stamp = int((phone_ms + self.offset_ms) * 1_000_000)
        if not now_ns - 5_000_000_000 <= stamp <= now_ns + 250_000_000:
            raise ValueError('Timestamp is stale or in the future; reconnect and re-sync')
        if stamp <= self.last_stamp.get(kind, -1):
            raise ValueError('Timestamps must increase within each stream')
        result = {'type': kind, 'stamp_ns': stamp, 'seq': seq}
        if kind in ('accel', 'gyro'):
            result['values'] = vector(message.get('values'), 'values', 250 if kind == 'accel' else 100)
        else:
            width, height = message.get('width'), message.get('height')
            if type(width) is not int or type(height) is not int or not 1 <= width <= 640 or not 1 <= height <= 640:
                raise ValueError('Image dimensions must be positive integers <=640')
            jpeg = message.get('jpeg')
            if not isinstance(jpeg, str) or len(jpeg) > MAX_JPEG * 4 // 3 + 8:
                raise ValueError('JPEG message is too large or missing')
            try:
                data = base64.b64decode(jpeg, validate=True)
            except Exception as exc:
                raise ValueError('Invalid base64 JPEG') from exc
            if len(data) > MAX_JPEG or not data.startswith(b'\xff\xd8') or not data.endswith(b'\xff\xd9'):
                raise ValueError('Invalid JPEG envelope')
            result.update(width=width, height=height, jpeg=data)
        self.last_stamp[kind] = stamp
        self.last_sequence[kind] = seq
        return result
