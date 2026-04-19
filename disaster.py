import streamlit as st
import random
import requests

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="EARTH CHAT: Connect with our Planet",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================
# 🌐 REAL-TIME DATA (Air Quality)
# =========================
@st.cache_data(ttl=600)
def fetch_real_risk():
    try:
        # Fetching PM2.5 data for Tokyo (as a baseline)
        url = "https://api.openaq.org/v2/latest?limit=1&parameter=pm25&city=Tokyo"
        r = requests.get(url, timeout=5)
        val = r.json()["results"][0]["measurements"][0]["value"]
        return val
    except:
        return 15.0 # Default value if fetch fails

pm25_val = fetch_real_risk()

# =========================
# SESSION STATE
# =========================
if "earth" not in st.session_state:
    st.session_state.earth = {"ecology": 50, "economy": 50, "society": 50}
    st.session_state.mood = 50
if "turn" not in st.session_state:
    st.session_state.turn = 0
if "history" not in st.session_state:
    st.session_state.history = []
if "game_over" not in st.session_state:
    st.session_state.game_over = False
if "tutorial" not in st.session_state:
    st.session_state.tutorial = True

# =========================
# ACTION OPTIONS (With tooltips)
# =========================
choice_map = {
    "nature": ("🌳 Protect Nature", "🌿 Air gets cleaner, but the economy might slow down."),
    "growth": ("🏭 Boost Economy", "💰 Money grows, but the air might get polluted."),
    "welfare": ("💊 Support People", "😊 Everyone is happier, but it costs more money."),
    "tech": ("🚀 Tech Innovation", "🤖 Efficiency goes up, but society might get unstable."),
    "strict": ("⚖️ New Laws", "🛡️ Order is kept, but freedom might decrease."),
    "exploit": ("⛏️ Resource Mining", "🔥 Immediate wealth, but it leaves deep scars on Earth.")
}

# =========================
# EARTH'S VOICES (Random)
# =========================
good_voices = [
    ("“Yay! I feel much lighter now!”", "(Ecology improved)"),
    ("“Thank you! I'm starting to feel energized!”", "(Earth's mood is up)"),
    ("“Let's make this planet a place where everyone smiles!”", "(Society score is rising)"),
    ("“Everything feels so balanced today!”", "(Stability detected)")
]
bad_voices = [
    ("“It's hard to breathe... I might glitch!”", "(Pollution interference detected)"),
    ("“Wait, did I press the wrong button? I'm confused...”", "(System Glitch: Unexpected feedback)"),
    ("“Ugh... I'm feeling a bit dizzy...”", "(Environment is declining)"),
    ("“Sorry... my head is spinning...”", "(Unstable atmosphere)")
]

# =========================
# LOGIC (Enhanced Gameplay)
# =========================
def apply_choice(key):
    effects = {
        "nature": (20, -15, -5), "growth": (-20, 25, 5), "welfare": (-5, -10, 20),
        "tech": (10, 10, -15), "strict": (15, -20, 15), "exploit": (-25, 20, 15)
    }
    e, m, s = effects[key]

    # 🌫️ 1. Pollution-based Glitch Rate
    # If PM2.5 is 60, there's a 60% chance actions will flip (glitch)
    interference_chance = min(0.6, pm25_val / 60)
    is_glitched = random.random() < interference_chance
    if is_glitched:
        e, m, s = -e, -m, -s

    # 🌫️ 2. Air Pollution Penalty (Continuous Damage)
    air_penalty = max(0, (pm25_val - 20) * 0.3)

    st.session_state.earth["ecology"] = max(0, min(100, st.session_state.earth["ecology"] + e - air_penalty))
    st.session_state.earth["economy"] = max(0, min(100, st.session_state.earth["economy"] + m))
    st.session_state.earth["society"] = max(0, min(100, st.session_state.earth["society"] + s))
    
    # Mood is also affected by air quality
    st.session_state.mood = max(0, min(100, st.session_state.mood + (e * 0.5) - air_penalty * 0.5))

    st.session_state.turn += 1

    voice, trans = random.choice(bad_voices if is_glitched else good_voices)
    st.session_state.history.append({
        "turn": st.session_state.turn, 
        "voice": voice, 
        "trans": trans, 
        "label": choice_map[key][0], 
        "glitch": is_glitched
    })

    if any(v <= 0 or v >= 100 for v in st.session_state.earth.values()) or st.session_state.turn >= 10:
        st.session_state.game_over = True

# =========================
# VISUAL PARAMS (Linked to Air)
# =========================
worst_v = min(st.session_state.earth.values())
if st.session_state.mood < 30 or worst_v < 30:
    msg, color, face = "Air is too toxic. Earth is breaking down.", "#ff00ff", "😱"
elif worst_v < 50:
    msg, color, face = "Earth is suffering. It needs your help.", "#ffea00", "😟"
else:
    msg, color, face = "Earth is calm. Let's keep it this way.", "#00ffff", "😊"

# Screen noise increases with pollution
noise = min(pm25_val / 100, 0.5)

# =========================
# UI STYLE
# =========================
st.markdown(f"""
<style>
html, body, [data-testid="stAppViewContainer"] {{
    height: 100vh; overflow: hidden !important;
    background: radial-gradient(circle at center, #1a0033 0%, #000000 100%) !important;
    color: {color} !important;
}}
[data-testid="stAppViewContainer"]::before {{
    content: " "; position: fixed; top: 0; left: 0; bottom: 0; right: 0;
    background: repeating-linear-gradient(0deg, rgba(255,0,255,{noise}), rgba(0,255,255,{noise}) 2px, transparent 2px, transparent 4px);
    z-index: 100; pointer-events: none; opacity: 0.3;
}}
h1, h2, h3, p {{ color: {color} !important; text-shadow: 0 0 10px {color}; }}
.hero {{ text-align:center; padding:1rem; border:2px solid {color}88; border-radius:20px; background: rgba(0,0,0,0.5); box-shadow: 0 0 20px {color}33; margin-bottom:1rem; }}
.big-face {{ font-size: 8rem; margin: 0; line-height: 1; }}
.panel {{ border: 1px solid {color}44; padding: 10px; background: rgba(255,255,255,0.03); border-radius: 10px; }}
.stProgress > div > div > div > div {{ background-color: {color} !important; height: 10px !important; }}
.stButton > button {{ border: 2px solid {color}66 !important; background: rgba(0,0,0,0.5) !important; color: {color} !important; border-radius: 15px !important; font-size: 1.1rem !important; font-weight: bold !important; text-shadow: 0 0 10px {color}; transition: all 0.3s ease; }}
.tutorial-box {{ padding:1.5rem; margin-bottom:1rem; border:2px solid {color}; border-radius:15px; background:rgba(0,0,0,0.7); box-shadow:0 0 15px {color}55; line-height: 1.6; }}
.log-container {{ height: 120px; overflow-y: auto; font-size: 0.8rem; border-top: 1px solid {color}33; padding-top: 5px; }}
</style>
""", unsafe_allow_html=True)

# =========================
# 📡 Air Quality Status
# =========================
if pm25_val < 12:
    air_label = "(Clean)"
elif pm25_val < 35:
    air_label = "(Fair)"
else:
    air_label = "(Polluted...)"

# =========================
# HEADER
# =========================
c_h1, c_h2 = st.columns([2.0, 1.5])
with c_h1:
    st.markdown(f"### 💖 EARTH CHAT: Talk to our Planet")

with c_h2:
    st.markdown(f"""
    <div style='text-align:right; border: 2px solid {color}88; padding: 10px; border-radius: 15px; background:rgba(0,0,0,0.5);'>
        <span style='font-size:1.1rem; font-weight:bold; color:{color}; text-shadow:0 0 10px {color};'>
            📡 Tokyo PM2.5: <span style="font-size:1.3rem;">{pm25_val:.1f}</span> {air_label}
        </span><br>
        <span style='font-size:0.8rem; opacity:0.9;'>Poor air quality can cause glitches and harm nature in this game!</span>
    </div>
    """, unsafe_allow_html=True)

# =========================
# MAIN CONTENT
# =========================
if not st.session_state.game_over:
    st.markdown(f"""<div class="hero"><div class="big-face">{face}</div><h2 style='margin:0.5rem 0;'>{msg}</h2></div>""", unsafe_allow_html=True)

    if st.session_state.tutorial:
        st.markdown(f"""
        <div class="tutorial-box">
            <h3 style='margin-top:0;'>🌍 “Hello! I'm Earth!”</h3>
            <p>I'm putting the next <b>“10 Years”</b> of my future in your hands!<br>
            Please choose one action for me each year.</p>
            <ul style="font-size: 0.95rem;">
                <li>🌳 Protecting <b>Nature</b> makes me feel better, but <b>Economy</b> is important too... it's all about balance!</li>
                <li>⚠️ If any meter hits <b>0 or 100</b>, I'll get too tired and the timeline might stop before we reach Year 10.</li>
            </ul>
            <p><b>📡 Today's Air Impact:</b><br>
            If the real-world air is polluted, I might <b>glitch (act opposite)</b> or lose some health. Be careful!</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🌏 Let's start the 10-year journey", use_container_width=True):
            st.session_state.tutorial = False
            st.rerun()

    if not st.session_state.tutorial:
        cols = st.columns(4)
        for i, (l, k) in enumerate([("🌳 Nature", "ecology"), ("💰 Economy", "economy"), ("👥 Society", "society"), ("🧠 Wellbeing", "mood")]):
            val = st.session_state.earth.get(k, st.session_state.mood)
            cols[i].markdown(f"<div class='panel' style='text-align:center;'><b>{l}</b><br>{val:.0f}%</div>", unsafe_allow_html=True)
            cols[i].progress(val/100)

        st.markdown(f"<div style='text-align:center; margin-top:1rem;'><b>📅 Current Status: Year {st.session_state.turn + 1} Selection</b></div>", unsafe_allow_html=True)
        c_cols = st.columns(3)
        keys = list(choice_map.keys())
        for i in range(3):
            with c_cols[i]:
                k1, k2 = keys[i*2], keys[i*2+1]
                if st.button(f"**{choice_map[k1][0]}**\n\n{choice_map[k1][1]}", key=k1, use_container_width=True):
                    apply_choice(k1); st.rerun()
                if st.button(f"**{choice_map[k2][0]}**\n\n{choice_map[k2][1]}", key=k2, use_container_width=True):
                    apply_choice(k2); st.rerun()

        st.markdown("<div class='panel log-container'>", unsafe_allow_html=True)
        if not st.session_state.history:
            st.markdown("<code>> Please select your policy for Year 1.</code>", unsafe_allow_html=True)
        else:
            for h in reversed(st.session_state.history):
                c = "#f0f" if h['glitch'] else color
                st.markdown(f"<div style='margin-bottom:8px;'><span style='font-size:0.7rem; opacity:0.6;'>Year {h['turn']}: {h['label']}</span><br><b style='color:{c}; font-size:1.1rem;'>🌍 Earth: {h['voice']}</b><br><span style='font-size:0.8rem; opacity:0.7;'>{h['trans']}</span></div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

# =========================
# GAME OVER (Gentle Storytelling)
# =========================
if st.session_state.game_over:
    ended_by_turn = st.session_state.turn >= 10
    
    end_reason_text = (
        "Our 10-year voyage has come to an end!"
        if ended_by_turn else
        f"Earth got a bit tired at Year {st.session_state.turn}... Let's take a little break."
    )

    eco = st.session_state.earth["ecology"]
    eco2 = st.session_state.earth["economy"]
    eco3 = st.session_state.earth["society"]
    mood = st.session_state.mood

    if eco >= 60:
        end_face, end_msg, end_color = "😊", "The future in 10 years looks so bright!\nYour choices saved our planet.", "#00ffcc"
        future_card = "🌈 **Future Forecast: Radiant Green Earth**\nThanks to 10 years of care, nature and people are thriving together!"
        closing_text = "I'll never forget the 10-year story you built."
    elif eco >= 30:
        end_face, end_msg, end_color = "😟", "The future in 10 years looks a bit tough...\nBut the path you've built is still there.", "#ffee00"
        future_card = "🌤️ **Future Forecast: Earth in Transition**\nThings are starting to improve. A few more changes could make a big difference!"
        closing_text = "I'll never forget the 10-year story you built."
    else:
        # 🌪️ BAD ENDING (Revised: Gentle & Educational)
        end_face = "😢"
        end_msg = (
            "Earth is feeling very tired right now...\n"
            "But let's think together about how we can make things better."
        )
        end_color = "#ff00aa"
        future_card = (
            "🌪️ **Future Forecast: Earth SOS**\n"
            "If we keep going like this, nature might face a very difficult future.\n"
            "Try talking with your family or friends about how we can protect our planet.\n"
            "Your new ideas can be the power that changes the next 10 years!"
        )
        closing_text = "Let's work together to make the next 10 years even better."

    st.markdown(f"""
    <div style='padding:2rem; text-align:center; border:3px solid {end_color}; border-radius:20px; background:rgba(0,0,0,0.6); box-shadow:0 0 25px {end_color}; margin-top:1rem;'>
        <p style='opacity:0.8; font-size:1.1rem; margin-bottom:1rem;'>{end_reason_text}</p>
        <div style='font-size:6rem;'>{end_face}</div>
        <h2 style='white-space:pre-line; color:{end_color}; text-shadow:0 0 15px {end_color};'>{end_msg}</h2>
        <p style='opacity:0.7; margin-top:1rem;'>{closing_text}</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"### 🌏 Final Status after {st.session_state.turn} Years")
    st.markdown(f"- 🌳 **Nature**: {eco:.0f}  \n- 💰 **Economy**: {eco2:.0f}  \n- 👥 **Society**: {eco3:.0f}  \n- 🧠 **Wellbeing**: {mood:.0f}")
    st.markdown("---")
    st.markdown(f"### 🔮 {future_card}")
    st.markdown(f"""<div style='margin-top:1.5rem; padding:1rem; text-align:center; border:2px dashed {end_color}; border-radius:15px; background:rgba(0,0,0,0.4);'><p style='font-size:1.2rem;'>🌍 “Come play again! What kind of future will you build next?”</p></div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔄 Start a New 10-Year Journey", use_container_width=True):
        for k in ["earth", "turn", "history", "game_over", "tutorial"]:
            st.session_state.pop(k, None)
        st.rerun()
