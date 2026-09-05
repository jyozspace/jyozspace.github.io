/* ============================================================
   MIMA demo — dummy data
   ============================================================ */
window.MIMA_DATA = {

  user: {
    name: "Aarohi Menon",
    username: "u/aarohi_m",
    initials: "AM",
    joined: "Since Mar 2025",
    cycleDay: 3,
    cycleLen: 28,
    periodLen: 5,
    nextPeriod: "in 25 days",
    plan: "MIMA Care+",
  },

  device: {
    name: "MIMA Module · A2F9",
    firmware: "v2.4.1",
    battery: 78,
    signal: "Strong",
    targetTemp: 42,
    currentTemp: 41.2,
    mode: "auto",          // auto | manual
    heating: true,
    timerMin: 20,
    skinTemp: 36.4,
    pulse: 82,
    emg: 58,               // % contraction intensity
  },

  /* ---- Analytics ---- */
  crampsByHour: [
    { h: "12a", v: 22, hot: false }, { h: "3a", v: 34, hot: false },
    { h: "6a", v: 58, hot: true },  { h: "9a", v: 41, hot: false },
    { h: "12p", v: 30, hot: false },{ h: "3p", v: 26, hot: false },
    { h: "6p", v: 47, hot: false }, { h: "9p", v: 71, hot: true },
  ],
  painTrend: [3, 4, 6, 7, 5, 4, 2, 2, 3, 5, 6, 4, 3, 2],
  emgTrend: [20, 35, 55, 72, 60, 40, 25, 18, 22, 44, 65, 50, 30, 20],
  cycleHistory: [
    { m: "Apr", len: 29, pain: 6 }, { m: "May", len: 28, pain: 7 },
    { m: "Jun", len: 27, pain: 5 }, { m: "Jul", len: 28, pain: 4 },
    { m: "Aug", len: 28, pain: 4 }, { m: "Sep", len: 28, pain: 3 },
  ],
  sleepByPhase: [
    { p: "Menstrual", v: 6.1 }, { p: "Follicular", v: 7.4 },
    { p: "Ovulation", v: 7.1 }, { p: "Luteal", v: 6.6 },
  ],
  insights: [
    { icon: "🌙", title: "Evening cramp peak", body: "Your abdominal muscle activity spikes around 9–10 PM on days 1–2. MIMA now pre-warms 15 min earlier on those evenings." },
    { icon: "📉", title: "Pain trending down", body: "Average reported pain fell from 7/10 (May) to 3/10 this cycle — closed-loop heat therapy sessions are up 40%." },
    { icon: "💗", title: "Elevated resting pulse", body: "Resting pulse ran 6 bpm higher across your last luteal phase. Worth mentioning at your next consult." },
    { icon: "🛌", title: "Sleep dips during menstruation", body: "You lose ~1.3 hrs of sleep on menstrual nights. Try a 20-min heat session before bed." },
  ],

  /* ---- Community ---- */
  groups: [
    { emoji: "🔥", name: "Cramp Warriors", count: "12.4k" },
    { emoji: "🌱", name: "PCOS Support", count: "8.1k" },
    { emoji: "🧘", name: "Endo Sisters", count: "5.6k" },
    { emoji: "💊", name: "First Period", count: "3.2k" },
    { emoji: "🌸", name: "Perimenopause", count: "2.9k" },
  ],
  posts: [
    {
      id: 1, anon: false, author: "u/lunar_tide", initials: "LT", color: "#EC6FA9",
      group: "Cramp Warriors", time: "2h",
      title: "MIMA auto-mode genuinely changed my day-1s",
      body: "I was skeptical about the EMG thing but it kicks in before I even register the cramp starting. Went to work on day 1 for the first time in years. Anyone else pairing it with magnesium?",
      tags: ["auto-mode", "win", "day-1"], up: 214, comments: [
        { anon: true, author: "Anonymous", time: "1h", body: "Magnesium glycinate at night + MIMA = my combo. Game changer." },
        { anon: false, author: "u/sea_glass", time: "48m", body: "Same experience. The pre-warming is the underrated part." },
      ],
    },
    {
      id: 2, anon: true, author: "Anonymous", initials: "A", color: "#8E4EC6",
      group: "Endo Sisters", time: "5h",
      title: "How do you explain endo pain to a new partner?",
      body: "Three weeks in and I don't know how to bring up that some days I physically cannot move. Scared of scaring him off but hiding it is worse. How did you all handle this?",
      tags: ["endometriosis", "relationships", "advice"], up: 156, comments: [
        { anon: false, author: "u/quietstorm", time: "4h", body: "I sent an article + said 'this is me ~4 days a month, ask me anything.' The ones worth keeping ask questions." },
        { anon: true, author: "Anonymous", time: "3h", body: "Sharing my MIMA analytics screen actually helped him get that it's real and measurable." },
        { anon: false, author: "u/mango_lassi", time: "2h", body: "You're not a burden. Framing it as 'here's how you can help' worked for me." },
      ],
    },
    {
      id: 3, anon: false, author: "u/dr_reddy_ob", initials: "DR", color: "#6FCF97",
      group: "PCOS Support", time: "8h",
      title: "[Verified OB-GYN] Answering PCOS + heat therapy questions this week",
      body: "Hi all — I run a clinic in Bengaluru and I'm doing a weekly thread. Drop questions about insulin resistance, cycle irregularity, or using localized heat for pain and I'll answer in batches. Not medical advice for your specific case, but happy to give general guidance.",
      tags: ["verified", "PCOS", "AMA"], up: 402, comments: [
        { anon: true, author: "Anonymous", time: "6h", body: "Does heat therapy affect ovulation timing at all?" },
        { anon: false, author: "u/thornbird", time: "5h", body: "Following. My cycles are 40+ days and nothing has helped." },
      ],
    },
    {
      id: 4, anon: false, author: "u/craft_witch", initials: "CW", color: "#F2C14E",
      group: "First Period", time: "1d",
      title: "DIY: sewed extra MIMA wing-pockets onto my older underwear",
      body: "Pattern + photos in comments. Took 20 min per pair with a basic machine. The module clips in fine. Not affiliated, just wanted more colors than the starter pack.",
      tags: ["DIY", "guide", "garment"], up: 88, comments: [
        { anon: false, author: "u/needle_moss", time: "20h", body: "This is brilliant, thank you for the measurements." },
      ],
    },
    {
      id: 5, anon: true, author: "Anonymous", initials: "A", color: "#F2795B",
      group: "Cramp Warriors", time: "1d",
      title: "Reminder that 'just take a painkiller' is not a personality",
      body: "Had a manager say this today. Posting so someone else feels less alone. We measure our cramps now — the data is right there. It's not in our heads.",
      tags: ["vent", "workplace"], up: 331, comments: [
        { anon: true, author: "Anonymous", time: "22h", body: "Solidarity. I exported my analytics PDF for HR. Worked." },
      ],
    },
  ],

  /* ---- Assistance ---- */
  doctors: [
    { id: 1, name: "Dr. Nandini Rao", spec: "Gynaecologist · Endometriosis", emoji: "👩‍⚕️", rating: 4.9, reviews: 312, exp: "14 yrs", fee: "₹700", next: "Today 5:30 PM", lang: "EN · HI · KN" },
    { id: 2, name: "Dr. Farida Qureshi", spec: "Obstetrician · PCOS", emoji: "🩺", rating: 4.8, reviews: 208, exp: "11 yrs", fee: "₹650", next: "Tomorrow 11:00 AM", lang: "EN · HI · UR" },
    { id: 3, name: "Dr. Leela Menon", spec: "Adolescent Gynaecology", emoji: "👩‍⚕️", rating: 5.0, reviews: 96, exp: "9 yrs", fee: "₹600", next: "Mon 3:00 PM", lang: "EN · ML · TA" },
  ],
  slots: ["9:00", "9:30", "10:00", "10:30", "11:00", "11:30", "5:00", "5:30", "6:00"],
  goneSlots: ["10:00", "11:30"],
  consultChat: [
    { who: "them", t: "9:02 AM", body: "Morning Aarohi — I've had a look at the analytics you shared. Your luteal-phase pulse elevation is mild but consistent." },
    { who: "them", t: "9:02 AM", body: "How are the evening cramps this cycle compared to last?" },
    { who: "me", t: "9:05 AM", body: "Much better honestly. Peak pain was 3/10 vs 7 last month. Auto-mode heat is doing a lot of the work." },
    { who: "them", t: "9:07 AM", body: "That's great. Let's keep the current routine and review after one more cycle. I'll note a possible iron panel if fatigue persists." },
    { who: "me", t: "9:08 AM", body: "Sounds good. Thank you!" },
  ],
  upcomingConsult: { doc: "Dr. Nandini Rao", when: "Today · 5:30 PM", type: "Video call", emoji: "👩‍⚕️" },

  /* ---- Emergency ---- */
  sosPresets: [
    { id: "pad", e: "🩸", n: "Sanitary pad", d: "Regular / overnight" },
    { id: "tampon", e: "🌀", n: "Tampon", d: "Any absorbency" },
    { id: "painkiller", e: "💊", n: "Painkiller", d: "Ibuprofen / paracetamol" },
    { id: "cup", e: "🌸", n: "Menstrual cup", d: "Spare / sanitiser" },
    { id: "clothes", e: "👖", n: "Change of clothes", d: "Leak emergency" },
    { id: "custom", e: "✏️", n: "Custom request", d: "Type your own" },
  ],
  responders: [
    { initials: "PK", name: "Priya (u/pk_here)", note: "Has pads + spare leggings", dist: "40 m · same building" },
    { initials: "RS", name: "Anonymous MIMA user", note: "Ibuprofen + pads", dist: "120 m" },
    { initials: "MT", name: "Meera (u/meera_t)", note: "Pads, tampons, heat patch", dist: "230 m" },
  ],
  incoming: [
    { t: "Pad needed — 2nd floor women's washroom", d: "Anonymous · 60 m away · 3 min ago", },
  ],
};
