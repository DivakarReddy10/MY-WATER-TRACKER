"""💧 My Water Tracker - a responsive, animated Streamlit hydration app."""
import json
import random
from datetime import date, datetime, timedelta
from pathlib import Path

import streamlit as st

st.set_page_config(page_title="My Water Tracker", page_icon="💧", layout="centered")

DATA_FILE = Path(__file__).with_name("water_data.json")
TODAY = date.today().isoformat()
TIPS = [
    "Start your day with a glass of water before coffee ☕",
    "Keep a bottle on your desk - what you see, you drink 👀",
    "Feeling hungry? Sometimes it's thirst. Sip first 🍎",
    "Add lemon or mint for a refreshing twist 🍋",
    "Drink a glass before every meal 🍽️",
    "Set small hourly sips instead of big gulps ⏰",
    "Water helps focus, mood and energy ⚡",
]
BADGES = [
    (250, "🥉", "First Sip"),
    (1000, "🥈", "Halfway Hero"),
    (2000, "🥇", "Goal Getter"),
    (3000, "🏆", "Hydration Legend"),
]


# ---------- storage ----------
def load_data():
    try:
        return json.loads(DATA_FILE.read_text())
    except Exception:
        return {"goal": 2000, "logs": {}, "celebrated": []}


def save_data():
    try:
        DATA_FILE.write_text(json.dumps(st.session_state.data))
    except Exception:
        pass  # read-only hosting: keep working in memory


if "data" not in st.session_state:
    st.session_state.data = load_data()
    st.session_state.flash = ""
data = st.session_state.data
data.setdefault("celebrated", [])
logs = data["logs"].setdefault(TODAY, [])


def total_for(day):
    return sum(e["ml"] for e in data["logs"].get(day, []))


# ---------- actions ----------
def add_water(ml):
    data["logs"][TODAY].append({"t": datetime.now().strftime("%H:%M"), "ml": int(ml)})
    st.session_state.flash = f"+{ml} ml 💦"
    save_data()


def undo():
    if data["logs"][TODAY]:
        data["logs"][TODAY].pop()
        if total_for(TODAY) < data["goal"] and TODAY in data["celebrated"]:
            data["celebrated"].remove(TODAY)
        save_data()


def reset_day():
    data["logs"][TODAY] = []
    if TODAY in data["celebrated"]:
        data["celebrated"].remove(TODAY)
    st.session_state.flash = "Fresh start! 🌱"
    save_data()


def set_goal():
    data["goal"] = int(st.session_state.goal_l * 1000)
    save_data()


# ---------- numbers ----------
goal = data["goal"]
total = total_for(TODAY)
remaining = max(goal - total, 0)
pct = min(total / goal * 100, 100) if goal else 0
streak, d = 0, date.today()
if total < goal:
    d -= timedelta(days=1)
while total_for(d.isoformat()) >= goal and goal > 0 and streak < 365:
    streak += 1
    d -= timedelta(days=1)
if total >= goal:
    pass

if pct >= 100:
    msg, mood = "🎉 Goal reached! You're a hydration superstar!", "🏆"
elif pct >= 75:
    msg, mood = "So close! Just a few more sips 🚀", "😎"
elif pct >= 50:
    msg, mood = "Halfway there - keep flowing! 🌊", "😄"
elif pct >= 25:
    msg, mood = "Great start! Your body says thanks 💙", "🙂"
elif total > 0:
    msg, mood = "Every sip counts. Keep going! 💧", "🙂"
else:
    msg, mood = "Let's drink some water today!", "🥤"

# ---------- style ----------
st.markdown(
    f"""
<style>
.stApp {{background: linear-gradient(160deg,#e0f7ff 0%,#b3e5fc 45%,#e8f5ff 100%);}}
.block-container {{padding-top:1.2rem; max-width:720px;}}
h1.title {{text-align:center; color:#01579b; margin:0; font-size:clamp(1.8rem,6vw,2.8rem);
  animation: pop .8s ease;}}
.sub {{text-align:center; color:#0277bd; margin-bottom:.8rem;}}
@keyframes pop {{0%{{transform:scale(.6);opacity:0}}100%{{transform:scale(1);opacity:1}}}}
@keyframes wave {{0%{{transform:translateX(0)}}100%{{transform:translateX(-50%)}}}}
@keyframes rise {{0%{{transform:translateY(0);opacity:.0}}20%{{opacity:.8}}100%{{transform:translateY(-220px);opacity:0}}}}
@keyframes float {{0%,100%{{transform:translateY(0)}}50%{{transform:translateY(-8px)}}}}
@keyframes glow {{0%,100%{{box-shadow:0 0 10px #4fc3f7}}50%{{box-shadow:0 0 30px #29b6f6}}}}
.glass-wrap {{display:flex; justify-content:center; animation: float 4s ease-in-out infinite;}}
.glass {{position:relative; width:170px; height:240px; border:5px solid rgba(255,255,255,.9);
  border-top:none; border-radius:0 0 40px 40px; overflow:hidden; background:rgba(255,255,255,.35);
  box-shadow:0 10px 30px rgba(1,87,155,.25); {"animation: glow 2s infinite;" if pct>=100 else ""}}}
.water {{position:absolute; bottom:0; left:0; width:100%; height:{pct}%;
  background:linear-gradient(180deg,#4fc3f7,#0288d1); transition:height 1.2s cubic-bezier(.2,.8,.2,1);}}
.wave {{position:absolute; top:-18px; left:0; width:200%; height:36px; animation: wave 3s linear infinite;
  background:radial-gradient(circle at 25px 36px,transparent 24px,#4fc3f7 25px) repeat-x; background-size:50px 36px;}}
.wave.b {{animation-duration:5s; opacity:.6; top:-24px}}
.bubble {{position:absolute; bottom:8px; width:10px; height:10px; border-radius:50%;
  background:rgba(255,255,255,.7); animation: rise 3s infinite;}}
.pct {{position:absolute; inset:0; display:flex; align-items:center; justify-content:center;
  font-size:2.2rem; font-weight:800; color:#fff; text-shadow:0 2px 8px rgba(0,0,0,.35); z-index:3;}}
.card {{background:rgba(255,255,255,.75); backdrop-filter:blur(6px); border-radius:18px; padding:.8rem;
  text-align:center; box-shadow:0 4px 14px rgba(1,87,155,.15); transition:transform .25s; animation: pop .6s ease;}}
.card:hover {{transform:translateY(-4px) scale(1.03);}}
.card b {{display:block; font-size:1.5rem; color:#01579b;}}
.card span {{color:#0277bd; font-size:.85rem;}}
.msg {{text-align:center; font-size:1.2rem; font-weight:700; color:#01579b; margin:.8rem 0;
  padding:.7rem; border-radius:16px; background:rgba(255,255,255,.8); animation: pop .6s ease;}}
.badge {{display:inline-block; margin:3px; padding:6px 12px; border-radius:20px; font-size:.85rem;
  background:#fff; box-shadow:0 2px 8px rgba(0,0,0,.1);}}
.badge.off {{filter:grayscale(1); opacity:.45}}
.flash {{position:fixed; top:70px; right:20px; z-index:999; background:#0288d1; color:#fff;
  padding:.5rem 1rem; border-radius:20px; font-weight:700; animation: pop .4s ease, fade 2.5s forwards;}}
@keyframes fade {{0%,70%{{opacity:1}}100%{{opacity:0;visibility:hidden}}}}
div.stButton > button {{width:100%; border-radius:16px; border:none; font-weight:700; padding:.7rem 0;
  background:linear-gradient(135deg,#29b6f6,#0277bd); color:#fff; transition:all .2s;}}
div.stButton > button:hover {{transform:translateY(-3px) scale(1.04); box-shadow:0 8px 18px rgba(2,119,189,.4); color:#fff;}}
div.stButton > button:active {{transform:scale(.94);}}
</style>
""",
    unsafe_allow_html=True,
)

# ---------- header ----------
st.markdown('<h1 class="title">💧 My Water Tracker</h1>', unsafe_allow_html=True)
st.markdown(
    f'<div class="sub">{date.today().strftime("%A, %d %B %Y")} · {mood}</div>',
    unsafe_allow_html=True,
)
if st.session_state.flash:
    st.markdown(f'<div class="flash">{st.session_state.flash}</div>', unsafe_allow_html=True)
    st.session_state.flash = ""

# ---------- glass ----------
bubbles = "".join(
    f'<i class="bubble" style="left:{random.randint(10,85)}%;animation-delay:{i*0.5}s;'
    f'width:{random.randint(6,12)}px;height:{random.randint(6,12)}px"></i>'
    for i in range(6)
) if pct > 0 else ""
st.markdown(
    f"""<div class="glass-wrap"><div class="glass">
    <div class="water"><div class="wave"></div><div class="wave b"></div>{bubbles}</div>
    <div class="pct">{int(pct)}%</div></div></div>""",
    unsafe_allow_html=True,
)
st.progress(int(pct))

# ---------- stats ----------
c1, c2, c3, c4 = st.columns(4)
for col, val, label in [
    (c1, f"{goal/1000:.2f} L", "🎯 Goal"),
    (c2, f"{total/1000:.2f} L", "🥤 Drunk"),
    (c3, f"{remaining/1000:.2f} L", "⏳ Remaining"),
    (c4, f"{streak} 🔥", "Day streak"),
]:
    col.markdown(f'<div class="card"><b>{val}</b><span>{label}</span></div>', unsafe_allow_html=True)

st.markdown(f'<div class="msg">{msg}</div>', unsafe_allow_html=True)

# celebration (once per day)
if total >= goal > 0 and TODAY not in data["celebrated"]:
    data["celebrated"].append(TODAY)
    save_data()
    st.balloons()
    st.toast("Daily goal achieved! 🏆", icon="🎉")

# ---------- add buttons ----------
st.subheader("➕ Add water")
b = st.columns(4)
for col, (label, ml) in zip(b, [("🥛 Sip\n100 ml", 100), ("🥛 Glass\n250 ml", 250),
                                ("🍶 Cup\n500 ml", 500), ("🧴 Bottle\n750 ml", 750)]):
    col.button(label, key=f"add{ml}", on_click=add_water, args=(ml,))

cc1, cc2 = st.columns([2, 1])
custom = cc1.number_input("Custom amount (ml)", 10, 2000, 300, 50, label_visibility="collapsed")
cc2.button("Add custom", on_click=add_water, args=(custom,))

u1, u2 = st.columns(2)
u1.button("↩️ Undo last", on_click=undo, disabled=not logs)
u2.button("🔄 Reset today", on_click=reset_day, disabled=not logs)

# ---------- settings ----------
with st.expander("⚙️ Set custom daily goal"):
    st.number_input("Daily goal (litres)", 0.5, 10.0, goal / 1000, 0.25,
                    key="goal_l", on_change=set_goal)
    st.caption("Tip: most adults aim for about 2–3 litres, depending on weight and activity.")

# ---------- badges ----------
st.subheader("🏅 Today's badges")
st.markdown(
    "".join(f'<span class="badge {"" if total>=t else "off"}">{e} {n}</span>' for t, e, n in BADGES),
    unsafe_allow_html=True,
)

# ---------- history ----------
st.subheader("📈 Last 7 days")
days = [(date.today() - timedelta(days=i)) for i in range(6, -1, -1)]
st.bar_chart({d.strftime("%a"): total_for(d.isoformat()) / 1000 for d in days}, color="#0288d1")

with st.expander("🧾 Today's log"):
    if logs:
        for e in reversed(logs):
            st.write(f"🕒 {e['t']} — **{e['ml']} ml**")
    else:
        st.write("No water logged yet today.")

st.info("💡 " + random.choice(TIPS))
