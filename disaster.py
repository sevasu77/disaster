import streamlit as st 

import random 

  

# ----------------------------- 

# ページ設定 

# ----------------------------- 

st.set_page_config(page_title="Earth Risk Monitor", layout="wide") 

  

# ----------------------------- 

# ① & ② タイトルと概要 

# ----------------------------- 

st.markdown("<h1>🌍 Earth Risk Monitor</h1>", unsafe_allow_html=True) 

st.markdown("<p style='margin-bottom: 2rem;'>Real-time environmental risk indicator (simulated)</p>", unsafe_allow_html=True) 

  

# ----------------------------- 

# ⑤ リスクタイプの選択（サイドバーに配置してUIをスッキリ） 

# ----------------------------- 

with st.sidebar: 

    st.header("Settings") 

    risk_type = st.selectbox( 

        "Select Risk Type", 

        ["Climate Change", "Natural Disaster", "Air Pollution", "Ocean Health"] 

    ) 

    # ④ ボタン名の変更 

    if st.button("🔄 Update Risk Status"): 

        st.rerun() 

     

    st.markdown("---") 

    # ⑧ 小さい説明 

    st.caption("This is a conceptual UI for environmental risk awareness.") 

  

# ----------------------------- 

# デモ用：危険度ランダム生成 

# ----------------------------- 

risk = random.randint(0, 100) 

  

# ----------------------------- 

# 状態判定 

# ----------------------------- 

if risk < 20: 

    state = "SAFE" 

elif risk < 40: 

    state = "NOTICE" 

elif risk < 60: 

    state = "WARNING" 

elif risk < 80: 

    state = "DANGER" 

else: 

    state = "CRASH" 

  

# ----------------------------- 

# ⑥ 理由をリスク別に変える 

# ----------------------------- 

reasons_map = { 

    "Climate Change": [ 

        "Global temperature rising", 

        "CO2 levels increasing", 

        "Extreme weather patterns" 

    ], 

    "Natural Disaster": [ 

        "Earthquake activity detected", 

        "Typhoon formation risk", 

        "Flood probability increasing" 

    ], 

    "Air Pollution": [ 

        "PM2.5 levels rising", 

        "Urban pollution spike", 

        "Industrial emissions detected" 

    ], 

    "Ocean Health": [ 

        "Coral bleaching alert", 

        "Ocean temperature rising", 

        "Plastic pollution increase" 

    ] 

} 

reason = random.choice(reasons_map[risk_type]) 

  

# ----------------------------- 

# 状態ごとのスタイル 

# ----------------------------- 

styles = { 

    "SAFE": {"bg": "#0f172a", "color": "#22c55e", "anim": ""}, 

    "NOTICE": {"bg": "#1e293b", "color": "#eab308", "anim": ""}, 

    "WARNING": {"bg": "#3f1d1d", "color": "#f97316", "anim": "pulse 1.5s infinite"}, 

    "DANGER": {"bg": "#450a0a", "color": "#ef4444", "anim": "pulse 1s infinite"}, 

    "CRASH": {"bg": "#000000", "color": "#ff0000", "anim": "shake 0.2s infinite"} 

} 

style = styles[state] 

  

# ----------------------------- 

# CSS 

# ----------------------------- 

st.markdown(f""" 

<style> 

[data-testid="stAppViewContainer"] {{ 

    background-color: {style["bg"]}; 

    animation: {style["anim"]}; 

    transition: background-color 0.5s ease; 

}} 

  

/* サイドバーの背景色も調整して統一感を出す */ 

[data-testid="stSidebar"] {{ 

    background-color: rgba(0,0,0,0.3); 

}} 

  

h1, p, label, .stSelectbox {{ 

    color: {style["color"]} !important; 

}} 

  

h1 {{ 

    text-align: center; 

    font-size: 4rem; 

    font-weight: 800; 

}} 

  

.status-label {{ 

    text-align: center; 

    font-size: 1.2rem; 

    letter-spacing: 0.2rem; 

    margin-bottom: 0px; 

}} 

  

.reason-text {{ 

    text-align: center; 

    font-size: 1.8rem; 

    font-weight: 300; 

}} 

  

@keyframes pulse {{ 

    0% {{ opacity: 1; }} 

    50% {{ opacity: 0.7; }} 

    100% {{ opacity: 1; }} 

}} 

  

@keyframes shake {{ 

    0% {{ transform: translate(0px, 0px); }} 

    25% {{ transform: translate(4px, -4px); }} 

    50% {{ transform: translate(-4px, 4px); }} 

    75% {{ transform: translate(4px, 4px); }} 

    100% {{ transform: translate(0px, 0px); }} 

}} 

</style> 

""", unsafe_allow_html=True) 

  

# ----------------------------- 

# 表示メインエリア 

# ----------------------------- 

# ③ ラベル追加 

st.markdown(f"<p class='status-label'>CURRENT STATUS</p>", unsafe_allow_html=True) 

st.markdown(f"<h1>{state}</h1>", unsafe_allow_html=True) 

  

# ⑦ プログレスバー 

# カスタムCSSでプログレスバーの色も変えるとさら良くなります 

st.progress(risk) 

  

# 理由の表示 

st.markdown(f"<p class='reason-text'>{reason}</p>", unsafe_allow_html=True) 

  

# ⑨ フッター 

st.markdown("<br><br><hr>", unsafe_allow_html=True) 

st.markdown("<p style='font-size: 0.8rem; opacity: 0.7;'>Built for Earth Day 🌍 | System Check: OK</p>", unsafe_allow_html=True) 