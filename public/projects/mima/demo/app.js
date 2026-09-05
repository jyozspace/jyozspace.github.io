/* ============================================================
   MIMA demo — app logic (vanilla JS, no build step)
   ============================================================ */
(function () {
  "use strict";

  const D = window.MIMA_DATA;
  const $  = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];

  /* ---------- state ---------- */
  const state = {
    screen: "device",
    dev: { ...D.device },
    votes: {},           // postId -> 1 | -1 | 0
    voteBase: {},
    sos: { preset: "pad", anon: false, radius: 500, custom: "" },
    booking: { docId: 1, slot: "5:30" },
    shareData: true,
  };
  D.posts.forEach(p => { state.voteBase[p.id] = p.up; state.votes[p.id] = 0; });

  /* ============================================================
     Theme
     ============================================================ */
  const THEME_KEY = "mima-theme";
  function initTheme() {
    let t;
    try { t = localStorage.getItem(THEME_KEY); } catch (e) {}
    if (!t) t = window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
    setTheme(t);
  }
  function setTheme(t) {
    document.documentElement.setAttribute("data-theme", t);
    try { localStorage.setItem(THEME_KEY, t); } catch (e) {}
    const meta = $('meta[name="theme-color"]');
    if (meta) meta.setAttribute("content", t === "dark" ? "#17101E" : "#8E4EC6");
  }
  $("#theme-btn").addEventListener("click", () => {
    setTheme(document.documentElement.getAttribute("data-theme") === "dark" ? "light" : "dark");
  });

  /* ============================================================
     Toast
     ============================================================ */
  let toastT;
  function toast(msg) {
    let t = $("#toast");
    if (!t) { t = document.createElement("div"); t.id = "toast"; $("#phone").appendChild(t); }
    t.textContent = msg;
    requestAnimationFrame(() => t.classList.add("show"));
    clearTimeout(toastT);
    toastT = setTimeout(() => t.classList.remove("show"), 2600);
  }

  /* ============================================================
     Sheets & modals
     ============================================================ */
  function openSheet(html) {
    const root = $("#sheet-root");
    root.innerHTML =
      `<div class="sheet-backdrop"><div class="sheet"><div class="sheet-grip"></div>${html}</div></div>`;
    const bd = $(".sheet-backdrop", root);
    bd.addEventListener("click", e => { if (e.target === bd) closeSheet(); });
    return root;
  }
  function openModal(html) {
    const root = $("#sheet-root");
    root.innerHTML = `<div class="modal-center"><div class="box">${html}</div></div>`;
    const bd = $(".modal-center", root);
    bd.addEventListener("click", e => { if (e.target === bd) closeSheet(); });
    return root;
  }
  function closeSheet() { $("#sheet-root").innerHTML = ""; }
  window.__mimaCloseSheet = closeSheet;

  /* ============================================================
     Chart helpers
     ============================================================ */
  function sparkline(values, w = 300, h = 60, color = "var(--accent)") {
    const max = Math.max(...values), min = Math.min(...values);
    const rng = max - min || 1;
    const step = w / (values.length - 1);
    const pts = values.map((v, i) => [i * step, h - ((v - min) / rng) * (h - 8) - 4]);
    const line = pts.map((p, i) => (i ? "L" : "M") + p[0].toFixed(1) + " " + p[1].toFixed(1)).join(" ");
    const area = `M0 ${h} ` + pts.map(p => "L" + p[0].toFixed(1) + " " + p[1].toFixed(1)).join(" ") + ` L${w} ${h} Z`;
    return `<svg class="spark" viewBox="0 0 ${w} ${h}" preserveAspectRatio="none" style="--accent:${color}">
      <path class="area" d="${area}"/><path class="line" d="${line}"/></svg>`;
  }
  function barChart(items, opts = {}) {
    const max = Math.max(...items.map(i => i.v));
    return `<div class="bar-chart">` + items.map(i => `
      <div class="bar ${i.hot ? "hot" : ""}">
        <span class="b" style="height:${Math.max(6, (i.v / max) * 100)}%"></span>
        <span class="l">${i.label}</span>
      </div>`).join("") + `</div>`;
  }
  function ring(pct, label, sub, color = "var(--accent)") {
    const r = 52, c = 2 * Math.PI * r, off = c * (1 - pct);
    return `<div class="ring"><svg viewBox="0 0 120 120">
      <circle cx="60" cy="60" r="${r}" fill="none" stroke="var(--line)" stroke-width="10"/>
      <circle cx="60" cy="60" r="${r}" fill="none" stroke="${color}" stroke-width="10"
        stroke-linecap="round" stroke-dasharray="${c}" stroke-dashoffset="${off}"/>
    </svg><div class="c"><b>${label}</b><span>${sub}</span></div></div>`;
  }

  /* ============================================================
     SCREEN: Device
     ============================================================ */
  function renderDevice() {
    const d = state.dev;
    const pct = (d.targetTemp - 35) / (48 - 35);
    const r = 92, circ = 2 * Math.PI * r;
    return `
    <div class="screen-head">
      <h1>Good morning, ${D.user.name.split(" ")[0]}</h1>
      <p>Cycle day ${D.user.cycleDay} · period phase · next in ${D.user.cycleLen - D.user.cycleDay} days</p>
    </div>

    <div class="card conn-card">
      <div class="card-title">MIMA Module</div>
      <div class="conn-status"><span class="dot"></span> Connected via Bluetooth</div>
      <div class="conn-meta">
        <div>Device<b>${d.name}</b></div>
        <div>Battery<b>${d.battery}%</b></div>
        <div>Signal<b>${d.signal}</b></div>
      </div>
    </div>

    <div class="card">
      <div class="card-title">Mode of operation</div>
      <div class="seg" id="mode-seg">
        <button data-mode="auto" class="${d.mode === "auto" ? "active" : ""}">Auto (EMG)</button>
        <button data-mode="manual" class="${d.mode === "manual" ? "active" : ""}">Manual</button>
      </div>
      <p class="muted" style="font-size:12.5px;margin-top:10px">
        ${d.mode === "auto"
          ? "The onboard sEMG sensor detects abdominal muscle contractions and activates targeted heat automatically, scaling intensity to cramp strength."
          : "You control heating, target temperature and the session timer manually."}
      </p>
    </div>

    <div class="card">
      <div class="card-title">Targeted heat therapy</div>
      <div class="dial-wrap">
        <div class="dial">
          <svg viewBox="0 0 200 200">
            <circle cx="100" cy="100" r="${r}" fill="none" stroke="var(--line)" stroke-width="14"/>
            <circle cx="100" cy="100" r="${r}" fill="none" stroke="url(#g)" stroke-width="14"
              stroke-linecap="round" stroke-dasharray="${circ}" stroke-dashoffset="${circ * (1 - pct * 0.75)}"/>
            <defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1">
              <stop offset="0" stop-color="#EC6FA9"/><stop offset="1" stop-color="#8E4EC6"/>
            </linearGradient></defs>
          </svg>
          <div class="dial-center">
            <div class="dial-temp">${d.targetTemp}<sup>°C</sup></div>
            <div class="dial-label">Target</div>
          </div>
        </div>
        <div class="dial-btns">
          <button id="temp-down" ${d.mode === "auto" ? "disabled style=opacity:.4" : ""}>–</button>
          <button id="temp-up" ${d.mode === "auto" ? "disabled style=opacity:.4" : ""}>+</button>
        </div>
      </div>
      <div class="divider"></div>
      <div class="row-between">
        <div><b style="font-size:14px">Heating element</b>
          <div class="muted" style="font-size:12px">Now at <span id="live-current-temp">${d.currentTemp.toFixed(1)}</span>°C · ${d.heating ? "active" : "idle"}</div>
        </div>
        <label class="switch">
          <input type="checkbox" id="heat-toggle" ${d.heating ? "checked" : ""} ${d.mode === "auto" ? "disabled" : ""}>
          <span class="track"></span><span class="thumb"></span>
        </label>
      </div>
      <div class="divider"></div>
      <div class="card-title" style="margin-bottom:8px">Session timer</div>
      <div class="timer-row" id="timer-row">
        ${[15, 20, 30, 45].map(m => `<button class="chip ${d.timerMin === m ? "active" : ""}" data-min="${m}">${m} min</button>`).join("")}
      </div>
    </div>

    <div class="card">
      <div class="card-title">Live physiological sensing</div>
      <div class="stat-grid">
        <div class="stat"><div class="k">Intimate-area temp</div><div class="v"><span id="live-skin-temp">${d.skinTemp}</span><small>°C</small></div></div>
        <div class="stat"><div class="k">Pulse rate</div><div class="v"><span id="live-pulse">${d.pulse}</span><small> bpm</small></div></div>
      </div>
      <div style="margin-top:10px">
        <div class="k" style="font-size:11px;font-weight:800;letter-spacing:.06em;text-transform:uppercase;color:var(--text-faint)">
          sEMG muscle activity · <span id="live-emg">${d.emg}</span>%
        </div>
        <div class="emg-bars">${Array.from({ length: 22 }, (_, i) =>
          `<i style="animation-delay:${(i * 0.07).toFixed(2)}s"></i>`).join("")}</div>
        <p class="muted" style="font-size:12px;margin-top:6px">
          ${d.mode === "auto"
            ? "Contraction detected — heat auto-scaled to " + d.targetTemp + "°C."
            : "Monitoring only. Switch to Auto to enable closed-loop response."}
        </p>
      </div>
    </div>`;
  }

  function wireDevice() {
    $$("#mode-seg button").forEach(b => b.addEventListener("click", () => {
      state.dev.mode = b.dataset.mode;
      if (state.dev.mode === "auto") state.dev.heating = true;
      rerender();
      toast(state.dev.mode === "auto" ? "Auto mode — EMG closed-loop enabled" : "Manual mode enabled");
    }));
    const up = $("#temp-up"), dn = $("#temp-down");
    if (up) up.addEventListener("click", () => { state.dev.targetTemp = Math.min(48, state.dev.targetTemp + 1); rerender(); });
    if (dn) dn.addEventListener("click", () => { state.dev.targetTemp = Math.max(35, state.dev.targetTemp - 1); rerender(); });
    const ht = $("#heat-toggle");
    if (ht) ht.addEventListener("change", () => { state.dev.heating = ht.checked; rerender(); toast(ht.checked ? "Heating on" : "Heating off"); });
    $$("#timer-row .chip").forEach(c => c.addEventListener("click", () => {
      state.dev.timerMin = +c.dataset.min; rerender(); toast(`Timer set to ${c.dataset.min} minutes`);
    }));
  }

  /* ============================================================
     SCREEN: Analytics
     ============================================================ */
  function renderAnalytics() {
    const painMax = 10;
    const cycleBars = D.cycleHistory.map(c => ({ v: c.pain, label: c.m }));
    const sleepBars = D.sleepByPhase.map(s => ({ v: s.v, label: s.p.slice(0, 4) }));
    return `
    <div class="screen-head">
      <h1>Your patterns</h1>
      <p>Learned from MIMA's onboard EMG, pulse &amp; temperature sensors over 6 cycles</p>
    </div>

    ${D.insights.map(i => `
      <div class="card insight">
        <h4>${i.icon} ${i.title}</h4>
        <p>${i.body}</p>
      </div>`).join("")}

    <div class="card">
      <div class="card-title">When cramps hit hardest</div>
      ${barChart(D.crampsByHour.map(c => ({ v: c.v, label: c.h, hot: c.hot })))}
      <p class="muted" style="font-size:12px">Muscle-activity intensity by time of day. Peaks around <b>6 AM</b> and <b>9 PM</b> on days 1–2.</p>
    </div>

    <div class="card">
      <div class="card-title">Cycle overview</div>
      <div class="cycle-ring">
        ${ring(D.user.cycleDay / D.user.cycleLen, "Day " + D.user.cycleDay, "of " + D.user.cycleLen)}
        <ul>
          <li style="--d:var(--pink)">Menstrual · days 1–${D.user.periodLen}</li>
          <li style="--d:var(--lavender)">Follicular · days 6–13</li>
          <li style="--d:var(--amber)">Ovulation · ~day 14</li>
          <li style="--d:var(--purple)">Luteal · days 15–28</li>
        </ul>
      </div>
      <div class="divider"></div>
      <div class="row-between"><span class="muted" style="font-size:12.5px">Predicted next period</span><span class="pill pink">${D.user.nextPeriod}</span></div>
    </div>

    <div class="card">
      <div class="card-title">Reported pain per cycle</div>
      ${barChart(cycleBars)}
      <p class="muted" style="font-size:12px">Down from <b>7/10</b> in May to <b>3/10</b> this cycle.</p>
    </div>

    <div class="card">
      <div class="card-title">This cycle · pain vs muscle activity</div>
      ${sparkline(D.painTrend, 300, 60, "var(--purple)")}
      <div style="margin-top:4px">${sparkline(D.emgTrend, 300, 60, "var(--pink)")}</div>
      <div class="legend">
        <i style="--sw:var(--accent)">Reported pain</i>
        <i style="--sw:var(--pink)">sEMG activity</i>
      </div>
    </div>

    <div class="card">
      <div class="card-title">Sleep by cycle phase</div>
      ${barChart(sleepBars)}
      <p class="muted" style="font-size:12px">Avg hours slept. Lowest during menstruation (6.1 hrs).</p>
    </div>

    <div class="card">
      <div class="card-title">Share with your clinician</div>
      <p class="muted" style="font-size:13px;margin-bottom:12px">Generate a summary PDF of these analytics for a gynaecological consultation.</p>
      <button class="btn outline" id="export-pdf">Export analytics summary</button>
    </div>`;
  }
  function wireAnalytics() {
    const b = $("#export-pdf");
    if (b) b.addEventListener("click", () => toast("Analytics summary generated (demo)"));
  }

  /* ============================================================
     SCREEN: Community
     ============================================================ */
  function renderCommunity() {
    return `
    <div class="screen-head">
      <h1>Community</h1>
      <p>A judgement-free forum for menstrual health — post as yourself or anonymously</p>
    </div>

    <div class="composer" id="composer">
      <div class="avatar sm">${D.user.initials}</div>
      <input placeholder="Share a problem or a solution…" readonly>
      <button class="btn sm">Post</button>
    </div>

    <div class="section-label" style="margin-left:2px">Your groups &amp; chatrooms</div>
    <div class="group-scroll">
      ${D.groups.map(g => `
        <button class="group-card" data-group="${g.name}">
          <div class="g-emoji">${g.emoji}</div>
          <div class="g-name">${g.name}</div>
          <div class="g-count">${g.count} members</div>
        </button>`).join("")}
    </div>

    <div class="chip-row" style="margin:12px 0">
      <button class="chip active">Hot</button>
      <button class="chip">New</button>
      <button class="chip">Top</button>
      <button class="chip">Following</button>
    </div>

    ${D.posts.map(p => renderPost(p)).join("")}`;
  }

  function renderPost(p, full = false) {
    const v = state.votes[p.id] || 0;
    const score = state.voteBase[p.id] + v;
    return `
    <article class="post" data-post="${p.id}">
      <div class="post-head">
        <div class="avatar sm" style="background:${p.color}">${p.initials}</div>
        <span>${p.anon ? "Anonymous" : p.author}</span>
        <span>· <span class="sub">g/${p.group}</span> · ${p.time}</span>
      </div>
      <h3>${p.title}</h3>
      <p class="body">${full ? p.body : (p.body.length > 160 ? p.body.slice(0, 160) + "…" : p.body)}</p>
      <div class="post-tags">${p.tags.map(t => `<span class="tag">#${t}</span>`).join("")}</div>
      <div class="post-actions">
        <div class="vote">
          <button class="up ${v === 1 ? "on" : ""}" data-vote="1" aria-label="Upvote">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M12 5v14M5 12l7-7 7 7"/></svg>
          </button>
          <span>${score}</span>
          <button data-vote="-1" aria-label="Downvote">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M12 19V5M5 12l7 7 7-7"/></svg>
          </button>
        </div>
        <button class="act-btn" data-open="${p.id}">💬 ${p.comments.length} comments</button>
        <button class="act-btn" data-share="${p.id}">↗ Share</button>
      </div>
      ${full ? `<div class="divider"></div>
        <div class="card-title">Comments</div>
        ${p.comments.map(c => `
          <div class="comment">
            <div class="avatar sm" style="background:${c.anon ? "var(--text-faint)" : "var(--purple)"}">${c.anon ? "A" : c.author.replace("u/", "")[0].toUpperCase()}</div>
            <div class="c-body">
              <div class="c-meta">${c.anon ? "Anonymous" : c.author} · ${c.time}</div>
              ${c.body}
            </div>
          </div>`).join("")}
        <div class="composer" style="margin-top:14px">
          <div class="avatar sm">${D.user.initials}</div>
          <input placeholder="Add a comment…" id="cmt-input">
          <button class="btn sm" id="cmt-send">Send</button>
        </div>` : ""}
    </article>`;
  }

  function wireCommunity() {
    $("#composer").addEventListener("click", openComposer);
    $$('.group-card').forEach(g => g.addEventListener("click", () =>
      openChatroom(g.dataset.group)));
    wirePostActions(document);
  }

  function wirePostActions(root) {
    $$(".post", root).forEach(art => {
      const id = +art.dataset.post;
      $$('[data-vote]', art).forEach(btn => btn.addEventListener("click", e => {
        e.stopPropagation();
        const dir = +btn.dataset.vote;
        state.votes[id] = state.votes[id] === dir ? 0 : dir;
        if ($("#sheet-root").innerHTML.includes("post-detail")) openPost(id);
        else rerender();
      }));
      const openBtn = $('[data-open]', art);
      if (openBtn) openBtn.addEventListener("click", e => { e.stopPropagation(); openPost(id); });
      const shareBtn = $('[data-share]', art);
      if (shareBtn) shareBtn.addEventListener("click", e => { e.stopPropagation(); toast("Link copied to clipboard (demo)"); });
      art.addEventListener("click", e => {
        if (e.target.closest("button")) return;
        openPost(id);
      });
    });
  }

  function openPost(id) {
    const p = D.posts.find(x => x.id === id);
    openSheet(`<div id="post-detail">${renderPost(p, true)}</div>`);
    wirePostActions($("#sheet-root"));
    const send = $("#cmt-send");
    if (send) send.addEventListener("click", () => {
      const inp = $("#cmt-input");
      if (!inp.value.trim()) return;
      p.comments.push({ anon: false, author: D.user.username, time: "now", body: inp.value.trim() });
      openPost(id);
      toast("Comment posted");
    });
  }

  function openComposer() {
    openSheet(`
      <h2>New post</h2>
      <p class="muted" style="font-size:13px;margin-bottom:14px">Your post helps others going through the same thing.</p>
      <div class="field"><label>Group</label>
        <select id="np-group">${D.groups.map(g => `<option>${g.name}</option>`).join("")}</select></div>
      <div class="field"><label>Title</label><input id="np-title" placeholder="Sum it up in a line"></div>
      <div class="field"><label>Details</label><textarea id="np-body" placeholder="Share your experience, question or solution…"></textarea></div>
      <div class="row-between" style="margin:6px 0 16px">
        <div><b style="font-size:14px">Post anonymously</b><div class="muted" style="font-size:12px">Hide your username on this post</div></div>
        <label class="switch"><input type="checkbox" id="np-anon"><span class="track"></span><span class="thumb"></span></label>
      </div>
      <button class="btn" id="np-submit">Publish post</button>`);
    $("#np-submit").addEventListener("click", () => {
      const title = $("#np-title").value.trim();
      if (!title) { toast("Add a title first"); return; }
      const anon = $("#np-anon").checked;
      D.posts.unshift({
        id: Date.now(), anon, author: D.user.username, initials: anon ? "A" : D.user.initials,
        color: "#8E4EC6", group: $("#np-group").value, time: "now",
        title, body: $("#np-body").value.trim() || "(no details)", tags: ["new"],
        up: 1, comments: [],
      });
      D.posts.forEach(pp => { if (!(pp.id in state.voteBase)) { state.voteBase[pp.id] = pp.up; state.votes[pp.id] = 0; } });
      closeSheet(); rerender(); toast(anon ? "Posted anonymously" : "Post published");
    });
  }

  function openChatroom(name) {
    const g = D.groups.find(x => x.name === name);
    openSheet(`
      <h2>${g.emoji} ${name}</h2>
      <p class="muted" style="font-size:12.5px;margin-bottom:14px">${g.count} members · group chatroom</p>
      <div class="chat-thread">
        <div class="msg them"><b>u/lunar_tide</b><br>Anyone up tonight? Rough day-1 over here 😩<span class="t">9:41 PM</span></div>
        <div class="msg them"><b>u/sea_glass</b><br>Here. Heat patch + tea. You on auto mode?<span class="t">9:43 PM</span></div>
        <div class="msg me">Yeah just switched it on. Already helping<span class="t">9:44 PM</span></div>
        <div class="msg them"><b>Anonymous</b><br>Sending warm thoughts 💜<span class="t">9:45 PM</span></div>
      </div>
      <div class="composer" style="margin-top:14px">
        <div class="avatar sm">${D.user.initials}</div>
        <input placeholder="Message ${name}…" id="cr-input">
        <button class="btn sm" id="cr-send">Send</button>
      </div>`);
    const send = () => {
      const i = $("#cr-input"); if (!i.value.trim()) return;
      const th = $(".chat-thread");
      const m = document.createElement("div");
      m.className = "msg me"; m.innerHTML = i.value.trim() + '<span class="t">now</span>';
      th.appendChild(m); i.value = ""; th.scrollTop = th.scrollHeight;
    };
    $("#cr-send").addEventListener("click", send);
    $("#cr-input").addEventListener("keydown", e => { if (e.key === "Enter") send(); });
  }

  /* ============================================================
     SCREEN: Assistance
     ============================================================ */
  function renderAssistance() {
    const c = D.upcomingConsult;
    return `
    <div class="screen-head">
      <h1>Assistance</h1>
      <p>Book a teleconsultation, chat, or start a video call with a gynaecologist</p>
    </div>

    <div class="card" style="background:linear-gradient(145deg,var(--purple),var(--plum));color:#fff;border:none">
      <div class="card-title" style="color:rgba(255,255,255,.7)">Upcoming consultation</div>
      <div class="row">
        <div class="doc-ph" style="background:rgba(255,255,255,.15)">${c.emoji}</div>
        <div><b style="font-size:15px;font-family:Fraunces,serif">${c.doc}</b>
          <div style="font-size:12.5px;opacity:.85">${c.when} · ${c.type}</div></div>
      </div>
      <div class="row" style="gap:10px;margin-top:14px">
        <button class="btn" style="background:#fff;color:var(--plum)" id="join-call">Join call</button>
        <button class="btn ghost" style="background:rgba(255,255,255,.15);color:#fff;border:none" id="open-chat">Chat</button>
      </div>
    </div>

    <div class="card">
      <div class="card-title">Data sharing</div>
      <div class="row-between">
        <div style="flex:1">
          <b style="font-size:14px">Share my physiological analytics</b>
          <div class="muted" style="font-size:12px">Your consulting gynaecologist can view EMG, pulse, temperature &amp; cycle trends</div>
        </div>
        <label class="switch"><input type="checkbox" id="share-toggle" ${state.shareData ? "checked" : ""}><span class="track"></span><span class="thumb"></span></label>
      </div>
      <div class="perm-row"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
        <span class="muted" style="font-size:12px">Access is per-clinician, time-limited to your consult window, and revocable anytime.</span></div>
    </div>

    <div class="section-label">Available gynaecologists</div>
    ${D.doctors.map(d => `
      <div class="card doc-card" data-doc="${d.id}">
        <div class="doc-ph">${d.emoji}</div>
        <div style="flex:1">
          <div class="d-name">${d.name}</div>
          <div class="d-spec">${d.spec}</div>
          <div class="d-meta">
            <span class="stars">★</span> ${d.rating} (${d.reviews}) · ${d.exp} · ${d.fee}
          </div>
          <div class="d-meta"><span>🗓 ${d.next}</span><span>🗣 ${d.lang}</span></div>
        </div>
      </div>`).join("")}

    <button class="btn outline" id="see-all-docs" style="margin-top:4px">Browse all specialists</button>`;
  }

  function wireAssistance() {
    $("#join-call").addEventListener("click", openVideoCall);
    $("#open-chat").addEventListener("click", openConsultChat);
    $("#share-toggle").addEventListener("change", e => {
      state.shareData = e.target.checked;
      toast(e.target.checked ? "Analytics sharing enabled" : "Analytics sharing revoked");
    });
    $$('.doc-card').forEach(dc => dc.addEventListener("click", () => openBooking(+dc.dataset.doc)));
    $("#see-all-docs").addEventListener("click", () => toast("Full directory coming in the live app"));
  }

  function openBooking(docId) {
    const d = D.doctors.find(x => x.id === docId);
    state.booking.docId = docId;
    openSheet(`
      <h2>Book with ${d.name}</h2>
      <p class="muted" style="font-size:12.5px;margin-bottom:14px">${d.spec} · ${d.fee} consultation</p>
      <div class="card-title">Consultation type</div>
      <div class="seg" id="ctype" style="margin-bottom:14px">
        <button class="active">Video</button><button>Voice</button><button>Chat</button>
      </div>
      <div class="card-title">Pick a slot — today</div>
      <div class="slot-grid" id="slot-grid">
        ${D.slots.map(s => {
          const gone = D.goneSlots.includes(s);
          return `<button class="slot ${gone ? "gone" : ""} ${s === state.booking.slot && !gone ? "active" : ""}" ${gone ? "disabled" : ""} data-slot="${s}">${s}</button>`;
        }).join("")}
      </div>
      <div class="row-between" style="margin:16px 0">
        <div><b style="font-size:14px">Share analytics with this clinician</b>
          <div class="muted" style="font-size:12px">For your consult window only</div></div>
        <label class="switch"><input type="checkbox" id="bk-share" ${state.shareData ? "checked" : ""}><span class="track"></span><span class="thumb"></span></label>
      </div>
      <button class="btn" id="bk-confirm">Confirm booking</button>`);
    $$("#ctype button").forEach(b => b.addEventListener("click", () => {
      $$("#ctype button").forEach(x => x.classList.remove("active")); b.classList.add("active");
    }));
    $$("#slot-grid .slot:not(.gone)").forEach(s => s.addEventListener("click", () => {
      $$("#slot-grid .slot").forEach(x => x.classList.remove("active"));
      s.classList.add("active"); state.booking.slot = s.dataset.slot;
    }));
    $("#bk-confirm").addEventListener("click", () => {
      closeSheet();
      openModal(`<div style="font-size:40px">✅</div>
        <h2 style="font-family:Fraunces,serif;font-size:20px;margin:8px 0">Booking confirmed</h2>
        <p class="muted" style="font-size:13px">${d.name} · today ${state.booking.slot} PM.<br>You'll get a reminder 15 min before.</p>
        <button class="btn" style="margin-top:16px" onclick="window.__mimaCloseSheet()">Done</button>`);
    });
  }

  function openConsultChat() {
    openSheet(`
      <h2>Dr. Nandini Rao</h2>
      <p class="muted" style="font-size:12.5px;margin-bottom:12px">Gynaecologist · usually replies within a few hours</p>
      <div class="pill green" style="margin-bottom:12px">🔓 You are sharing analytics with this clinician</div>
      <div class="chat-thread">
        ${D.consultChat.map(m => `<div class="msg ${m.who}">${m.body}<span class="t">${m.t}</span></div>`).join("")}
      </div>
      <div class="composer" style="margin-top:14px">
        <div class="avatar sm">${D.user.initials}</div>
        <input placeholder="Message Dr. Rao…" id="cc-input">
        <button class="btn sm" id="cc-send">Send</button>
      </div>`);
    const send = () => {
      const i = $("#cc-input"); if (!i.value.trim()) return;
      const th = $(".chat-thread");
      const m = document.createElement("div"); m.className = "msg me";
      m.innerHTML = i.value.trim() + '<span class="t">now</span>';
      th.appendChild(m); i.value = ""; th.scrollTop = th.scrollHeight;
      setTimeout(() => {
        const r = document.createElement("div"); r.className = "msg them";
        r.innerHTML = "Noted — I'll review and get back to you shortly.<span class=\"t\">now</span>";
        th.appendChild(r); th.scrollTop = th.scrollHeight;
      }, 1100);
    };
    $("#cc-send").addEventListener("click", send);
    $("#cc-input").addEventListener("keydown", e => { if (e.key === "Enter") send(); });
  }

  function openVideoCall() {
    openSheet(`
      <h2>Video consultation</h2>
      <p class="muted" style="font-size:12.5px;margin-bottom:12px">Dr. Nandini Rao · connected · 00:04</p>
      <div class="video-stage">
        <div style="text-align:center">
          <div style="font-size:52px">👩‍⚕️</div>
          <div style="font-weight:800;margin-top:6px">Dr. Nandini Rao</div>
          <div style="font-size:12px;opacity:.7">Camera on · audio clear</div>
        </div>
        <div class="self"></div>
      </div>
      <div class="pill" style="margin:12px 0">📊 Dr. Rao is viewing your shared analytics</div>
      <div class="video-ctrls">
        <button aria-label="Mute"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2a3 3 0 0 1 3 3v6a3 3 0 0 1-6 0V5a3 3 0 0 1 3-3z"/><path d="M19 10v1a7 7 0 0 1-14 0v-1M12 18v4"/></svg></button>
        <button aria-label="Camera"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M23 7l-7 5 7 5V7z"/><rect x="1" y="5" width="15" height="14" rx="2"/></svg></button>
        <button class="end" id="end-call" aria-label="End"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M21 15.5c-2.5 0-4.9-.4-7.1-1.1a1 1 0 0 0-1 .2l-2.2 2.2a15 15 0 0 1-6.6-6.6l2.2-2.2a1 1 0 0 0 .2-1C5.9 6.4 5.5 4 5.5 1.5A1 1 0 0 0 4.5.5H2A1 1 0 0 0 1 1.5 20 20 0 0 0 22.5 23a1 1 0 0 0 1-1v-2.5a1 1 0 0 0-1-1z"/></svg></button>
      </div>`);
    $("#end-call").addEventListener("click", () => { closeSheet(); toast("Call ended · summary added to your records"); });
  }

  /* ============================================================
     Emergency sheet
     ============================================================ */
  function openSOS() {
    const s = state.sos;
    openSheet(`
      <h2 style="color:var(--coral)">Emergency support</h2>
      <p class="muted" style="font-size:12.5px;margin-bottom:14px">
        Your request goes to verified MIMA users within your chosen radius. Someone nearby can help with a pad, medicine or supplies.
      </p>

      <div class="card-title">What do you need?</div>
      <div class="sos-preset-grid" id="sos-presets">
        ${D.sosPresets.map(p => `
          <button class="sos-preset ${s.preset === p.id ? "active" : ""}" data-p="${p.id}">
            <div class="e">${p.e}</div><div class="n">${p.n}</div><div class="d">${p.d}</div>
          </button>`).join("")}
      </div>

      <div id="sos-custom-wrap" class="field" style="margin-top:12px;${s.preset === "custom" ? "" : "display:none"}">
        <label>Your message</label>
        <textarea id="sos-custom" placeholder="Describe what you need…">${s.custom}</textarea>
      </div>

      <div class="field" style="margin-top:12px">
        <label>Alert radius · <span id="rad-val">${s.radius} m</span></label>
        <div class="radius-track">
          <input type="range" id="sos-radius" min="100" max="2000" step="100" value="${s.radius}">
        </div>
        <div class="muted" style="font-size:11.5px">Reaches ~<b id="rad-count">${estReach(s.radius)}</b> MIMA users nearby</div>
      </div>

      <div class="row-between" style="margin:8px 0 16px">
        <div><b style="font-size:14px">Send anonymously</b>
          <div class="muted" style="font-size:12px">Hide your name and username from responders</div></div>
        <label class="switch"><input type="checkbox" id="sos-anon" ${s.anon ? "checked" : ""}><span class="track"></span><span class="thumb"></span></label>
      </div>

      <button class="btn danger" id="sos-send">Send emergency request</button>

      <div class="section-label">Requests near you right now</div>
      ${D.incoming.map(i => `
        <div class="incoming">
          <div class="i-t">🆘 ${i.t}</div>
          <div class="i-d">${i.d}</div>
          <button class="btn sm" data-help style="background:var(--coral);color:#fff">I can help</button>
        </div>`).join("")}

      <div class="section-label">Nearby helpers who opted in</div>
      ${D.responders.map(r => `
        <div class="responder">
          <div class="avatar sm" style="background:var(--mint)">${r.initials}</div>
          <div><b style="font-size:13px">${r.name}</b><div class="muted" style="font-size:11.5px">${r.note}</div></div>
          <span class="r-dist">${r.dist}</span>
        </div>`).join("")}
    `);

    $$("#sos-presets .sos-preset").forEach(b => b.addEventListener("click", () => {
      state.sos.preset = b.dataset.p;
      $$("#sos-presets .sos-preset").forEach(x => x.classList.toggle("active", x === b));
      $("#sos-custom-wrap").style.display = b.dataset.p === "custom" ? "" : "none";
    }));
    $("#sos-radius").addEventListener("input", e => {
      state.sos.radius = +e.target.value;
      $("#rad-val").textContent = state.sos.radius + " m";
      $("#rad-count").textContent = estReach(state.sos.radius);
    });
    $("#sos-anon").addEventListener("change", e => state.sos.anon = e.target.checked);
    const cust = $("#sos-custom");
    if (cust) cust.addEventListener("input", e => state.sos.custom = e.target.value);
    $("#sos-send").addEventListener("click", () => {
      const p = D.sosPresets.find(x => x.id === state.sos.preset);
      const label = state.sos.preset === "custom" ? (state.sos.custom.trim() || "Custom request") : p.n;
      closeSheet();
      openModal(`
        <div style="font-size:40px">📡</div>
        <h2 style="font-family:Fraunces,serif;font-size:19px;margin:8px 0">Request broadcast</h2>
        <p class="muted" style="font-size:13px">"<b>${label}</b>" sent to ${estReach(state.sos.radius)} MIMA users within ${state.sos.radius} m${state.sos.anon ? ", anonymously" : ""}.</p>
        <div class="pill green" style="margin:14px auto 0">2 helpers notified · Priya is responding</div>
        <button class="btn" style="margin-top:16px" onclick="window.__mimaCloseSheet()">OK</button>`);
    });
    const help = $("[data-help]");
    if (help) help.addEventListener("click", () => { closeSheet(); toast("Thank you 💜 The requester has been notified you're coming."); });
  }
  function estReach(r) { return Math.round(r / 100) * 3 + 4; }

  $("#sos-fab").addEventListener("click", openSOS);

  /* ============================================================
     SCREEN: Profile
     ============================================================ */
  function renderProfile() {
    const isDark = document.documentElement.getAttribute("data-theme") === "dark";
    return `
    <div class="profile-hero">
      <div class="avatar lg">${D.user.initials}</div>
      <h2>${D.user.name}</h2>
      <div class="u">${D.user.username}</div>
      <div class="pill" style="margin-top:8px">${D.user.plan} · ${D.user.joined}</div>
    </div>

    <div class="profile-stats">
      <div class="ps"><b>6</b><span>Cycles tracked</span></div>
      <div class="ps"><b>142</b><span>Heat sessions</span></div>
      <div class="ps"><b>3</b><span>Helped nearby</span></div>
    </div>

    <div class="section-label">MIMA device</div>
    <div class="settings-list">
      <div class="item"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="7" y="3" width="10" height="18" rx="2"/><path d="M11 7h2"/></svg> Module ${D.device.name.split("· ")[1]} <span class="val">Firmware ${D.device.firmware}</span></div>
      <div class="item"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M6 7h11a3 3 0 0 1 3 3v4a3 3 0 0 1-3 3H6a3 3 0 0 1-3-3v-4a3 3 0 0 1 3-3z"/><path d="M23 11v2"/></svg> Battery health <span class="val">Good · ${D.device.battery}%</span></div>
      <div class="item" data-act="calibrate"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2v4M12 18v4M2 12h4M18 12h4"/><circle cx="12" cy="12" r="4"/></svg> Re-calibrate sEMG sensor <span class="chev">›</span></div>
      <div class="item" data-act="pair"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M7 7l10 10M17 7L7 17"/></svg> Pair a new module <span class="chev">›</span></div>
    </div>

    <div class="section-label">Preferences</div>
    <div class="settings-list">
      <div class="item"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 3a9 9 0 1 0 9 9c-5 0-9-4-9-9z"/></svg> Dark mode
        <label class="switch" style="margin-left:auto"><input type="checkbox" id="pf-theme" ${isDark ? "checked" : ""}><span class="track"></span><span class="thumb"></span></label></div>
      <div class="item"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 8a6 6 0 0 0-12 0c0 7-3 9-3 9h18s-3-2-3-9"/><path d="M13.7 21a2 2 0 0 1-3.4 0"/></svg> Cramp-forecast alerts
        <label class="switch" style="margin-left:auto"><input type="checkbox" checked><span class="track"></span><span class="thumb"></span></label></div>
      <div class="item"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M12 8v8M8 12h8"/></svg> Auto pre-warm before predicted peaks
        <label class="switch" style="margin-left:auto"><input type="checkbox" checked><span class="track"></span><span class="thumb"></span></label></div>
      <div class="item"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg> Respond to nearby SOS alerts
        <label class="switch" style="margin-left:auto"><input type="checkbox" checked><span class="track"></span><span class="thumb"></span></label></div>
    </div>

    <div class="section-label">Privacy &amp; data</div>
    <div class="settings-list">
      <div class="item" data-act="export"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 3v12M8 11l4 4 4-4M4 21h16"/></svg> Export my data <span class="chev">›</span></div>
      <div class="item" data-act="clinicians"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="8" r="4"/><path d="M4 21c0-4 4-6 8-6s8 2 8 6"/></svg> Clinicians with access <span class="val">1 active</span></div>
      <div class="item" data-act="default-anon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M2 12s3-7 10-7 10 7 10 7-3 7-10 7S2 12 2 12z"/><circle cx="12" cy="12" r="3"/></svg> Default posting identity <span class="val">Username</span></div>
    </div>

    <div class="section-label">Account</div>
    <div class="settings-list">
      <div class="item" data-act="help"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M9.1 9a3 3 0 0 1 5.8 1c0 2-3 3-3 3"/><path d="M12 17h.01"/></svg> Help &amp; support <span class="chev">›</span></div>
      <div class="item" data-act="about"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M12 16v-4M12 8h.01"/></svg> About MIMA <span class="val">Patent pending</span></div>
      <div class="item" data-act="signout" style="color:var(--danger)"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4M16 17l5-5-5-5M21 12H9"/></svg> Sign out</div>
    </div>

    <p class="faint" style="text-align:center;font-size:11px;margin:20px 0 0">
      MIMA · Multifunctional IoT Integrated Menstrual Aid<br>
      Indian Patent Application No. 202531001119 · Demo build
    </p>`;
  }

  function wireProfile() {
    $("#pf-theme").addEventListener("change", e => { setTheme(e.target.checked ? "dark" : "light"); rerender(); });
    $$('[data-act]').forEach(it => it.addEventListener("click", () => {
      const a = it.dataset.act;
      const map = {
        calibrate: "Hold still for 10s while we calibrate… (demo)",
        pair: "Scanning for MIMA modules over Bluetooth… (demo)",
        export: "Data export requested — you'll get an email (demo)",
        clinicians: "Dr. Nandini Rao has access until today 6:30 PM",
        "default-anon": "Toggle between Username and Anonymous per post",
        help: "Opening help centre… (demo)",
        about: "MIMA integrates a specialised garment, IoT heat therapy, physiological sensing and this app.",
        signout: "Signed out (demo)",
      };
      toast(map[a] || "Demo action");
    }));
  }

  /* ============================================================
     Router
     ============================================================ */
  const SCREENS = {
    device:     { title: "Device",     render: renderDevice,     wire: wireDevice },
    analytics:  { title: "Insights",   render: renderAnalytics,  wire: wireAnalytics },
    community:  { title: "Community",  render: renderCommunity,  wire: wireCommunity },
    assistance: { title: "Assistance", render: renderAssistance, wire: wireAssistance },
    profile:    { title: "Profile",    render: renderProfile,    wire: wireProfile },
  };

  function go(name) {
    if (!SCREENS[name]) name = "device";
    state.screen = name;
    try { history.replaceState(null, "", "#" + name); } catch (e) {}
    rerender();
    $("#screen").scrollTop = 0;
  }
  function rerender() {
    const s = SCREENS[state.screen];
    $("#topbar-sub").textContent = s.title;
    const scr = $("#screen");
    scr.innerHTML = `<div class="fade-in">${s.render()}</div>`;
    s.wire();
    $$("#bottomnav .nav-item").forEach(b =>
      b.classList.toggle("active", b.dataset.screen === state.screen));
  }

  $$("#bottomnav .nav-item").forEach(b =>
    b.addEventListener("click", () => go(b.dataset.screen)));
  $("#menu-btn").addEventListener("click", () => go("profile"));

  /* ---- live sensor jitter for realism ---- */
  // Patch just the changing values in place — a full rerender() here made the
  // whole device screen flash (DOM rebuild + fade-in replay) every tick.
  setInterval(() => {
    if (state.screen !== "device") return;
    if ($("#sheet-root").hasChildNodes()) return;
    const d = state.dev;
    d.pulse = 78 + Math.round(Math.random() * 8);
    d.emg = state.dev.mode === "auto" ? 45 + Math.round(Math.random() * 30) : 20 + Math.round(Math.random() * 15);
    d.currentTemp = +(d.targetTemp - 0.4 - Math.random() * 0.8).toFixed(1);
    d.skinTemp = +(36.2 + Math.random() * 0.5).toFixed(1);
    const set = (id, val) => { const el = document.getElementById(id); if (el) el.textContent = val; };
    set("live-current-temp", d.currentTemp.toFixed(1));
    set("live-skin-temp", d.skinTemp);
    set("live-pulse", d.pulse);
    set("live-emg", d.emg);
  }, 4000);

  /* ---- init ---- */
  initTheme();
  go((location.hash || "").replace("#", "") || "device");
  window.addEventListener("hashchange", () => {
    const h = (location.hash || "").replace("#", "");
    if (h && h !== state.screen) go(h);
  });

})();
