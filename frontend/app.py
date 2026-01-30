import streamlit as st
import requests
import re

# =============================================================================
# CONFIGURATION
# =============================================================================
BACKEND_URL = "http://localhost:8000"

# Page Config
st.set_page_config(
    page_title="AURA-Learn | AI Career Architect",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =============================================================================
# CUSTOM CSS STYLES (Professional Dark Theme)
# =============================================================================
st.markdown("""
<style>
    /* Import Google Font */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');
    
    /* Global Reset & Font */
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        scroll-behavior: smooth;
    }
    
    /* Main App Background - Deep Space Dark */
    .stApp {
        background-color: #0E1117;
        background-image: radial-gradient(circle at 50% 0%, #1c2333 0%, #0E1117 70%);
        background-attachment: fixed;
    }
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #0d1016;
        border-right: 1px solid #2d313a;
    }
    
    /* Typography */
    h1 {
        background: linear-gradient(90deg, #4CC9F0 0%, #4361EE 50%, #7209B7 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800 !important;
        letter-spacing: -0.02em;
        margin-bottom: 0.5rem !important;
    }
    h2, h3 {
        color: #E2E8F0 !important;
        font-weight: 700 !important;
        letter-spacing: -0.01em;
    }
    p, li, span, label {
        color: #94A3B8;
        line-height: 1.6;
    }
    
    /* Custom Cards (Glassmorphism) */
    .custom-card {
        background: rgba(30, 41, 59, 0.4);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        backdrop-filter: blur(12px);
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        transition: all 0.3s ease;
    }
    .custom-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.2);
        border-color: #4361EE;
    }
    
    .card-title {
        color: #F8FAFC;
        font-size: 1.1rem;
        font-weight: 600;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }
    .card-body {
        color: #CBD5E1;
        font-size: 0.95rem;
    }
    
    /* Stage specific borders */
    .stage-foundation { border-left: 4px solid #4CC9F0; }
    .stage-growth { border-left: 4px solid #4361EE; }
    .stage-mastery { border-left: 4px solid #7209B7; }
    
    /* Input Fields */
    .stTextInput > div > div > input,
    .stSelectbox > div > div,
    .stTextArea > div > div > textarea {
        background-color: rgba(15, 23, 42, 0.6) !important;
        border: 1px solid #334155 !important;
        border-radius: 8px !important;
        color: #F1F5F9 !important;
        transition: border 0.2s;
    }
    .stTextInput > div > div > input:focus,
    .stSelectbox > div > div:focus {
        border-color: #4361EE !important;
        box-shadow: 0 0 0 2px rgba(67, 97, 238, 0.3) !important;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #4361EE 0%, #3A0CA3 100%);
        color: white !important;
        border: none;
        border-radius: 8px;
        font-weight: 600;
        padding: 0.6rem 1.5rem;
        box-shadow: 0 4px 6px rgba(67, 97, 238, 0.3);
        transition: all 0.2s ease;
    }
    .stButton > button:hover {
        transform: scale(1.02);
        box-shadow: 0 6px 12px rgba(67, 97, 238, 0.5);
    }
    /* Secondary/Ghost Buttons */
    button[kind="secondary"] {
        background: transparent !important;
        border: 1px solid #4361EE !important;
        color: #4361EE !important;
    }
    
    /* Tags */
    .skill-tag {
        display: inline-block;
        background: rgba(67, 97, 238, 0.15);
        border: 1px solid rgba(67, 97, 238, 0.3);
        color: #4CC9F0;
        padding: 5px 14px;
        border-radius: 20px;
        font-size: 0.8rem;
        margin: 4px;
        font-weight: 500;
        letter-spacing: 0.02em;
    }
    
    /* Status Indicators */
    .status-online { color: #10B981; font-weight: 600; font-size: 0.9rem; display: flex; align-items: center; gap: 8px; }
    .status-offline { color: #EF4444; font-weight: 600; font-size: 0.9rem; }
    .status-dot { width: 8px; height: 8px; background: #10B981; border-radius: 50%; box-shadow: 0 0 8px #10B981; animation: pulse 2s infinite; }
    
    /* Chat Bubbles */
    .chat-user {
        background: #1E293B;
        border: 1px solid #334155;
        padding: 1rem;
        border-radius: 12px 12px 0 12px;
        margin: 8px 0;
        text-align: right;
        margin-left: auto;
        max-width: 80%;
    }
    .chat-ai {
        background: rgba(67, 97, 238, 0.1);
        border: 1px solid rgba(67, 97, 238, 0.2);
        padding: 1rem;
        border-radius: 12px 12px 12px 0;
        margin: 8px 0;
        max-width: 90%;
    }

    /* Expander Styling */
    .streamlit-expanderHeader {
        background-color: rgba(30, 41, 59, 0.5) !important;
        border-radius: 8px !important;
        color: #F1F5F9 !important;
    }
    
    /* Utility */
    hr { border-color: #334155; margin: 2rem 0; }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    @keyframes pulse { 0% { opacity: 1; } 50% { opacity: 0.5; } 100% { opacity: 1; } }
</style>
""", unsafe_allow_html=True)

# =============================================================================
# SESSION STATE INITIALIZATION
# =============================================================================
if "current_page" not in st.session_state:
    st.session_state.current_page = "home"
if "user_profile" not in st.session_state:
    st.session_state.user_profile = {}
if "api_response" not in st.session_state:
    st.session_state.api_response = None
if "backend_status" not in st.session_state:
    st.session_state.backend_status = "unknown"
if "selected_skill" not in st.session_state:
    st.session_state.selected_skill = None
if "learning_content" not in st.session_state:
    st.session_state.learning_content = None
if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []
if "skill_feedback" not in st.session_state:
    st.session_state.skill_feedback = {}
if "refined_path" not in st.session_state:
    st.session_state.refined_path = None
if "feedback_changes" not in st.session_state:
    st.session_state.feedback_changes = []

# =============================================================================
# HELPER FUNCTIONS (BACKEND LOGIC - UNTOUCHED)
# =============================================================================
def check_backend_health():
    try:
        response = requests.get(f"{BACKEND_URL}/health", timeout=5)
        if response.status_code == 200 and response.json().get("status") == "ok":
            return "online"
    except:
        pass
    return "offline"

def call_orchestrate_api(user_input: str):
    try:
        response = requests.post(
            f"{BACKEND_URL}/orchestrate",
            params={"user_input": user_input},
            timeout=120
        )
        if response.status_code == 200:
            return {"success": True, "data": response.json()}
        else:
            return {"success": False, "error": f"HTTP {response.status_code}"}
    except requests.exceptions.Timeout:
        return {"success": False, "error": "Request timed out. The AI is taking too long."}
    except requests.exceptions.ConnectionError:
        return {"success": False, "error": "Cannot connect to backend. Is it running?"}
    except Exception as e:
        return {"success": False, "error": str(e)}

def navigate_to(page: str):
    st.session_state.current_page = page
    st.rerun()

def call_learn_api(skill: str, user_level: str = "Beginner"):
    try:
        response = requests.post(
            f"{BACKEND_URL}/learn",
            params={"skill": skill, "user_level": user_level},
            timeout=90
        )
        if response.status_code == 200:
            return {"success": True, "data": response.json()}
        else:
            return {"success": False, "error": f"HTTP {response.status_code}"}
    except Exception as e:
        return {"success": False, "error": str(e)}

def call_chat_api(message: str, skill_context: str = ""):
    try:
        response = requests.post(
            f"{BACKEND_URL}/chat",
            params={"message": message, "skill_context": skill_context},
            timeout=60
        )
        if response.status_code == 200:
            return {"success": True, "data": response.json()}
        else:
            return {"success": False, "error": f"HTTP {response.status_code}"}
    except Exception as e:
        return {"success": False, "error": str(e)}

def call_refine_api(original_path: dict, feedback: dict, original_goal: str):
    try:
        response = requests.post(
            f"{BACKEND_URL}/refine",
            json={
                "original_path": original_path,
                "feedback": feedback,
                "original_goal": original_goal
            },
            timeout=90
        )
        if response.status_code == 200:
            return {"success": True, "data": response.json()}
        else:
            return {"success": False, "error": f"HTTP {response.status_code}"}
    except Exception as e:
        return {"success": False, "error": str(e)}

def format_lesson_content(text: str) -> str:
    """Formats raw LLM output into clean HTML for display."""
    if not text:
        return ""
    text = re.sub(r'\n{3,}', '\n\n', text)
    lines = [line.strip() for line in text.split('\n')]
    text = '\n'.join(lines)
    text = re.sub(r'\*\*([^*]+)\*\*', r'<strong style="color: #F8FAFC; font-weight: 600;">\1</strong>', text)
    text = re.sub(r'`([^`]+)`', r'<code style="background: #1E293B; color: #4CC9F0; padding: 2px 6px; border-radius: 4px; font-family: monospace; font-size: 0.9em; border: 1px solid #334155;">\1</code>', text)
    text = re.sub(r'^(\d+)\.\s*\n*\s*', r'<div style="margin: 12px 0; padding-left: 8px; border-left: 2px solid #334155;"><span style="color: #4CC9F0; font-weight: 600;">\1.</span> ', text, flags=re.MULTILINE)
    text = re.sub(r'(<div style="margin: 12px 0.*?">.*?)(\n\n|$)', r'\1</div>\2', text, flags=re.DOTALL)
    text = re.sub(r'^[-•]\s*(.+)$', r'<div style="margin: 8px 0; padding-left: 16px;">• \1</div>', text, flags=re.MULTILINE)
    text = re.sub(r'^([A-Z][a-zA-Z\s]+):', r'<strong style="color: #4361EE;">\1:</strong>', text, flags=re.MULTILINE)
    text = text.replace('\n\n', '</p><p style="margin: 12px 0; color: #CBD5E1; line-height: 1.7;">')
    text = text.replace('\n', ' ')
    if not text.startswith('<'):
        text = f'<p style="margin: 12px 0; color: #CBD5E1; line-height: 1.7;">{text}</p>'
    return text

# =============================================================================
# SIDEBAR
# =============================================================================
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/artificial-intelligence.png", width=60)
    st.markdown("## AURA-Learn")
    st.caption("AI Career Architect v2.2")
    st.markdown("---")
    
    st.markdown("### Menu")
    
    # Navigation Buttons
    if st.button("🏠  Dashboard", use_container_width=True, key="nav_home"):
        navigate_to("home")
    if st.button("🚀  Planner", use_container_width=True, key="nav_planner"):
        navigate_to("planner")
    if st.button("📚  Classroom", use_container_width=True, key="nav_learn"):
        navigate_to("learn")
    if st.button("ℹ️  About System", use_container_width=True, key="nav_about"):
        navigate_to("about")
    
    st.markdown("---")
    
    # System Status
    st.markdown("### System Health")
    status = check_backend_health()
    st.session_state.backend_status = status
    
    if status == "online":
        st.markdown("""
        <div class="status-online">
            <span class="status-dot"></span>
            <span>Neural Core Online</span>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="status-offline">
            ⚠️ Backend Disconnected
        </div>
        """, unsafe_allow_html=True)
        st.caption("Check server logs")

# =============================================================================
# PAGE: HOME
# =============================================================================
def render_home_page():
    # Hero Section
    st.markdown("""
    <div style="text-align: center; padding: 5rem 1rem;">
        <h1 style="font-size: 4rem; line-height: 1.2; margin-bottom: 1.5rem;">
            Architect Your <br> <span style="background: linear-gradient(90deg, #4CC9F0, #4361EE); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Future Self</span>
        </h1>
        <p style="font-size: 1.2rem; color: #94A3B8; max-width: 700px; margin: 0 auto 3rem auto;">
            Stop guessing. Start evolving. AURA uses multi-agent AI to construct 
            hallucination-free, industry-verified learning architectures tailored specifically to you.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 0.8, 1])
    with col2:
        if st.button("⚡ Build My Roadmap", use_container_width=True, key="home_cta"):
            navigate_to("planner")
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("### Core Capabilities")
    
    f1, f2, f3 = st.columns(3)
    
    with f1:
        st.markdown("""
        <div class="custom-card">
            <div class="card-title"><span style="font-size:1.5rem">🧠</span> Grounded Intelligence</div>
            <div class="card-body">
                Curated knowledge bases ensure every recommendation is factual. 
                Zero hallucinations, 100% verifiable skills.
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with f2:
        st.markdown("""
        <div class="custom-card">
            <div class="card-title"><span style="font-size:1.5rem">🤖</span> Agentic Orchestration</div>
            <div class="card-body">
                A symphony of specialized agents analyzes your profile, decomposes 
                complex goals, and optimizes your path.
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with f3:
        st.markdown("""
        <div class="custom-card">
            <div class="card-title"><span style="font-size:1.5rem">👁️</span> Transparent Reasoning</div>
            <div class="card-body">
                Don't just follow orders. Our explainability engine reveals the 'Why' 
                behind every step of your journey.
            </div>
        </div>
        """, unsafe_allow_html=True)

# =============================================================================
# PAGE: PLANNER
# =============================================================================
def render_planner_page():
    st.markdown("# 🚀 Path Generator")
    st.markdown("Configure your parameters. The agents will architect a bespoke roadmap.")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    with st.container():
        st.markdown("""
        <div style="background: rgba(30, 41, 59, 0.3); padding: 2rem; border-radius: 16px; border: 1px solid rgba(255,255,255,0.05);">
        """, unsafe_allow_html=True)
        
        with st.form(key="planner_form", clear_on_submit=False):
            st.markdown("### 👤 User Parameters")
            c1, c2 = st.columns(2)
            with c1:
                name = st.text_input("Full Name", value=st.session_state.user_profile.get("name", ""), placeholder="e.g. Alex Chen")
                degree = st.text_input("Current Qualification", value=st.session_state.user_profile.get("degree", ""), placeholder="e.g. B.Tech Computer Science")
            with c2:
                role = st.selectbox("Current Role", ["Student", "University Faculty", "Working Professional", "Researcher", "Career Changer"])
                knowledge_level = st.selectbox("Proficiency Level", ["Beginner (Novice)", "Intermediate (Competent)", "Advanced (Proficient)", "Expert (Master)"])
            
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("### 🎯 Target Objective")
            goal = st.text_input("Primary Ambition", value=st.session_state.user_profile.get("goal", ""), placeholder="e.g. Master MLOps and deploy LLMs on AWS")
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            c_sub1, c_sub2, c_sub3 = st.columns([1, 2, 1])
            with c_sub2:
                generate_clicked = st.form_submit_button("✨ Initialize Architecture Agent", use_container_width=True)
        
        st.markdown("</div>", unsafe_allow_html=True)

    if generate_clicked:
        if not goal.strip():
            st.error("⚠️  Objective required to proceed.")
        else:
            st.session_state.user_profile = {"name": name, "degree": degree, "role": role, "level": knowledge_level, "goal": goal}
            enriched_input = f"User Profile: {name}, {role}, {knowledge_level}, Background: {degree}. Learning Goal: {goal}"
            
            with st.spinner("🔄 Agents orchestrating... Analyzing constraints and dependencies..."):
                result = call_orchestrate_api(enriched_input)
            
            if result["success"]:
                st.session_state.api_response = result["data"]
                st.success("✅ Architecture generated successfully.")
            else:
                st.error(f"❌ System Fault: {result['error']}")

    if st.session_state.api_response:
        render_results_section(st.session_state.api_response)

def render_results_section(data: dict):
    st.markdown("---")
    st.markdown("## 📊 Your Architecture")
    
    learning_plan = data.get("learning_plan", {})
    if learning_plan.get("status") != "success":
        st.error(f"🚫 {learning_plan.get('message', 'Generation failed.')}")
        return
    
    roadmap = learning_plan.get("learning_path", {})
    skills_identified = learning_plan.get("skills_identified", [])
    
    if skills_identified:
        st.markdown("**Identified Key Skills:**")
        skills_html = "".join([f'<span class="skill-tag">{skill}</span>' for skill in skills_identified[:15]])
        st.markdown(f'<div style="margin-bottom: 2rem;">{skills_html}</div>', unsafe_allow_html=True)
    
    # Stages
    c1, c2, c3 = st.columns(3)
    
    with c1:
        skills = roadmap.get("foundation", [])
        content = "".join([f"<li>{s}</li>" for s in skills]) if skills else "<li>Analyzing prerequisites...</li>"
        st.markdown(f"""
        <div class="custom-card stage-foundation">
            <div class="card-title">🏗️ Foundation</div>
            <div class="card-body"><ul style="padding-left:1rem;margin:0">{content}</ul></div>
        </div>
        """, unsafe_allow_html=True)
    
    with c2:
        skills = roadmap.get("intermediate", [])
        content = "".join([f"<li>{s}</li>" for s in skills]) if skills else "<li>Calculating trajectory...</li>"
        st.markdown(f"""
        <div class="custom-card stage-growth">
            <div class="card-title">🚀 Growth</div>
            <div class="card-body"><ul style="padding-left:1rem;margin:0">{content}</ul></div>
        </div>
        """, unsafe_allow_html=True)
    
    with c3:
        skills = roadmap.get("advanced", [])
        content = "".join([f"<li>{s}</li>" for s in skills]) if skills else "<li>Defining mastery...</li>"
        st.markdown(f"""
        <div class="custom-card stage-mastery">
            <div class="card-title">🏆 Mastery</div>
            <div class="card-body"><ul style="padding-left:1rem;margin:0">{content}</ul></div>
        </div>
        """, unsafe_allow_html=True)
    
    # Cross Domain
    cross_domain = data.get("cross_domain_impact", {})
    if cross_domain:
        st.markdown("### 🌐 Application Domains")
        d1, d2, d3 = st.columns(3)
        for idx, (domain, impact) in enumerate(list(cross_domain.items())[:3]):
            with [d1, d2, d3][idx]:
                st.markdown(f"""
                <div class="custom-card">
                    <div class="card-title">🔗 {domain.capitalize()}</div>
                    <div class="card-body">{impact}</div>
                </div>
                """, unsafe_allow_html=True)

    # Explanation
    explanation = data.get("explanation", {})
    if explanation:
        with st.expander("🧠 **View Agent Reasoning**"):
            st.markdown(f"**Strategic Summary:** {explanation.get('summary', 'N/A')}")
            st.markdown(f"**Confidence Score:** `{explanation.get('confidence', 'N/A')}`")
            if explanation.get("assumptions"):
                st.markdown("**Assumptions:**")
                for a in explanation["assumptions"]:
                    st.markdown(f"- {a}")

    # Feedback Refinement Loop
    st.markdown("---")
    st.markdown("### 🔄 Optimization Loop")
    st.info("💡 Rate skills to help the agents recalibrate your learning path.")
    
    all_skills = []
    all_skills.extend([(s, "Foundation") for s in roadmap.get("foundation", [])])
    all_skills.extend([(s, "Growth") for s in roadmap.get("intermediate", [])])
    all_skills.extend([(s, "Mastery") for s in roadmap.get("advanced", [])])
    
    with st.expander("📝 **Open Skill Calibration Panel**", expanded=True):
        feedback_options = ["✅ Keep", "📚 Already Know", "⚡ Too Advanced", "❌ Not Relevant", "🔍 Want More"]
        
        # Grid layout for cleaner feedback
        for stage_name, color in [("Foundation", "#4CC9F0"), ("Growth", "#4361EE"), ("Mastery", "#7209B7")]:
            stage_skills = [s for s, stg in all_skills if stg == stage_name]
            if stage_skills:
                st.markdown(f'<div style="color:{color};font-weight:700;margin-top:1rem;border-bottom:1px solid {color}33;padding-bottom:5px;">{stage_name} Phase</div>', unsafe_allow_html=True)
                for skill in stage_skills:
                    fc1, fc2 = st.columns([3, 2])
                    with fc1:
                        st.markdown(f"<span style='color:#CBD5E1; vertical-align: middle;'>{skill}</span>", unsafe_allow_html=True)
                    with fc2:
                        current = st.session_state.skill_feedback.get(skill, "✅ Keep")
                        new_rating = st.selectbox(f"Rate {skill}", feedback_options, index=feedback_options.index(current) if current in feedback_options else 0, key=f"fb_{skill}", label_visibility="collapsed")
                        st.session_state.skill_feedback[skill] = new_rating

        st.markdown("<br>", unsafe_allow_html=True)
        gen_feedback = st.text_area("Additional constraints or preferences", height=80)
        
        if st.button("🔄 Refine Architecture", key="refine_btn", use_container_width=True):
            skill_ratings = {s: r for s, r in st.session_state.skill_feedback.items() if r != "✅ Keep"}
            feedback_map = {"✅ Keep": "keep", "📚 Already Know": "already_known", "⚡ Too Advanced": "too_advanced", "❌ Not Relevant": "not_relevant", "🔍 Want More": "want_more"}
            formatted_feedback = {k: feedback_map.get(v, "keep") for k, v in skill_ratings.items()}
            
            with st.spinner("🔄 Re-calculating optimal path..."):
                res = call_refine_api(learning_plan, {"skill_feedback": formatted_feedback, "general_feedback": gen_feedback}, st.session_state.user_profile.get("goal",""))
            
            if res["success"]:
                st.session_state.refined_path = res["data"].get("refined_path")
                st.session_state.feedback_changes = res["data"].get("changes_made", [])
                st.success("Calibration complete.")
                st.rerun()
            else:
                st.error(res["error"])

    if st.session_state.refined_path:
        st.markdown("### ✨ Optimized Path Proposal")
        if st.session_state.feedback_changes:
            st.success(f"Adjustments: {', '.join(st.session_state.feedback_changes)}")
        
        # Display Refined Layout (Simplified for brevity)
        r1, r2, r3 = st.columns(3)
        rp = st.session_state.refined_path
        with r1:
            st.markdown(f"<div class='custom-card stage-foundation'><div class='card-title'>New Foundation</div><div class='card-body'><ul>{''.join([f'<li>{s}</li>' for s in rp.get('foundation',[])])}</ul></div></div>", unsafe_allow_html=True)
        with r2:
            st.markdown(f"<div class='custom-card stage-growth'><div class='card-title'>New Growth</div><div class='card-body'><ul>{''.join([f'<li>{s}</li>' for s in rp.get('intermediate',[])])}</ul></div></div>", unsafe_allow_html=True)
        with r3:
            st.markdown(f"<div class='custom-card stage-mastery'><div class='card-title'>New Mastery</div><div class='card-body'><ul>{''.join([f'<li>{s}</li>' for s in rp.get('advanced',[])])}</ul></div></div>", unsafe_allow_html=True)
            
        if st.button("✅ Commit to This Path", use_container_width=True):
            st.session_state.api_response["learning_plan"]["learning_path"] = st.session_state.refined_path
            st.session_state.refined_path = None
            st.rerun()

# =============================================================================
# PAGE: LEARN
# =============================================================================
def render_learn_page():
    st.markdown("# 📚 Interactive Knowledge Base")
    
    roadmap = {}
    if st.session_state.api_response:
        roadmap = st.session_state.api_response.get("learning_plan", {}).get("learning_path", {})

    main_col, path_col = st.columns([7, 3])
    
    with path_col:
        st.markdown("### 🗺️ Context")
        if roadmap:
            for stage, color, icon in [("foundation", "#4CC9F0", "🏗️"), ("intermediate", "#4361EE", "🚀"), ("advanced", "#7209B7", "🏆")]:
                skills = roadmap.get(stage, [])
                if skills:
                    st.markdown(f"""
                    <div style="background: rgba(15, 23, 42, 0.5); border-left: 3px solid {color}; padding: 10px; margin-bottom: 8px; border-radius: 0 8px 8px 0;">
                        <div style="color: {color}; font-weight: 700; font-size: 0.85rem; margin-bottom: 5px;">{icon} {stage.capitalize()}</div>
                    """, unsafe_allow_html=True)
                    for skill in skills[:5]:
                        marker = "➤ " if skill == st.session_state.selected_skill else ""
                        st.markdown(f'<div style="color: #94A3B8; font-size: 0.8rem; padding: 1px 0;">{marker}{skill}</div>', unsafe_allow_html=True)
                    st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.info("No roadmap found. Go to Planner.")

    with main_col:
        st.markdown("### 🔍 Topic Explorer")
        ic1, ic2, ic3 = st.columns([3, 1, 1])
        with ic1:
            manual_skill = st.text_input("Skill/Concept", placeholder="e.g. Docker Containers", label_visibility="collapsed")
        with ic2:
            user_level = st.selectbox("Depth", ["Beginner", "Intermediate", "Advanced"], label_visibility="collapsed")
        with ic3:
            if st.button("Start", use_container_width=True):
                target = manual_skill.strip() or st.session_state.selected_skill
                if target:
                    st.session_state.selected_skill = target
                    with st.spinner("Retrieving verified content..."):
                        res = call_learn_api(target, user_level)
                        if res["success"]: st.session_state.learning_content = res["data"]
                else:
                    st.warning("Enter a topic.")

        # Content Display
        if st.session_state.learning_content:
            data = st.session_state.learning_content
            if data.get("status") == "success":
                st.markdown("---")
                st.markdown(f"<h2 style='color:#4CC9F0!important'>{data.get('skill')}</h2>", unsafe_allow_html=True)
                
                raw = data.get('content', '')
                
                # Render content in sections
                sections = {
                    "Introduction": {"icon": "📌", "color": "#4CC9F0"},
                    "Key Concepts": {"icon": "🔑", "color": "#4361EE"},
                    "Practical Example": {"icon": "💻", "color": "#10B981"},
                    "Common Mistakes": {"icon": "⚠️", "color": "#F59E0B"},
                    "Next Steps": {"icon": "🚀", "color": "#7209B7"}
                }
                
                # Simple parsing logic (preserved from original)
                curr = None
                parsed = {}
                for line in raw.split('\n'):
                    found = False
                    for s in sections:
                        if s.lower() in line.lower() and ('**' in line or '#' in line):
                            curr = s
                            parsed[curr] = []
                            found = True
                            break
                    if not found and curr: parsed[curr].append(line)

                if parsed:
                    for s_name, config in sections.items():
                        if s_name in parsed and parsed[s_name]:
                            html = format_lesson_content('\n'.join(parsed[s_name]))
                            st.markdown(f"""
                            <div style="background: rgba(30, 41, 59, 0.4); border: 1px solid {config['color']}44; border-left: 4px solid {config['color']}; border-radius: 8px; padding: 20px; margin: 16px 0;">
                                <div style="color: {config['color']}; font-weight: 700; margin-bottom: 10px; display: flex; align-items: center; gap: 8px;">
                                    <span style="font-size: 1.2rem;">{config['icon']}</span> {s_name}
                                </div>
                                <div>{html}</div>
                            </div>
                            """, unsafe_allow_html=True)
                else:
                    st.markdown(format_lesson_content(raw), unsafe_allow_html=True)

        # Chat
        st.markdown("---")
        st.markdown("### 💬 Neural Tutor")
        
        # Chat History
        if st.session_state.chat_messages:
            for msg in st.session_state.chat_messages:
                if msg["role"] == "user":
                    st.markdown(f'<div class="chat-user"><div style="color:#4CC9F0;font-size:0.8rem;margin-bottom:4px;">YOU</div>{msg["content"]}</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="chat-ai"><div style="color:#7209B7;font-size:0.8rem;margin-bottom:4px;">AURA</div>{msg["content"]}</div>', unsafe_allow_html=True)
        
        # Chat Input
        with st.form(key="chat_form", clear_on_submit=True):
            c_in, c_btn = st.columns([5, 1])
            with c_in:
                user_q = st.text_input("Ask a question...", placeholder="Explain this concept simply...", label_visibility="collapsed")
            with c_btn:
                send = st.form_submit_button("Send")
            
            if send and user_q:
                st.session_state.chat_messages.append({"role": "user", "content": user_q})
                with st.spinner("Processing..."):
                    res = call_chat_api(user_q, st.session_state.selected_skill or "")
                    ans = res["data"]["response"] if res["success"] else f"Error: {res['error']}"
                    st.session_state.chat_messages.append({"role": "assistant", "content": ans})
                st.rerun()

# =============================================================================
# PAGE: ABOUT
# =============================================================================
def render_about_page():
    st.markdown("# ℹ️ System Architecture")
    st.markdown("AURA (Agentic Universal Reasoning Architecture) represents a shift from static learning to dynamic, AI-architected growth.")
    
    st.markdown("---")
    
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("### 🧩 Core Agents")
        st.markdown("""
        <div class="custom-card">
            <strong style="color:#4CC9F0">Orchestrator Agent</strong><br>
            Analyzes high-level goals and decomposes them into dependency graphs.
        </div>
        <div class="custom-card">
            <strong style="color:#4361EE">Education Agent</strong><br>
            Interfaces with vector databases to retrieve grounded educational content.
        </div>
        """, unsafe_allow_html=True)
    
    with c2:
        st.markdown("### 🛡️ Guardrails")
        st.markdown("""
        <div class="custom-card">
            <strong style="color:#10B981">Fact Verification</strong><br>
            Cross-references LLM output against trusted knowledge bases.
        </div>
        <div class="custom-card">
            <strong style="color:#F59E0B">Explainability</strong><br>
            Forces the model to output reasoning chains before final conclusions.
        </div>
        """, unsafe_allow_html=True)
        
    st.info("🏆 Built for GenAI Hackathon 2026 • AWS Bedrock Track")

# =============================================================================
# ROUTER
# =============================================================================
if st.session_state.current_page == "home":
    render_home_page()
elif st.session_state.current_page == "planner":
    render_planner_page()
elif st.session_state.current_page == "learn":
    render_learn_page()
elif st.session_state.current_page == "about":
    render_about_page()
else:
    render_home_page()