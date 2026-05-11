import streamlit as st
import streamlit.components.v1 as components
import json
import math
import random
from datetime import datetime
from pathlib import Path

# ── Setup ────────────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="My Anxiety Toolkit",
    page_icon="🌿",
    layout="centered",
    initial_sidebar_state="collapsed",
)

DATA_DIR = Path.home() / ".anxiety_toolkit"
DATA_DIR.mkdir(exist_ok=True)
DATA_FILE = DATA_DIR / "data.json"


def load_data():
    if DATA_FILE.exists():
        try:
            return json.loads(DATA_FILE.read_text(encoding="utf-8"))
        except Exception:
            return {}
    return {}


def save_data(d):
    DATA_FILE.write_text(json.dumps(d, indent=2, ensure_ascii=False), encoding="utf-8")


if "data" not in st.session_state:
    st.session_state.data = load_data()

data = st.session_state.data
data.setdefault("worry_list", [])
data.setdefault("morning_people", ["", "", ""])
data.setdefault("worry_time_slot", "")
data.setdefault("worry_time_place", "")
data.setdefault("evening_gratitude", [])
data.setdefault("energy_audit", [])
data.setdefault("reality_log", [])
data.setdefault("point_of_no_return", "")


# ── Theme / CSS ──────────────────────────────────────────────────────────────

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;1,400&family=Inter:wght@300;400;500&display=swap');

    .stApp {
        background: #0d0e10;
        color: #d8d6d0;
        font-family: 'Inter', system-ui, sans-serif;
    }
    .main .block-container {
        max-width: 880px;
        padding-top: 2rem;
    }

    /* Header */
    .toolkit-title {
        font-family: 'Playfair Display', serif;
        font-size: 2.6rem;
        text-align: center;
        color: #e8e6df;
        font-weight: 600;
        margin-bottom: 0.3rem;
    }
    .toolkit-title .accent {
        font-style: italic;
        background: linear-gradient(90deg, #d4a85a, #b88a3e);
        -webkit-background-clip: text;
        background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .toolkit-sub {
        text-align: center;
        color: #8a8780;
        font-style: italic;
        font-family: 'Playfair Display', serif;
        margin-bottom: 2rem;
    }

    /* Section headings (used sparingly) */
    .section-title {
        font-family: 'Playfair Display', serif;
        color: #c9c5bb;
        font-size: 1.2rem;
        margin: 2rem 0 0.8rem 0;
        font-style: italic;
    }
    .section-prompt {
        font-family: 'Playfair Display', serif;
        color: #d4a85a;
        font-size: 1.4rem;
        text-align: center;
        font-style: italic;
        margin: 2.5rem 0 1.2rem 0;
    }

    /* Cards */
    .card {
        background: #16181c;
        border: 1px solid #24262b;
        border-radius: 14px;
        padding: 1.6rem 1.8rem;
        margin: 1rem 0;
    }
    .card-header {
        display: flex;
        align-items: center;
        gap: 0.9rem;
        margin-bottom: 0.8rem;
    }
    .card-icon {
        width: 42px; height: 42px;
        background: #1f2228;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.3rem;
    }
    .card-title {
        font-family: 'Playfair Display', serif;
        font-size: 1.4rem;
        color: #e8e6df;
        margin: 0;
        line-height: 1.2;
    }
    .card-subtitle {
        font-size: 0.7rem;
        color: #6f6c66;
        letter-spacing: 0.15em;
        text-transform: uppercase;
        margin-top: 2px;
    }
    .card-body {
        color: #b8b6b0;
        font-size: 0.95rem;
        line-height: 1.65;
    }
    .card-body em { color: #d4a85a; font-style: italic; }
    .card-body strong { color: #e8e6df; font-weight: 500; }

    .aside {
        border-left: 2px solid #5dd6c0;
        padding: 0.6rem 1rem;
        color: #9c998f;
        font-style: italic;
        margin: 1rem 0;
        font-family: 'Playfair Display', serif;
    }

    .use-when {
        background: rgba(93, 214, 192, 0.08);
        border-left: 2px solid #5dd6c0;
        padding: 0.7rem 1rem;
        border-radius: 4px;
        color: #b6cdc7;
        font-size: 0.92rem;
        margin: 0.8rem 0 1rem 0;
    }

    /* Inputs */
    .stTextInput input, .stTextArea textarea, .stSelectbox > div > div {
        background: #1a1d22 !important;
        color: #d8d6d0 !important;
        border: 1px solid #2a2c30 !important;
        border-radius: 6px !important;
    }
    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: #5dd6c0 !important;
    }

    /* Default buttons */
    .stButton > button {
        background: transparent;
        color: #d8d6d0;
        border: 1px solid #3a3d44;
        border-radius: 8px;
        font-family: 'Playfair Display', serif;
        padding: 0.5rem 1.2rem;
        transition: all 0.15s ease;
    }
    .stButton > button:hover {
        border-color: #5dd6c0;
        color: #5dd6c0;
        background: rgba(93, 214, 192, 0.04);
    }

    /* Mood cards: large, two-line, full-width buttons styled as cards */
    .mood-grid-wrap .stButton > button {
        background: #16181c;
        border: 1px solid #24262b;
        border-radius: 12px;
        padding: 1.3rem 1.2rem;
        font-family: 'Playfair Display', serif;
        font-size: 1.05rem;
        color: #e8e6df;
        text-align: left;
        line-height: 1.4;
        height: auto;
        min-height: 90px;
        white-space: pre-wrap;
        width: 100%;
        transition: all 0.2s ease;
    }
    .mood-grid-wrap .stButton > button:hover {
        border-color: #d4a85a;
        background: #1a1d22;
        color: #e8e6df;
        transform: translateY(-1px);
    }

    /* Primary "settle me" CTA — compact bar */
    .calm-cta-wrap .stButton > button {
        background: linear-gradient(90deg, rgba(212, 168, 90, 0.15), rgba(184, 138, 62, 0.08));
        border: 1px solid rgba(212, 168, 90, 0.4);
        color: #d4a85a;
        font-family: 'Playfair Display', serif;
        font-size: 1.05rem;
        padding: 0.9rem 1.5rem;
        border-radius: 10px;
        width: 100%;
        font-style: italic;
    }
    .calm-cta-wrap .stButton > button:hover {
        background: rgba(212, 168, 90, 0.18);
        border-color: #d4a85a;
        color: #f0d896;
    }

    /* Secondary "spin the wheel" CTA — same shape, teal accent */
    .wheel-cta-wrap {
        margin-top: 0.6rem;
    }
    .wheel-cta-wrap .stButton > button {
        background: linear-gradient(90deg, rgba(93, 214, 192, 0.10), rgba(93, 214, 192, 0.04));
        border: 1px solid rgba(93, 214, 192, 0.35);
        color: #5dd6c0;
        font-family: 'Playfair Display', serif;
        font-size: 1.05rem;
        padding: 0.9rem 1.5rem;
        border-radius: 10px;
        width: 100%;
        font-style: italic;
    }
    .wheel-cta-wrap .stButton > button:hover {
        background: rgba(93, 214, 192, 0.14);
        border-color: #5dd6c0;
        color: #8ee7d2;
    }

    /* Active mood banner */
    .active-mood-banner {
        background: rgba(212, 168, 90, 0.06);
        border-left: 3px solid #d4a85a;
        border-radius: 4px;
        padding: 0.6rem 1rem;
        margin: 0.5rem 0 1rem 0;
        font-family: 'Playfair Display', serif;
        color: #d4a85a;
        font-style: italic;
        font-size: 0.95rem;
    }

    /* Step number circle */
    .step {
        display: inline-block;
        width: 1.6rem; height: 1.6rem;
        background: rgba(212, 168, 90, 0.15);
        color: #d4a85a;
        border-radius: 50%;
        text-align: center;
        line-height: 1.6rem;
        font-weight: 500;
        margin-right: 0.6rem;
        font-size: 0.85rem;
        font-family: 'Playfair Display', serif;
    }

    /* Hide streamlit chrome */
    #MainMenu, footer, header { visibility: hidden; }

    /* Expanders */
    div[data-testid="stExpander"] {
        background: #131418;
        border: 1px solid #24262b !important;
        border-radius: 10px !important;
        margin: 0.5rem 0;
    }
    .streamlit-expanderHeader, [data-testid="stExpander"] summary {
        font-family: 'Playfair Display', serif !important;
        color: #c9c5bb !important;
        font-size: 1rem !important;
    }

    /* Daily timeline */
    .timeline-item {
        border-left: 1px solid #2a2c30;
        padding: 0.5rem 0 1.5rem 1.5rem;
        margin-left: 0.5rem;
        position: relative;
    }
    .timeline-item::before {
        content: "";
        width: 10px; height: 10px;
        background: #d4a85a;
        border-radius: 50%;
        position: absolute;
        left: -5.5px;
        top: 0.6rem;
    }
    .timeline-time {
        color: #d4a85a;
        font-family: 'Playfair Display', serif;
        font-size: 0.85rem;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        margin-bottom: 0.5rem;
    }

    /* Footer */
    .footer-text {
        text-align: center;
        color: #6f6c66;
        margin-top: 3rem;
        padding-top: 1.5rem;
        border-top: 1px solid #2a2c30;
        font-family: 'Playfair Display', serif;
        font-style: italic;
    }

    /* Helper: secondary tool switcher row */
    .switcher-label {
        color: #6f6c66;
        font-size: 0.75rem;
        letter-spacing: 0.18em;
        text-transform: uppercase;
        margin: 1.5rem 0 0.5rem 0;
        font-family: 'Inter', sans-serif;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ── Header ───────────────────────────────────────────────────────────────────

st.markdown(
    '<div class="toolkit-title">My <span class="accent">Anxiety</span> Toolkit</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="toolkit-sub">Reach for this whenever anxiety arrives. These tools are yours.</div>',
    unsafe_allow_html=True,
)


# ── Helpers ──────────────────────────────────────────────────────────────────

def card_header(icon: str, title: str, subtitle: str):
    st.markdown(
        f"""
        <div class="card-header">
            <div class="card-icon">{icon}</div>
            <div>
                <div class="card-title">{title}</div>
                <div class="card-subtitle">{subtitle}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def use_when(text: str):
    st.markdown(f'<div class="use-when"><strong>Use when:</strong> {text}</div>', unsafe_allow_html=True)


def aside(text: str):
    st.markdown(f'<div class="aside">{text}</div>', unsafe_allow_html=True)


def section(title: str):
    st.markdown(f'<div class="section-title">{title}</div>', unsafe_allow_html=True)


# ── HTML components ──────────────────────────────────────────────────────────

BREATH_HTML = """
<div style="
    background: #16181c;
    border: 1px solid #24262b;
    border-radius: 14px;
    padding: 2rem;
    text-align: center;
    font-family: 'Playfair Display', Georgia, serif;
    color: #d8d6d0;
">
  <div id="circle" style="
      width: 180px; height: 180px;
      border: 2px solid #5dd6c0;
      border-radius: 50%;
      margin: 0 auto 1.5rem;
      display: flex; align-items: center; justify-content: center;
      transition: transform 4s ease-in-out;
  ">
    <div style="font-size: 1.4rem;">🌿</div>
  </div>
  <div id="phase" style="font-size: 1.5rem; font-style: italic; color: #5dd6c0; margin-bottom: 0.4rem;">Press start</div>
  <div id="patternName" style="color: #8a8780; margin-bottom: 1.2rem; font-family: Inter, sans-serif; font-size: 0.9rem;">Box breathing • 4-4-4-4</div>
  <div>
    <button id="startBtn" onclick="toggle()" style="
        padding: 0.5rem 1.5rem; margin: 0 0.4rem;
        background: transparent; border: 1px solid #5dd6c0;
        color: #5dd6c0; border-radius: 6px; cursor: pointer;
        font-family: inherit; font-size: 1rem;
    ">Start</button>
    <button onclick="cycle()" style="
        padding: 0.5rem 1.5rem; margin: 0 0.4rem;
        background: transparent; border: 1px solid #3a3d44;
        color: #aaa; border-radius: 6px; cursor: pointer;
        font-family: inherit; font-size: 1rem;
    ">Change pattern</button>
  </div>
  <div id="rhythm" style="color: #6f6c66; margin-top: 1rem; font-size: 0.85rem; font-family: Inter, sans-serif;">Box: 4s in · 4s hold · 4s out · 4s hold</div>
</div>
<script>
const patterns=[{name:'Box breathing • 4-4-4-4',desc:'Box: 4s in · 4s hold · 4s out · 4s hold',seq:[{phase:'Inhale',dur:4,scale:1.4},{phase:'Hold',dur:4,scale:1.4},{phase:'Exhale',dur:4,scale:1.0},{phase:'Hold',dur:4,scale:1.0}]},{name:'4-7-8 calming breath',desc:'4s in · 7s hold · 8s out',seq:[{phase:'Inhale',dur:4,scale:1.4},{phase:'Hold',dur:7,scale:1.4},{phase:'Exhale',dur:8,scale:1.0}]},{name:'Coherent breath • 5-5',desc:'5s in · 5s out (steady)',seq:[{phase:'Inhale',dur:5,scale:1.4},{phase:'Exhale',dur:5,scale:1.0}]}];
let p=0,idx=0,running=false,timer=null;
function step(){const s=patterns[p].seq[idx];document.getElementById('phase').textContent=s.phase;const c=document.getElementById('circle');c.style.transition=`transform ${s.dur}s ease-in-out`;c.style.transform=`scale(${s.scale})`;timer=setTimeout(()=>{idx=(idx+1)%patterns[p].seq.length;if(running)step();},s.dur*1000);}
function toggle(){const btn=document.getElementById('startBtn');if(running){running=false;clearTimeout(timer);btn.textContent='Start';document.getElementById('phase').textContent='Paused';}else{running=true;btn.textContent='Stop';idx=0;step();}}
function cycle(){p=(p+1)%patterns.length;document.getElementById('patternName').textContent=patterns[p].name;document.getElementById('rhythm').textContent=patterns[p].desc;if(running){clearTimeout(timer);idx=0;step();}}
</script>
"""

GROUNDING_SENSES = [
    ("5", "👁", "See", "Find five things you can see. Look at each one — colour, shape, light."),
    ("4", "✋", "Touch", "Find four things you can touch. Notice the temperature, texture, weight."),
    ("3", "👂", "Hear", "Find three sounds. Some near, some far. Don't label them — just listen."),
    ("2", "👃", "Smell", "Find two scents. Or breathe in deeply through your nose and notice the air."),
    ("1", "👅", "Taste", "Find one taste. Sip something, or just notice what's in your mouth right now."),
]
GROUNDING_HTML = """<div style="background:#16181c;border:1px solid #24262b;border-radius:14px;padding:1.8rem;font-family:'Inter',sans-serif;color:#d8d6d0;"><p style="color:#b8b6b0;line-height:1.6;margin-bottom:1.5rem;">Anxiety lives in the past or future. Your senses only exist <em style="color:#d4a85a;">right now</em>. Tap each card to pull yourself into the present moment.</p><div style="display:grid;grid-template-columns:1fr 1fr;gap:0.8rem;">"""
for num, icon, label, hint in GROUNDING_SENSES:
    GROUNDING_HTML += f'<div class="sense-card" onclick="toggleDone(this)" style="background:#1a1d22;border:1px solid #2a2c30;padding:1rem 1.2rem;border-radius:10px;cursor:pointer;transition:all 0.2s;"><div style="display:flex;align-items:baseline;gap:0.6rem;"><span class="num" style="font-size:1.6rem;font-family:\'Playfair Display\',serif;color:#d4a85a;font-style:italic;">{num}</span><span class="label" style="color:#c9c5bb;">{icon} {label}</span></div><div class="hint" style="display:none;color:#8a8780;font-size:0.85rem;margin-top:0.6rem;line-height:1.5;">{hint}</div></div>'
GROUNDING_HTML += """</div><button onclick="resetAll()" style="margin-top:1.5rem;padding:0.4rem 1.2rem;background:transparent;border:1px solid #3a3d44;color:#aaa;border-radius:6px;cursor:pointer;font-family:'Playfair Display',serif;">Reset</button></div><script>function toggleDone(el){if(el.classList.contains('done')){el.classList.remove('done');el.style.background='#1a1d22';el.style.borderColor='#2a2c30';el.style.opacity='1';el.querySelector('.hint').style.display='none';}else{el.classList.add('done');el.style.background='rgba(93,214,192,0.08)';el.style.borderColor='#5dd6c0';el.style.opacity='0.6';el.querySelector('.hint').style.display='block';}}function resetAll(){document.querySelectorAll('.sense-card').forEach(el=>{el.classList.remove('done');el.style.background='#1a1d22';el.style.borderColor='#2a2c30';el.style.opacity='1';el.querySelector('.hint').style.display='none';});}</script>"""

THANKYOU_HTML = """<div style="background:#16181c;border:1px solid #24262b;border-radius:14px;padding:2rem;text-align:center;font-family:'Playfair Display',serif;color:#d8d6d0;"><div id="ty-line" style="font-size:1.3rem;font-style:italic;color:#d4a85a;min-height:5rem;line-height:1.6;padding:1rem;">Press start when you're ready.</div><button id="tyBtn" onclick="tyStart()" style="padding:0.5rem 1.5rem;background:transparent;border:1px solid #d4a85a;color:#d4a85a;border-radius:6px;cursor:pointer;font-family:inherit;font-size:1rem;">Start guided</button></div><script>const tyLines=["Smile gently. Just a small one.","Take one slow breath in.","Thank you for this feeling.","I appreciate this shift in energy.","I love you.","I've missed you.","Now keep going with your day."];let tyIdx=0,tyRunning=false;function tyStart(){if(tyRunning)return;tyRunning=true;tyIdx=0;document.getElementById('tyBtn').textContent='Running...';showNext();}function showNext(){if(tyIdx>=tyLines.length){document.getElementById('ty-line').textContent="Done. You can repeat anytime.";document.getElementById('tyBtn').textContent='Start guided';tyRunning=false;return;}document.getElementById('ty-line').textContent=tyLines[tyIdx];tyIdx++;setTimeout(showNext,3500);}</script>"""


# ── Tool render functions ───────────────────────────────────────────────────

def render_breathe(kp="breathe"):
    components.html(BREATH_HTML, height=480)


def render_grounding(kp="ground"):
    components.html(GROUNDING_HTML, height=600)


def render_tool_1(kp="t1"):
    st.markdown('<div class="card">', unsafe_allow_html=True)
    card_header("🪞", "The Witness Practice", "Tool 1 · Observe instead of becoming")
    use_when("an emotion is taking you over and you feel fused with it.")
    st.markdown(
        """
        <div class="card-body">
        <p><span class="step">1</span><strong>Name it specifically.</strong> Not "I feel bad" — say
        "I'm noticing <em>disappointment</em>." Specific names reduce amygdala activity.</p>
        <p><span class="step">2</span><strong>Create distance with language.</strong> Don't say
        <em>"I am angry."</em> Say: <em>"I notice anger arising in me right now."</em></p>
        <p><span class="step">3</span><strong>Find it in your body.</strong> Chest tight? Stomach knot?
        Heat in face? Put your attention there for 30 seconds.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    emo = st.text_input("Right now, I'm noticing...", key=f"{kp}_emo", placeholder="e.g., a wave of anxiety")
    body = st.text_input("I feel it in my body here:", key=f"{kp}_body", placeholder="e.g., tightness in my chest")
    if emo and body:
        aside(f"Stay with this for 30 seconds: <em>I notice {emo}, and I feel it as {body}.</em> Let it pass through you.")
    st.markdown('</div>', unsafe_allow_html=True)


def render_tool_2(kp="t2"):
    st.markdown('<div class="card">', unsafe_allow_html=True)
    card_header("🍃", "Thought Diffusion", "Tool 2 · For intrusive / repetitive thoughts")
    use_when("the same thought keeps circling — replaying a conversation, fixating on a worry.")
    st.markdown(
        """
        <div class="card-body">
        <p><span class="step">1</span>Notice you're stuck in a repetitive thought.</p>
        <p><span class="step">2</span>Say: <em>"I am noticing that I'm having the thought that ____."</em></p>
        <p><span class="step">3</span>Visualize the thought as <strong>text scrolling on a screen</strong>,
        or words on a leaf floating downstream.</p>
        <p><span class="step">4</span>Watch it pass without arguing or trying to solve it.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    t = st.text_input("The thought I'm stuck on:", key=f"{kp}_thought", placeholder="e.g., they hate me now")
    if t:
        aside(f"I am noticing that I'm having the thought that <em>{t}</em>. "
              "Now picture those words on a leaf, floating downstream. Watch them go.")
    aside("What you resist persists. Watching weakens grip without a fight.")
    st.markdown('</div>', unsafe_allow_html=True)


def render_tool_3(kp="t3"):
    st.markdown('<div class="card">', unsafe_allow_html=True)
    card_header("⚡", "Pattern Interrupt + Pivot (4 R's)", "Tool 3 · Break a deep spiral now")
    use_when("you're already deep in a spiral and need to break it NOW.")
    st.markdown(
        """
        <div class="card-body">
        <p><span class="step">1</span><strong>RELABEL</strong> — Say out loud: <em>"This is rumination."</em></p>
        <p><span class="step">2</span><strong>REATTRIBUTE</strong> — <em>"This is my brain getting stuck.
        It is not an accurate reflection of reality."</em></p>
        <p><span class="step">3</span><strong>REFOCUS</strong> — Do something that demands full attention:</p>
        <ul style="color: #b8b6b0; margin-left: 2.5rem;">
            <li>Count backward from 100 by 7s</li>
            <li>Name everything blue in the room</li>
            <li>20 pushups, or walk around the block</li>
            <li>Cold water on face/wrists</li>
        </ul>
        <p><span class="step">4</span><strong>REVALUE</strong> — <em>"That thought pattern wasn't helpful or necessary."</em></p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    aside("The Anxiety Loop: thought → emotion → behavior. Intervene in the pause between thought and emotion.")
    st.markdown('</div>', unsafe_allow_html=True)


def render_tool_4(kp="t4"):
    st.markdown('<div class="card">', unsafe_allow_html=True)
    card_header("🙏", "The 'Thank You' Technique", "Tool 4 · The author's go-to")
    use_when("anxiety shows up out of nowhere, OR when logic isn't working.")
    st.markdown(
        """
        <div class="card-body">
        <p>What you resist persists. Fighting anxiety strengthens it. Gratitude activates entirely
        different neural circuits than fear.</p>
        <p style="margin-top: 1rem;">When anxiety arises, smile (or smirk — whatever feels real).
        Say out loud or in your head:</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown('</div>', unsafe_allow_html=True)
    components.html(THANKYOU_HTML, height=260)
    aside("Genuinely try to feel grateful, like greeting an old friend.")


def render_tool_5(kp="t5"):
    st.markdown('<div class="card">', unsafe_allow_html=True)
    card_header("📋", "Worry Time", "Tool 5 · Capture worries, address them later")
    use_when("worries keep popping up all day and hijacking everything you try to do.")

    c1, c2 = st.columns(2)
    with c1:
        slot = st.text_input("My worry time (15-20 min, NOT before bed):",
                             value=data["worry_time_slot"], key=f"{kp}_slot",
                             placeholder="e.g., Daily, 6:30 PM")
        if slot != data["worry_time_slot"]:
            data["worry_time_slot"] = slot
            save_data(data)
    with c2:
        place = st.text_input("Where I'll do it:",
                              value=data["worry_time_place"], key=f"{kp}_place",
                              placeholder="e.g., kitchen table")
        if place != data["worry_time_place"]:
            data["worry_time_place"] = place
            save_data(data)

    st.markdown(
        "<div class='card-body' style='margin-top: 0.8rem;'>When a worry pops up: acknowledge it "
        "(<em>'I see you. I'll address you at worry time.'</em>) then drop it here.</div>",
        unsafe_allow_html=True,
    )

    new_worry = st.text_area("New worry:", height=80, key=f"{kp}_new_worry", label_visibility="collapsed",
                             placeholder="Write the worry here...")
    if st.button("Capture worry", key=f"{kp}_add_worry"):
        if new_worry.strip():
            data["worry_list"].append({
                "text": new_worry.strip(),
                "captured": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "addressed": False,
            })
            save_data(data)
            st.rerun()

    active = [w for w in data["worry_list"] if not w.get("addressed")]
    if active:
        st.markdown('<div class="section-title">Active worries</div>', unsafe_allow_html=True)
        for i, w in enumerate(data["worry_list"]):
            if w.get("addressed"):
                continue
            with st.container(border=True):
                st.markdown(f"**{w['text']}**")
                st.caption(f"Captured: {w['captured']}")
                st.markdown(
                    "*During worry time:*\n"
                    "- Action I can take NOW? If yes — smallest first step?\n"
                    "- If no — can I accept this uncertainty for now?"
                )
                cc1, cc2 = st.columns(2)
                if cc1.button("✓ Addressed", key=f"{kp}_done_{i}"):
                    data["worry_list"][i]["addressed"] = True
                    save_data(data)
                    st.rerun()
                if cc2.button("Delete", key=f"{kp}_del_{i}"):
                    data["worry_list"].pop(i)
                    save_data(data)
                    st.rerun()
    else:
        st.markdown('<div class="aside">No active worries. The list is clear.</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


def render_tool_6(kp="t6"):
    st.markdown('<div class="card">', unsafe_allow_html=True)
    card_header("🎯", "Control Inventory", "Tool 6 · Reclaim what you can actually influence")
    use_when("you're stressed about a specific situation and feel out of control.")
    st.markdown(
        "<div class='card-body'>Fill in what's stressing you on the left, and ONE thing you "
        "<em>can</em> influence on the right.</div>",
        unsafe_allow_html=True,
    )
    rows_key = f"{kp}_rows"
    if rows_key not in st.session_state:
        st.session_state[rows_key] = 4
    for i in range(st.session_state[rows_key]):
        c1, c2 = st.columns(2)
        with c1:
            st.text_input("Stressor", key=f"{kp}_stress_{i}", label_visibility="collapsed",
                          placeholder=f"What's stressing me #{i+1}")
        with c2:
            st.text_input("Control", key=f"{kp}_ctrl_{i}", label_visibility="collapsed",
                          placeholder=f"One thing I can influence #{i+1}")
    if st.button("+ Add row", key=f"{kp}_add_ctrl_row"):
        st.session_state[rows_key] += 1
        st.rerun()
    aside("You can't control: traffic, others' behavior, outcomes. "
          "You CAN control: your response, how you talk to yourself, the next hour, your boundaries.")
    st.markdown('</div>', unsafe_allow_html=True)


def render_tool_7(kp="t7"):
    st.markdown('<div class="card">', unsafe_allow_html=True)
    card_header("📵", "Emotional Circuit Breaker", "Tool 7 · After rejection or being ignored")
    use_when("someone didn't respond, ignored you, or said something that stung.")
    st.markdown(
        """
        <div class="card-body">
        <p><span class="step">1</span>Take a deep breath. Acknowledge:
        <em>"I'm feeling threatened right now, but I'm actually safe."</em></p>
        <p><span class="step">2</span>Use the 5-4-3-2-1 grounding below.</p>
        <p><span class="step">3</span>Ask: <em>"What do I truly need right now?"</em>
        before deciding how to respond.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    aside("Their behavior is a reflection of THEM — their experiences, their level. "
          "It literally has nothing to do with your worth.")
    st.markdown('</div>', unsafe_allow_html=True)
    render_grounding(kp=f"{kp}_ground")


def render_tool_8(kp="t8"):
    st.markdown('<div class="card">', unsafe_allow_html=True)
    card_header("🥊", "Redirection Protocol", "Tool 8 · When you want to 'win' or get revenge")
    use_when("you're fantasizing about them regretting losing you, or planning how to 'win.'")
    st.markdown(
        """
        <div class="card-body">
        <p><span class="step">1</span>Acknowledge without judgment:
        <em>"I want to win against them right now, that's okay."</em></p>
        <p><span class="step">2</span>Ask: <em>"What meaningful goal would give me a genuine
        sense of agency — that has nothing to do with them?"</em></p>
        <p><span class="step">3</span>Take ONE small action toward that goal in the next 10 min.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    goal = st.text_input("My goal that has NOTHING to do with them:", key=f"{kp}_goal",
                         placeholder="e.g., finish the gym session I planned")
    if goal:
        action = st.text_input("Smallest action I can take in the next 10 min:", key=f"{kp}_action",
                               placeholder="e.g., change into gym clothes now")
        if action:
            aside(f"Go do it: <em>{action}</em>.")
    st.markdown('</div>', unsafe_allow_html=True)


def render_tool_9(kp="t9"):
    st.markdown('<div class="card">', unsafe_allow_html=True)
    card_header("🔍", "Energy Exchange Audit", "Tool 9 · Pinpoint who's draining you")
    use_when("you keep feeling drained but can't pinpoint why. Run this for one week.")
    with st.form(f"{kp}_form", clear_on_submit=True):
        c1, c2 = st.columns(2)
        with c1:
            person = st.text_input("Person")
            before = st.selectbox("Before", ["energized", "neutral", "drained"])
        with c2:
            after = st.selectbox("After", ["energized", "neutral", "drained"])
            absorbed = st.text_input("What I absorbed")
        if st.form_submit_button("Log entry"):
            if person:
                data["energy_audit"].append({
                    "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "person": person, "before": before, "after": after, "absorbed": absorbed,
                })
                save_data(data)
                st.success("Logged.")
    if data["energy_audit"]:
        st.dataframe(data["energy_audit"][-20:], use_container_width=True)
        if st.button("Clear log", key=f"{kp}_clear_audit"):
            data["energy_audit"] = []
            save_data(data)
            st.rerun()
    aside("End of week, ask: do I feel energized or drained after time with them? "
          "When I'm struggling, do they show up like I show up for them?")
    st.markdown('</div>', unsafe_allow_html=True)


def render_tool_10(kp="t10"):
    st.markdown('<div class="card">', unsafe_allow_html=True)
    card_header("🫶", "Compassionate Container", "Tool 10 · Care without absorbing")
    use_when("someone is offloading their problems and you feel yourself absorbing their emotions.")
    st.markdown(
        """
        <div class="card-body">
        <p><strong>During the conversation:</strong></p>
        <p>Visualize their emotions as <em>water</em>. Instead of absorbing it, picture a beautiful
        container holding the water — separate from you. You can see it, honor it, care about it.
        But it's not in your body.</p>
        <p style="margin-top: 1rem;"><strong>Phrases you can use out loud:</strong></p>
        <ul style="color: #b8b6b0; margin-left: 1.5rem;">
            <li><em>"I'm here to listen, but I may not have solutions."</em></li>
            <li><em>"I can hold space for you without taking this on as my responsibility."</em></li>
            <li><em>"I care about you while still maintaining my own balance."</em></li>
        </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown('</div>', unsafe_allow_html=True)


def render_tool_11(kp="t11"):
    st.markdown('<div class="card">', unsafe_allow_html=True)
    card_header("💛", "Guided Guilt Release", "Tool 11 · After setting a boundary")
    use_when("you said no, set a limit, didn't reply — and the guilt is eating you.")
    st.markdown(
        """
        <div class="card-body">
        <p><span class="step">1</span>Acknowledge: <em>"I notice I'm feeling guilty right now."</em></p>
        <p><span class="step">2</span>Remind yourself: <em>"This feeling is temporary.
        It's my brain adjusting to a new pattern — like withdrawal."</em></p>
        <p><span class="step">3</span>Slow breathing (4 in, 6 out) until intensity drops.</p>
        <p><span class="step">4</span>Affirm: <em>"Boundaries don't make me selfish.
        They make me sustainable."</em></p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown('</div>', unsafe_allow_html=True)


def render_tool_12(kp="t12"):
    st.markdown('<div class="card">', unsafe_allow_html=True)
    card_header("🤐", "Minimal Explanation Policy", "Tool 12 · Stop justifying yourself")
    use_when("you feel the compulsion to justify your decision, your boundary, your 'no.'")
    st.markdown(
        """
        <div class="card-body">
        <p><strong>Pick the right level — don't go higher:</strong></p>
        <ul style="color: #b8b6b0; margin-left: 1.5rem; line-height: 2;">
            <li><strong>Casual:</strong> <em>"This doesn't work for me."</em> (Complete sentence.)</li>
            <li><strong>Closer:</strong> <em>"I'm making changes to support my wellbeing."</em></li>
            <li><strong>Essential:</strong> <em>"I care about our connection and I need to make
            these changes. I'm happy to answer specific questions, but I won't defend my need for
            these boundaries."</em></li>
        </ul>
        <p style="margin-top: 1rem;">If they push back: don't expand. Repeat the same sentence.
        Silence is allowed.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown('</div>', unsafe_allow_html=True)


def render_tool_13(kp="t13"):
    st.markdown('<div class="card">', unsafe_allow_html=True)
    card_header("☀️", "Morning Anchor Ritual", "Tool 13 · Before you get out of bed")
    use_when("you wake up with that heavy chest, vague unease, or anticipatory dread.")
    st.markdown(
        """
        <div class="card-body">
        <p><span class="step">1</span>Place your hand over your heart.</p>
        <p><span class="step">2</span>Acknowledge the weight — don't fight it.</p>
        <p><span class="step">3</span>Whisper: <em>"Thank you, for another day of life."</em></p>
        <p><span class="step">4</span>Add: <em>"I am also in control of how I feel."</em></p>
        <p><span class="step">5</span>Visualize three specific people you love.
        Let gratitude fill your chest, breath by breath.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown('<div class="section-title" style="font-size: 1rem;">My three people</div>', unsafe_allow_html=True)
    cols = st.columns(3)
    changed = False
    for i, c in enumerate(cols):
        with c:
            v = st.text_input(f"Person {i+1}", value=data["morning_people"][i],
                              key=f"{kp}_mp_{i}", label_visibility="collapsed",
                              placeholder=f"Person {i+1}")
            if v != data["morning_people"][i]:
                data["morning_people"][i] = v
                changed = True
    if changed:
        save_data(data)
    if all(data["morning_people"]):
        names = ", ".join(p for p in data["morning_people"] if p)
        aside(f"Tomorrow morning, hand on heart, picture: <em>{names}</em>.")
    st.markdown('</div>', unsafe_allow_html=True)


def render_tool_14(kp="t14"):
    st.markdown('<div class="card">', unsafe_allow_html=True)
    card_header("🎭", "Reality Preservation", "Tool 14 · When someone makes you doubt yourself")
    use_when("you keep feeling confused after talking to someone, second-guessing your memory.")
    st.markdown(
        "<div class='card-body'>After a confusing interaction, log what actually happened "
        "while it's fresh. This is YOUR record — they don't see it.</div>",
        unsafe_allow_html=True,
    )
    with st.form(f"{kp}_form", clear_on_submit=True):
        person = st.text_input("Person", key=f"{kp}_rl_person")
        what_happened = st.text_area("What was actually said/done:", height=120, key=f"{kp}_rl_what")
        how_felt = st.text_area("How I felt:", height=80, key=f"{kp}_rl_felt")
        if st.form_submit_button("Log entry"):
            if what_happened.strip():
                data["reality_log"].append({
                    "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "person": person,
                    "what_happened": what_happened.strip(),
                    "how_felt": how_felt.strip(),
                })
                save_data(data)
                st.success("Logged. This is your record.")
    if data["reality_log"]:
        for entry in reversed(data["reality_log"]):
            felt = (f"<div style='color:#8a8780;margin-top:0.4rem;font-style:italic;'>Felt: {entry['how_felt']}</div>"
                    if entry.get('how_felt') else "")
            st.markdown(
                f"<div style='background:#1a1d22;padding:0.8rem 1rem;border-radius:6px;margin:0.4rem 0;'>"
                f"<div style='color:#d4a85a;font-size:0.85rem;'>{entry['date']} · {entry.get('person', '')}</div>"
                f"<div style='color:#b8b6b0;margin-top:0.4rem;'>{entry['what_happened']}</div>"
                f"{felt}</div>",
                unsafe_allow_html=True,
            )
    aside("Red flags: always confused after talking to them, always defending basic perceptions, "
          "your concerns always turned back on you.")
    st.markdown('</div>', unsafe_allow_html=True)


def render_tool_15(kp="t15"):
    st.markdown('<div class="card">', unsafe_allow_html=True)
    card_header("🚶", "Change Your Environment", "Tool 15 · When you feel stuck")
    use_when("you've been mentally pushing through for days/weeks and nothing is shifting.")
    st.markdown(
        """
        <div class="card-body">
        <p>Sometimes the block isn't mental — it's environmental.</p>
        <p style="margin-top: 0.8rem;">Pick the <strong>smallest</strong> option you can do today:</p>
        <ul style="color: #b8b6b0; margin-left: 1.5rem;">
            <li>10-minute walk in nature</li>
            <li>Work from a different room or café</li>
            <li>Drive somewhere new for an hour</li>
            <li>Weekend day-trip alone</li>
            <li>Rearrange your space</li>
        </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )
    aside("The author's example: weeks of meditation didn't break his loop. A 2-hour drive away from home did.")
    st.markdown('</div>', unsafe_allow_html=True)


def render_tool_16(kp="t16"):
    st.markdown('<div class="card">', unsafe_allow_html=True)
    card_header("🚪", "Point of No Return", "Tool 16 · When you keep going back")
    use_when("you've tried to leave a relationship/situation before but kept going back on 'one more chance.'")
    st.markdown(
        "<div class='card-body'>List every broken promise, repeated pattern, hopeful "
        "expectation that was disappointed. Be ruthlessly specific.</div>",
        unsafe_allow_html=True,
    )
    txt = st.text_area("List:", value=data["point_of_no_return"], height=240,
                       key=f"{kp}_pnr_text", label_visibility="collapsed",
                       placeholder="- Promised to stop, didn't\n- Said they'd come to therapy, never did\n...")
    if txt != data["point_of_no_return"]:
        data["point_of_no_return"] = txt
        save_data(data)
    aside("If this exact pattern continues unchanged for 5 more years, am I willing to live with it?")
    ans = st.radio("My answer:", ["— select —", "Yes, I can live with it", "No, I cannot"],
                   horizontal=True, key=f"{kp}_pnr_ans")
    if ans == "No, I cannot":
        st.error("Then that's your answer about whether to stay. Trust this clarity. You earned it by being honest.")
    elif ans == "Yes, I can live with it":
        st.info("Then stay — but stay consciously, with eyes open, knowing what you're choosing.")
    st.markdown('</div>', unsafe_allow_html=True)


# ── Tool dispatch + metadata ────────────────────────────────────────────────

TOOL_DISPATCH = {
    "Breathe": render_breathe, "Ground": render_grounding,
    "1": render_tool_1, "2": render_tool_2, "3": render_tool_3,
    "4": render_tool_4, "5": render_tool_5, "6": render_tool_6,
    "7": render_tool_7, "8": render_tool_8, "9": render_tool_9,
    "10": render_tool_10, "11": render_tool_11, "12": render_tool_12,
    "13": render_tool_13, "14": render_tool_14, "15": render_tool_15,
    "16": render_tool_16,
}

TOOL_TITLES = {
    "Breathe": "Box Breathing",
    "Ground": "5-4-3-2-1 Grounding",
    "1": "Witness Practice", "2": "Thought Diffusion", "3": "Pattern Interrupt",
    "4": "Thank You Technique", "5": "Worry Time", "6": "Control Inventory",
    "7": "Emotional Circuit Breaker", "8": "Redirection Protocol",
    "9": "Energy Exchange Audit", "10": "Compassionate Container",
    "11": "Guilt Release", "12": "Minimal Explanation",
    "13": "Morning Anchor Ritual", "14": "Reality Preservation",
    "15": "Change Your Environment", "16": "Point of No Return",
}


# ── Spinning wheel ──────────────────────────────────────────────────────────

# Tools eligible for the random wheel — curated for "any time" practice,
# excluding tools that only make sense in specific situations.
WHEEL_TOOLS = [
    {"id": "Breathe", "icon": "🌿"},
    {"id": "Ground",  "icon": "🌱"},
    {"id": "1",       "icon": "🪞"},
    {"id": "2",       "icon": "🍃"},
    {"id": "3",       "icon": "⚡"},
    {"id": "4",       "icon": "🙏"},
    {"id": "6",       "icon": "🎯"},
    {"id": "7",       "icon": "📵"},
    {"id": "10",      "icon": "🫶"},
    {"id": "13",      "icon": "☀️"},
]


def generate_wheel_html(target_idx, nonce):
    """Build the SVG wheel. If target_idx is None, render static (no spin).
    Otherwise, animate from 0 to land on segment at target_idx."""
    tools = WHEEL_TOOLS
    n = len(tools)
    seg = 360.0 / n
    cx, cy, r = 200, 200, 180

    segments = []
    for i, tool in enumerate(tools):
        a1 = i * seg
        a2 = (i + 1) * seg
        a1r = math.radians(a1)
        a2r = math.radians(a2)
        x1 = cx + r * math.sin(a1r)
        y1 = cy - r * math.cos(a1r)
        x2 = cx + r * math.sin(a2r)
        y2 = cy - r * math.cos(a2r)
        color = '#1a1d22' if i % 2 == 0 else '#22252b'
        if target_idx is not None and i == target_idx:
            color = 'rgba(212, 168, 90, 0.22)'
        path = f'M {cx} {cy} L {x1:.1f} {y1:.1f} A {r} {r} 0 0 1 {x2:.1f} {y2:.1f} Z'
        segments.append(
            f'<path d="{path}" fill="{color}" stroke="#0d0e10" stroke-width="1.5"/>'
        )
        # Emoji centered in segment
        mid_a = (a1 + a2) / 2.0
        mid_r = math.radians(mid_a)
        tr = 130
        tx = cx + tr * math.sin(mid_r)
        ty = cy - tr * math.cos(mid_r)
        segments.append(
            f'<text x="{tx:.1f}" y="{ty:.1f}" text-anchor="middle" '
            f'dominant-baseline="central" font-size="28" font-family="Georgia">'
            f'{tool["icon"]}</text>'
        )
    segments_html = "\n".join(segments)

    if target_idx is not None:
        target_mid = target_idx * seg + seg / 2.0
        final_rot = 5 * 360 + (360 - target_mid)
        animation_css = (
            "@keyframes wheelspin" + str(nonce) + " { "
            "from { transform: rotate(0deg); } "
            "to { transform: rotate(" + f"{final_rot:.2f}" + "deg); } "
            "} "
            "#wheel" + str(nonce) + " { "
            "transform-origin: 200px 200px; "
            "animation: wheelspin" + str(nonce) + " 4s cubic-bezier(0.17, 0.67, 0.32, 1) forwards; "
            "}"
        )
        chosen_title = TOOL_TITLES[tools[target_idx]["id"]]
        result_opacity = "0"
        reveal_delay_ms = 4000
    else:
        animation_css = ""
        chosen_title = 'Click "Spin" to pick a tool'
        result_opacity = "1"
        reveal_delay_ms = 0

    result_css = (
        ".wheel-result-" + str(nonce) + " { "
        "text-align: center; color: #d4a85a; "
        "font-family: 'Playfair Display', Georgia, serif; "
        "font-style: italic; font-size: 1.25rem; "
        "margin: 1.2rem 0 0.3rem 0; opacity: " + result_opacity + "; "
        "transition: opacity 0.6s ease-in; "
        "}"
    )

    html = (
        '<!-- spin ' + str(nonce) + ' -->'
        '<style>' + animation_css + ' ' + result_css + '</style>'
        '<svg viewBox="0 0 400 420" width="100%" '
        'style="max-width: 380px; display: block; margin: 0 auto;">'
        '<g id="wheel' + str(nonce) + '">' + segments_html + '</g>'
        '<circle cx="200" cy="200" r="22" fill="#0d0e10" '
        'stroke="#d4a85a" stroke-width="2"/>'
        '<text x="200" y="207" text-anchor="middle" font-size="18" '
        'fill="#d4a85a">✦</text>'
        '<polygon points="200,5 186,40 214,40" fill="#d4a85a"/>'
        '</svg>'
        '<div class="wheel-result-' + str(nonce) + '" id="result' + str(nonce) + '">'
        '✦ ' + chosen_title + ' ✦</div>'
        '<script>'
        '(function() { '
        'var el = document.getElementById("result' + str(nonce) + '"); '
        'if (el) setTimeout(function() { el.style.opacity = 1; }, '
        + str(reveal_delay_ms) + '); '
        '})();'
        '</script>'
    )
    return html


# ── Mood map ─────────────────────────────────────────────────────────────────
# 6 core moods (always visible). Each maps to 1-3 tools, primary first.

MOODS_PRIMARY = [
    {"id": "spiraling", "icon": "🌀", "label": "I'm spiraling",
     "subtitle": "Anxious thoughts won't stop", "tools": ["3", "2", "1"]},
    {"id": "overthinking", "icon": "💭", "label": "Overthinking",
     "subtitle": "Replaying conversations, second-guessing", "tools": ["2", "1", "4"]},
    {"id": "rejected", "icon": "💔", "label": "Hurt or rejected",
     "subtitle": "They didn't reply, ignored me, or said something that stung", "tools": ["7", "1"]},
    {"id": "drained", "icon": "🪫", "label": "Drained",
     "subtitle": "Carrying others' emotions, exhausted by people", "tools": ["10", "9"]},
    {"id": "morning", "icon": "🌅", "label": "Heavy on waking",
     "subtitle": "Anxiety before I even get out of bed", "tools": ["13"]},
    {"id": "vague", "icon": "😶‍🌫️", "label": "Anxiety from nowhere",
     "subtitle": "Just there, no clear cause, won't shift with logic", "tools": ["4", "Breathe"]},
]

MOODS_MORE = [
    {"id": "guilt", "icon": "😔", "label": "Guilt after saying no", "tools": ["11"]},
    {"id": "explain", "icon": "📣", "label": "Urge to over-explain myself", "tools": ["12"]},
    {"id": "control", "icon": "🎮", "label": "Need to control everything", "tools": ["6"]},
    {"id": "revenge", "icon": "🥊", "label": "Want to 'win' / get revenge", "tools": ["8"]},
    {"id": "worries", "icon": "📋", "label": "Worries piling up all day", "tools": ["5"]},
    {"id": "gaslit", "icon": "🎭", "label": "Doubting my own perception", "tools": ["14"]},
    {"id": "stuck", "icon": "🪨", "label": "Stuck — can't move forward", "tools": ["15"]},
    {"id": "leaving", "icon": "🚪", "label": "Considering leaving for real", "tools": ["16", "15"]},
]

ALL_MOODS = {m["id"]: m for m in MOODS_PRIMARY + MOODS_MORE}


# ──────────────────────────────────────────────────────────────────────────────
# MAIN LAYOUT — UX-first
# ──────────────────────────────────────────────────────────────────────────────

# Initialize session state
st.session_state.setdefault("active_mood", None)
st.session_state.setdefault("active_tool", None)
st.session_state.setdefault("breath_open", False)
st.session_state.setdefault("wheel_open", False)
st.session_state.setdefault("spin_idx", None)
st.session_state.setdefault("spin_nonce", 0)


# ── 1. PRIMARY ACTION: One-tap settle ────────────────────────────────────────
# Always visible at top. The universal first response.

st.markdown('<div class="calm-cta-wrap">', unsafe_allow_html=True)
breath_label = "✕  Close breathing" if st.session_state.breath_open else "🌿  Settle me — take a breath"
if st.button(breath_label, key="cta_breath", use_container_width=True):
    st.session_state.breath_open = not st.session_state.breath_open
    st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

if st.session_state.breath_open:
    render_breathe(kp="hero_breathe")
    st.markdown(
        '<div class="aside" style="text-align: center;">'
        "Try one full minute. If anxiety is high, switch to <em>4-7-8</em> — "
        "the long exhale is the calming part.</div>",
        unsafe_allow_html=True,
    )


# ── 1b. SECONDARY: Spin the wheel for a random tool ──────────────────────────

st.markdown('<div class="wheel-cta-wrap">', unsafe_allow_html=True)
wheel_label = ("✕  Close the wheel" if st.session_state.wheel_open
               else "🎲  Spin the wheel — pick a tool for me")
if st.button(wheel_label, key="cta_wheel", use_container_width=True):
    st.session_state.wheel_open = not st.session_state.wheel_open
    st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

if st.session_state.wheel_open:
    components.html(
        generate_wheel_html(
            target_idx=st.session_state.spin_idx,
            nonce=st.session_state.spin_nonce,
        ),
        height=520,
    )
    wcols = st.columns([1, 1])
    with wcols[0]:
        if st.button("🎲  Spin", key="do_spin", use_container_width=True):
            st.session_state.spin_idx = random.randint(0, len(WHEEL_TOOLS) - 1)
            st.session_state.spin_nonce += 1
            st.rerun()
    with wcols[1]:
        if st.session_state.spin_idx is not None:
            chosen = WHEEL_TOOLS[st.session_state.spin_idx]
            chosen_title = TOOL_TITLES[chosen["id"]]
            if st.button(f"Use {chosen_title} ↓", key="use_spin",
                         use_container_width=True):
                st.session_state.active_tool = chosen["id"]
                st.session_state.active_mood = None  # wheel-picked, no mood
                st.session_state.wheel_open = False
                st.rerun()


# ── 2. MOOD-BASED ROUTING ────────────────────────────────────────────────────

if st.session_state.active_tool is None:
    # Show mood grid
    st.markdown('<div class="section-prompt">What\'s happening right now?</div>', unsafe_allow_html=True)

    st.markdown('<div class="mood-grid-wrap">', unsafe_allow_html=True)
    for row_start in range(0, len(MOODS_PRIMARY), 2):
        cols = st.columns(2, gap="small")
        for offset in range(2):
            i = row_start + offset
            if i >= len(MOODS_PRIMARY):
                continue
            m = MOODS_PRIMARY[i]
            with cols[offset]:
                if st.button(
                    f"{m['icon']}  {m['label']}\n{m['subtitle']}",
                    key=f"mood_{m['id']}",
                    use_container_width=True,
                ):
                    st.session_state.active_mood = m["id"]
                    st.session_state.active_tool = m["tools"][0]
                    st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # More situations expander
    with st.expander("More situations…"):
        st.markdown('<div class="mood-grid-wrap">', unsafe_allow_html=True)
        for row_start in range(0, len(MOODS_MORE), 2):
            cols = st.columns(2, gap="small")
            for offset in range(2):
                i = row_start + offset
                if i >= len(MOODS_MORE):
                    continue
                m = MOODS_MORE[i]
                with cols[offset]:
                    if st.button(
                        f"{m['icon']}  {m['label']}",
                        key=f"mmood_{m['id']}",
                        use_container_width=True,
                    ):
                        st.session_state.active_mood = m["id"]
                        st.session_state.active_tool = m["tools"][0]
                        st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

else:
    # A tool is selected — either from a mood or from the wheel
    active_tool_id = st.session_state.active_tool
    active_mood_id = st.session_state.active_mood
    mood = ALL_MOODS.get(active_mood_id) if active_mood_id else None

    if mood:
        banner_text = (f'{mood["icon"]} &nbsp; {mood["label"]} — using '
                       f'<strong>{TOOL_TITLES[active_tool_id]}</strong>')
        back_label = "← Different feeling"
    else:
        banner_text = (f'🎲 &nbsp; Random pick — using '
                       f'<strong>{TOOL_TITLES[active_tool_id]}</strong>')
        back_label = "← Back"

    # Header bar with back link
    cols = st.columns([5, 2])
    with cols[0]:
        st.markdown(
            f'<div class="active-mood-banner">{banner_text}</div>',
            unsafe_allow_html=True,
        )
    with cols[1]:
        if st.button(back_label, key="back_to_moods", use_container_width=True):
            st.session_state.active_mood = None
            st.session_state.active_tool = None
            st.rerun()

    # Render the active tool
    TOOL_DISPATCH[active_tool_id](kp=f"mood_{active_tool_id}")

    # Tool switcher (only for mood-picked tools with multiple recommendations)
    if mood and len(mood["tools"]) > 1:
        st.markdown('<div class="switcher-label">Other tools that may help</div>', unsafe_allow_html=True)
        cols = st.columns(len(mood["tools"]))
        for i, tid in enumerate(mood["tools"]):
            with cols[i]:
                is_current = tid == active_tool_id
                label = ("● " if is_current else "○ ") + TOOL_TITLES[tid]
                if st.button(label, key=f"switch_{tid}", use_container_width=True, disabled=is_current):
                    st.session_state.active_tool = tid
                    st.rerun()


# ── 3. SUPPORTING SECTIONS (collapsed) ───────────────────────────────────────

st.markdown('<div class="section-title">Other things you can do</div>', unsafe_allow_html=True)

# Browse all tools
with st.expander("📚  Browse all 18 tools"):
    st.markdown(
        '<div class="card-body" style="margin-bottom: 0.5rem;">'
        "Pick any tool individually. Each one tells you exactly when to use it and what to do."
        "</div>",
        unsafe_allow_html=True,
    )
    ALL_TOOLS_LIST = [
        ("Breathe", "🌿", "Box Breathing", "Universal first response — settle your nervous system"),
        ("Ground", "🌱", "5-4-3-2-1 Grounding", "Pull yourself out of past/future into the present"),
        ("1", "🪞", "Witness Practice", "An emotion is taking you over"),
        ("2", "🍃", "Thought Diffusion", "Intrusive / repetitive thoughts looping"),
        ("3", "⚡", "Pattern Interrupt + Pivot", "Already deep in a spiral"),
        ("4", "🙏", "The 'Thank You' Technique", "Anxiety from nowhere; logic isn't working"),
        ("5", "📋", "Worry Time", "Worries hijacking your day"),
        ("6", "🎯", "Control Inventory", "Feeling powerless"),
        ("7", "📵", "Emotional Circuit Breaker", "Rejection / taking it personally"),
        ("8", "🥊", "Redirection Protocol", "Urge to 'win' / get revenge"),
        ("9", "🔍", "Energy Exchange Audit", "Drained but can't pinpoint why"),
        ("10", "🫶", "Compassionate Container", "Absorbing others' emotions"),
        ("11", "💛", "Guilt Release", "After setting a boundary"),
        ("12", "🤐", "Minimal Explanation", "Compulsion to over-explain"),
        ("13", "☀️", "Morning Anchor Ritual", "Heavy chest on waking"),
        ("14", "🎭", "Reality Preservation", "Doubting your perception"),
        ("15", "🚶", "Change Your Environment", "Stuck — coping skills aren't working"),
        ("16", "🚪", "Point of No Return", "Tried to leave before but went back"),
    ]
    for tid, icon, title, when in ALL_TOOLS_LIST:
        with st.expander(f"{icon}  {title}  ·  {when}"):
            TOOL_DISPATCH[tid](kp=f"all_{tid}")


# Daily routine
with st.expander("🗓  Daily routine"):
    st.markdown(
        '<div class="card-body" style="margin-bottom: 1rem;">'
        "Each step shows exactly what to do, not just a tool name. Follow it as a checklist."
        "</div>",
        unsafe_allow_html=True,
    )

    st.markdown('<div class="timeline-item">', unsafe_allow_html=True)
    st.markdown('<div class="timeline-time">Wake up</div>', unsafe_allow_html=True)
    st.markdown(
        f"""
        <div class="card-body">
            <strong>Morning Anchor Ritual</strong> — before you get out of bed:
            <ol style="color: #b8b6b0; margin-left: 1.2rem; line-height: 1.9; margin-top: 0.5rem;">
                <li>Place your hand over your heart.</li>
                <li>Acknowledge any heaviness — don't fight it.</li>
                <li>Whisper: <em>"Thank you, for another day of life."</em></li>
                <li>Say: <em>"I am also in control of how I feel."</em></li>
                <li>Visualize: <em>{', '.join([p for p in data['morning_people'] if p]) or '(set your three people in Settings below)'}</em>.</li>
                <li>Let gratitude fill your chest, breath by breath.</li>
            </ol>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="timeline-item">', unsafe_allow_html=True)
    st.markdown('<div class="timeline-time">Throughout the day</div>', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="card-body">
            <strong>When an emotion takes you over</strong> — Witness Practice:
            <ol style="color: #b8b6b0; margin-left: 1.2rem; line-height: 1.8;">
                <li>Name it specifically: <em>"I'm noticing disappointment."</em></li>
                <li>Create distance: <em>"I notice anxiety arising in me right now."</em></li>
                <li>Find it in your body. Stay there 30 seconds.</li>
            </ol>
            <strong style="display: block; margin-top: 1rem;">When a worry pops up</strong> —
            don't engage. Acknowledge: <em>"I see you. I'll address you at worry time."</em>
            Then capture it (Worry Time tool).
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="timeline-item">', unsafe_allow_html=True)
    st.markdown('<div class="timeline-time">Midday</div>', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="card-body">
            <strong>Attention Restoration</strong> — 5-10 min completely device-free.
            No phone, no screens, no podcasts. Step outside if you can.
            Even sitting still in a quiet room counts. Your nervous system needs this gap.
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="timeline-item">', unsafe_allow_html=True)
    st.markdown('<div class="timeline-time">Evening</div>', unsafe_allow_html=True)
    active_count = len([w for w in data["worry_list"] if not w.get("addressed")])
    st.markdown(
        f"""
        <div class="card-body">
            <strong>Worry Time</strong> — {data['worry_time_slot'] or '(set your slot in Settings below)'}.
            Currently <strong>{active_count}</strong> active worries on your list. For each one:
            <ul style="color: #b8b6b0; margin-left: 1.2rem; line-height: 1.8; margin-top: 0.5rem;">
                <li>Action I can take NOW? If yes — what's the smallest first step?</li>
                <li>If no — can I accept this uncertainty for now?</li>
            </ul>
            Mark each one addressed when you're done. Close the list.
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="timeline-item">', unsafe_allow_html=True)
    st.markdown('<div class="timeline-time">Before sleep</div>', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="card-body">
            <strong>One good thing</strong> — counter the brain's negativity bias by naming
            ONE good thing that happened today. Could be tiny.
        </div>
        """,
        unsafe_allow_html=True,
    )
    g = st.text_input("Tonight's good thing:", key="grat_input", label_visibility="collapsed",
                      placeholder="One good thing that happened today...")
    if st.button("Save", key="save_grat"):
        if g.strip():
            data["evening_gratitude"].append({
                "date": datetime.now().strftime("%Y-%m-%d"),
                "text": g.strip(),
            })
            save_data(data)
            st.rerun()

    if data["evening_gratitude"]:
        with st.expander(f"My gratitude log ({len(data['evening_gratitude'])} entries)"):
            for entry in reversed(data["evening_gratitude"][-30:]):
                st.markdown(f"<div style='color: #b8b6b0; padding: 0.4rem 0;'>"
                            f"<span style='color: #d4a85a;'>{entry['date']}</span> — {entry['text']}</div>",
                            unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


# Settings & data
with st.expander("⚙️  Settings & my data"):
    st.markdown(
        '<div class="card-body" style="margin-bottom: 0.8rem;">'
        "Set these once — they personalize the daily routine and morning ritual."
        "</div>",
        unsafe_allow_html=True,
    )

    # Worry time
    st.markdown('<div class="section-title" style="font-size: 1rem;">Worry time slot</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        slot = st.text_input("My worry time", value=data["worry_time_slot"], key="settings_slot",
                             placeholder="e.g., Daily, 6:30 PM")
        if slot != data["worry_time_slot"]:
            data["worry_time_slot"] = slot
            save_data(data)
    with c2:
        place = st.text_input("Where I'll do it", value=data["worry_time_place"], key="settings_place",
                              placeholder="e.g., kitchen table")
        if place != data["worry_time_place"]:
            data["worry_time_place"] = place
            save_data(data)

    # 3 people
    st.markdown('<div class="section-title" style="font-size: 1rem;">My three people (morning ritual)</div>',
                unsafe_allow_html=True)
    cols = st.columns(3)
    changed = False
    for i, c in enumerate(cols):
        with c:
            v = st.text_input(f"Person {i+1}", value=data["morning_people"][i],
                              key=f"settings_mp_{i}", label_visibility="collapsed",
                              placeholder=f"Person {i+1}")
            if v != data["morning_people"][i]:
                data["morning_people"][i] = v
                changed = True
    if changed:
        save_data(data)

    # Data location
    st.markdown(
        f'<div class="card-body" style="margin-top: 1rem; color: #6f6c66; font-size: 0.85rem;">'
        f"Your data lives at <code>{DATA_FILE}</code>. Only on this computer."
        f"</div>",
        unsafe_allow_html=True,
    )


# ── Footer ───────────────────────────────────────────────────────────────────

st.markdown(
    '<div class="footer-text">You\'re stronger than you think. You always have been.</div>',
    unsafe_allow_html=True,
)
