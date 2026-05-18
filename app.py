"""
app.py — Spam Email Detector
Streamlit + Scikit-learn | Deployed via GitHub + Render
"""

import streamlit as st
import pickle
import re
import time
from datetime import datetime

# ─────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Spam Email Detector",
    page_icon="🛡️",
    layout="centered",
)

# ─────────────────────────────────────────────
#  GLOBAL CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

.stApp {
  background: linear-gradient(160deg, #0f0c29, #1a1a2e, #16213e);
  color: #e2e8f0;
}

#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 1.5rem; max-width: 760px; }

/* ── Hero ── */
.hero {
  text-align: center;
  padding: 2.5rem 1rem 1.5rem;
  margin-bottom: 1.5rem;
}
.hero-icon { font-size: 3.5rem; margin-bottom: 0.5rem; }
.hero-title {
  font-size: 2.2rem;
  font-weight: 800;
  background: linear-gradient(135deg, #667eea, #764ba2, #f093fb);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin: 0;
}
.hero-sub {
  color: #64748b;
  font-size: 0.9rem;
  margin-top: 0.4rem;
}
.hero-badges {
  display: flex;
  justify-content: center;
  gap: 0.5rem;
  margin-top: 1rem;
  flex-wrap: wrap;
}
.badge {
  background: rgba(102,126,234,0.15);
  border: 1px solid rgba(102,126,234,0.4);
  color: #a5b4fc;
  padding: 0.2rem 0.75rem;
  border-radius: 20px;
  font-size: 0.72rem;
  font-weight: 600;
}

/* ── Cards ── */
.card {
  background: rgba(15,23,42,0.7);
  border: 1px solid rgba(51,65,85,0.5);
  border-radius: 16px;
  padding: 1.4rem 1.6rem;
  margin-bottom: 1.2rem;
  backdrop-filter: blur(10px);
}
.card-title {
  font-size: 0.7rem;
  font-weight: 700;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: #475569;
  margin-bottom: 0.8rem;
}

/* ── Result Cards ── */
.result-spam {
  background: linear-gradient(135deg, rgba(239,68,68,0.15), rgba(185,28,28,0.08));
  border: 1px solid rgba(239,68,68,0.5);
  border-radius: 16px;
  padding: 1.8rem;
  text-align: center;
  animation: pulse-red 2s infinite;
  margin-bottom: 1.2rem;
}
.result-ham {
  background: linear-gradient(135deg, rgba(16,185,129,0.15), rgba(5,150,105,0.08));
  border: 1px solid rgba(16,185,129,0.5);
  border-radius: 16px;
  padding: 1.8rem;
  text-align: center;
  margin-bottom: 1.2rem;
}
@keyframes pulse-red {
  0%,100% { box-shadow: 0 0 0 0 rgba(239,68,68,0.2); }
  50%      { box-shadow: 0 0 0 12px rgba(239,68,68,0); }
}
.result-icon { font-size: 3rem; margin-bottom: 0.4rem; }
.result-label {
  font-size: 1.8rem;
  font-weight: 800;
  margin: 0;
  line-height: 1.1;
}
.label-spam { color: #f87171; }
.label-ham  { color: #34d399; }
.result-desc { color: #94a3b8; font-size: 0.85rem; margin-top: 0.4rem; }

/* ── Confidence Bar ── */
.conf-wrap { margin-top: 1rem; }
.conf-row {
  display: flex;
  justify-content: space-between;
  font-size: 0.8rem;
  color: #64748b;
  margin-bottom: 0.3rem;
}
.conf-val { font-weight: 700; color: #e2e8f0; }
.bar-bg {
  background: rgba(51,65,85,0.5);
  border-radius: 8px;
  height: 8px;
  overflow: hidden;
}
.bar-fill-spam {
  height: 100%;
  border-radius: 8px;
  background: linear-gradient(90deg, #ef4444, #f87171);
  transition: width 0.8s ease;
}
.bar-fill-ham {
  height: 100%;
  border-radius: 8px;
  background: linear-gradient(90deg, #10b981, #34d399);
  transition: width 0.8s ease;
}

/* ── Tips ── */
.tip-item {
  display: flex;
  align-items: flex-start;
  gap: 0.6rem;
  padding: 0.5rem 0;
  border-bottom: 1px solid rgba(51,65,85,0.3);
  font-size: 0.82rem;
  color: #94a3b8;
}
.tip-item:last-child { border-bottom: none; }
.tip-icon { font-size: 1rem; flex-shrink: 0; margin-top: 0.05rem; }

/* ── History ── */
.hist-row {
  display: flex;
  align-items: center;
  gap: 0.8rem;
  padding: 0.5rem 0;
  border-bottom: 1px solid rgba(51,65,85,0.25);
  font-size: 0.8rem;
}
.hist-row:last-child { border-bottom: none; }
.pill-spam {
  background: rgba(239,68,68,0.15);
  color: #f87171;
  padding: 0.15rem 0.6rem;
  border-radius: 20px;
  font-size: 0.7rem;
  font-weight: 600;
  white-space: nowrap;
}
.pill-ham {
  background: rgba(16,185,129,0.15);
  color: #34d399;
  padding: 0.15rem 0.6rem;
  border-radius: 20px;
  font-size: 0.7rem;
  font-weight: 600;
  white-space: nowrap;
}

/* Streamlit textarea */
div[data-testid="stTextArea"] textarea {
  background: rgba(15,23,42,0.8) !important;
  border: 1px solid rgba(51,65,85,0.6) !important;
  border-radius: 12px !important;
  color: #e2e8f0 !important;
  font-family: 'Inter', sans-serif !important;
  font-size: 0.9rem !important;
}
div[data-testid="stTextArea"] textarea:focus {
  border-color: rgba(102,126,234,0.6) !important;
  box-shadow: 0 0 0 3px rgba(102,126,234,0.1) !important;
}

/* Streamlit button */
div.stButton > button {
  width: 100%;
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
  border: none;
  border-radius: 12px;
  padding: 0.8rem 1.5rem;
  font-size: 1rem;
  font-weight: 700;
  letter-spacing: 0.02em;
  transition: all 0.2s ease;
  box-shadow: 0 6px 20px rgba(102,126,234,0.35);
}
div.stButton > button:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 28px rgba(102,126,234,0.5);
}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  SESSION STATE
# ─────────────────────────────────────────────
if "history" not in st.session_state:
    st.session_state.history = []


# ─────────────────────────────────────────────
#  LOAD MODEL
# ─────────────────────────────────────────────
@st.cache_resource
def load_model():
    with open("model.pkl", "rb") as f:
        return pickle.load(f)

model = load_model()


# ─────────────────────────────────────────────
#  HELPER: Clean text
# ─────────────────────────────────────────────
def clean_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"http\S+|www\S+", " ", text)       # remove URLs
    text = re.sub(r"[^a-z\s]", " ", text)             # keep letters only
    text = re.sub(r"\s+", " ", text).strip()
    return text


# ─────────────────────────────────────────────
#  HERO HEADER
# ─────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <div class="hero-icon">🛡️</div>
  <h1 class="hero-title">Spam Email Detector</h1>
  <p class="hero-sub">Paste any email and our ML model will tell you if it's spam</p>
  <div class="hero-badges">
    <span class="badge">🤖 Naive Bayes</span>
    <span class="badge">📊 TF-IDF Features</span>
    <span class="badge">☁️ Deployed on Render</span>
    <span class="badge">🔄 CI/CD via GitHub</span>
  </div>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  INPUT CARD
# ─────────────────────────────────────────────
st.markdown('<div class="card"><p class="card-title">📧 Enter Email Content</p>', unsafe_allow_html=True)

email_input = st.text_area(
    label="",
    placeholder='Paste the email text here...\n\nExample: "Congratulations! You\'ve won a $1000 gift card. Click here to claim now!"',
    height=180,
    key="email_input",
    label_visibility="collapsed",
)

col1, col2 = st.columns([3, 1])
with col1:
    detect_btn = st.button("🔍  Detect Spam", key="detect")
with col2:
    clear_btn = st.button("🗑️  Clear", key="clear")

st.markdown('</div>', unsafe_allow_html=True)

if clear_btn:
    st.session_state.email_input = ""
    st.rerun()


# ─────────────────────────────────────────────
#  PREDICTION
# ─────────────────────────────────────────────
if detect_btn:
    if not email_input.strip():
        st.warning("⚠️ Please paste some email text first.")
    else:
        with st.spinner("Analyzing email..."):
            time.sleep(0.6)  # slight delay for UX

        cleaned  = clean_text(email_input)
        proba    = model.predict_proba([cleaned])[0]
        pred     = int(model.predict([cleaned])[0])
        spam_conf = proba[1]
        ham_conf  = proba[0]

        is_spam = pred == 1
        label   = "SPAM" if is_spam else "NOT SPAM"
        icon    = "🚨" if is_spam else "✅"
        desc    = "This email shows strong signs of spam. Be cautious!" \
                  if is_spam else \
                  "This email looks legitimate. No spam detected."
        card_cls   = "result-spam" if is_spam else "result-ham"
        label_cls  = "label-spam" if is_spam else "label-ham"
        bar_cls    = "bar-fill-spam" if is_spam else "bar-fill-ham"
        conf_pct   = int((spam_conf if is_spam else ham_conf) * 100)

        # Result card
        st.markdown(f"""
        <div class="{card_cls}">
          <div class="result-icon">{icon}</div>
          <p class="result-label {label_cls}">{label}</p>
          <p class="result-desc">{desc}</p>
          <div class="conf-wrap">
            <div class="conf-row">
              <span>Confidence</span>
              <span class="conf-val">{conf_pct}%</span>
            </div>
            <div class="bar-bg">
              <div class="{bar_cls}" style="width:{conf_pct}%"></div>
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        # Probability breakdown
        st.markdown('<div class="card"><p class="card-title">📊 Probability Breakdown</p>', unsafe_allow_html=True)
        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown(f"""
            <div style="text-align:center; padding:1rem; background:rgba(16,185,129,0.08);
                        border:1px solid rgba(16,185,129,0.3); border-radius:12px;">
              <p style="color:#64748b; font-size:0.72rem; margin:0; text-transform:uppercase; letter-spacing:0.1em;">✅ Ham (Legit)</p>
              <p style="color:#34d399; font-size:2rem; font-weight:800; margin:0.2rem 0;">
                {int(ham_conf*100)}%
              </p>
            </div>
            """, unsafe_allow_html=True)
        with col_b:
            st.markdown(f"""
            <div style="text-align:center; padding:1rem; background:rgba(239,68,68,0.08);
                        border:1px solid rgba(239,68,68,0.3); border-radius:12px;">
              <p style="color:#64748b; font-size:0.72rem; margin:0; text-transform:uppercase; letter-spacing:0.1em;">🚨 Spam</p>
              <p style="color:#f87171; font-size:2rem; font-weight:800; margin:0.2rem 0;">
                {int(spam_conf*100)}%
              </p>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # Save to history
        preview = email_input[:55] + "..." if len(email_input) > 55 else email_input
        st.session_state.history.insert(0, {
            "time":  datetime.now().strftime("%H:%M:%S"),
            "label": label,
            "conf":  f"{conf_pct}%",
            "preview": preview,
            "is_spam": is_spam,
        })
        st.session_state.history = st.session_state.history[:8]


# ─────────────────────────────────────────────
#  SPAM TIPS
# ─────────────────────────────────────────────
st.markdown('<div class="card"><p class="card-title">💡 Common Spam Signals</p>', unsafe_allow_html=True)
tips = [
    ("🎁", "Promises of prizes, gifts or lottery winnings you didn't enter"),
    ("💰", "Urgency around money — 'claim now', 'limited time', 'act fast'"),
    ("🔗", "Suspicious links or requests to verify account credentials"),
    ("📢", "ALL CAPS words, excessive exclamation marks!!!"),
    ("🏦", "Requests for personal or banking information"),
    ("💊", "Unsolicited offers for products, meds or services"),
]
for icon, tip in tips:
    st.markdown(f'<div class="tip-item"><span class="tip-icon">{icon}</span><span>{tip}</span></div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  HISTORY
# ─────────────────────────────────────────────
if st.session_state.history:
    st.markdown('<div class="card"><p class="card-title">🕒 Detection History</p>', unsafe_allow_html=True)
    for h in st.session_state.history:
        pill_cls = "pill-spam" if h["is_spam"] else "pill-ham"
        st.markdown(f"""
        <div class="hist-row">
          <span style="color:#475569; font-size:0.75rem; white-space:nowrap;">{h['time']}</span>
          <span class="{pill_cls}">{h['label']}</span>
          <span style="color:#64748b; flex:1; overflow:hidden; text-overflow:ellipsis; white-space:nowrap;">{h['preview']}</span>
          <span style="color:#475569; white-space:nowrap;">{h['conf']}</span>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    if st.button("🗑️  Clear History"):
        st.session_state.history = []
        st.rerun()


# ─────────────────────────────────────────────
#  FOOTER
# ─────────────────────────────────────────────
st.markdown("""
<div style="text-align:center; padding:2rem 0 0.5rem; color:#1e293b; font-size:0.72rem; letter-spacing:0.05em;">
  Spam Email Detector · Naive Bayes + TF-IDF · Deployed via GitHub + Render CI/CD
</div>
""", unsafe_allow_html=True)
