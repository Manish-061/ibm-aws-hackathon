import streamlit as st
import requests

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
# CUSTOM CSS STYLES
# =============================================================================
st.markdown("""
<style>
    /* Import Google Font */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    
    /* Global Styling */
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }
    
    /* Main App Background */
    .stApp {
        background: linear-gradient(135deg, #0D1117 0%, #161B22 50%, #0D1117 100%);
    }
    
    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #161B22 0%, #0D1117 100%);
        border-right: 1px solid #30363D;
    }
    section[data-testid="stSidebar"] .block-container {
        padding-top: 2rem;
    }
    
    /* Headers */
    h1 {
        background: linear-gradient(90deg, #58A6FF 0%, #A371F7 50%, #F778BA 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 800 !important;
    }
    h2, h3 {
        color: #F0F6FC !important;
        font-weight: 600 !important;
    }
    
    /* Text */
    p, li, span {
        color: #8B949E;
    }
    
    /* Cards */
    .custom-card {
        background: rgba(22, 27, 34, 0.8);
        border: 1px solid #30363D;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
    }
    .custom-card:hover {
        border-color: #58A6FF;
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(88, 166, 255, 0.1);
    }
    .card-title {
        color: #F0F6FC;
        font-size: 1rem;
        font-weight: 600;
        margin-bottom: 0.75rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    .card-body {
        color: #8B949E;
        font-size: 0.9rem;
        line-height: 1.6;
    }
    
    /* Stage Cards */
    .stage-foundation { border-left: 4px solid #58A6FF; }
    .stage-growth { border-left: 4px solid #A371F7; }
    .stage-mastery { border-left: 4px solid #3FB950; }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #6E40C9 0%, #7C4DFF 50%, #58A6FF 100%);
        color: white !important;
        border: none;
        border-radius: 8px;
        font-weight: 600;
        padding: 0.75rem 2rem;
        transition: all 0.2s ease;
        box-shadow: 0 4px 12px rgba(124, 77, 255, 0.3);
    }
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 6px 20px rgba(124, 77, 255, 0.5);
        background: linear-gradient(135deg, #7C4DFF 0%, #8B5CF6 50%, #58A6FF 100%);
    }
    
    /* Form Inputs */
    .stTextInput > div > div > input,
    .stSelectbox > div > div {
        background-color: #0D1117 !important;
        border: 1px solid #30363D !important;
        border-radius: 8px !important;
        color: #F0F6FC !important;
    }
    .stTextInput > div > div > input:focus {
        border-color: #58A6FF !important;
        box-shadow: 0 0 0 3px rgba(88, 166, 255, 0.2) !important;
    }
    
    /* Tags/Badges */
    .skill-tag {
        display: inline-block;
        background: rgba(88, 166, 255, 0.1);
        border: 1px solid rgba(88, 166, 255, 0.3);
        color: #58A6FF;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.85rem;
        margin: 4px;
        font-weight: 500;
    }
    
    /* Status Indicator */
    .status-online {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        color: #3FB950;
        font-size: 0.85rem;
    }
    .status-dot {
        width: 8px;
        height: 8px;
        background: #3FB950;
        border-radius: 50%;
        animation: pulse 2s infinite;
    }
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }
    
    /* Hero Section */
    .hero-container {
        text-align: center;
        padding: 4rem 2rem;
    }
    .hero-tagline {
        font-size: 1.25rem;
        color: #8B949E;
        margin-bottom: 2rem;
        max-width: 600px;
        margin-left: auto;
        margin-right: auto;
    }
    
    /* Feature Cards */
    .feature-icon {
        font-size: 2rem;
        margin-bottom: 1rem;
    }
    
    /* Expander Styling */
    .streamlit-expanderHeader {
        background-color: #161B22;
        border-radius: 8px;
    }
    
    /* Dividers */
    hr {
        border-color: #30363D;
    }
    
    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
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
# HELPER FUNCTIONS
# =============================================================================
def check_backend_health():
    """Check if backend is online."""
    try:
        response = requests.get(f"{BACKEND_URL}/health", timeout=5)
        if response.status_code == 200 and response.json().get("status") == "ok":
            return "online"
    except:
        pass
    return "offline"

def call_orchestrate_api(user_input: str):
    """Call the /orchestrate endpoint."""
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
    """Navigate to a different page."""
    st.session_state.current_page = page
    st.rerun()

def call_learn_api(skill: str, user_level: str = "Beginner"):
    """Call the /learn endpoint to get educational content."""
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
    """Call the /chat endpoint for interactive tutoring."""
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
    """Call the /refine endpoint to get a refined learning path based on feedback."""
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

import re

def format_lesson_content(text: str) -> str:
    """
    Format raw LLM output into clean, professional HTML.
    - Converts **bold** to styled bold
    - Converts `code` to styled code spans
    - Cleans up extra whitespace
    - Formats numbered lists properly
    - Highlights important terms
    """
    if not text:
        return ""
    
    # Remove excessive blank lines (more than 2 consecutive)
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    # Remove leading/trailing whitespace from each line
    lines = [line.strip() for line in text.split('\n')]
    text = '\n'.join(lines)
    
    # Convert markdown bold **text** to styled HTML
    text = re.sub(
        r'\*\*([^*]+)\*\*',
        r'<strong style="color: #F0F6FC; font-weight: 600;">\1</strong>',
        text
    )
    
    # Convert markdown code `code` to styled code spans
    text = re.sub(
        r'`([^`]+)`',
        r'<code style="background: #21262D; color: #79C0FF; padding: 2px 6px; border-radius: 4px; font-family: monospace; font-size: 0.9em;">\1</code>',
        text
    )
    
    # Format numbered list items (1. 2. 3. etc.) - clean up spacing
    text = re.sub(
        r'^(\d+)\.\s*\n*\s*',
        r'<div style="margin: 12px 0; padding-left: 8px; border-left: 2px solid #30363D;"><span style="color: #8B949E; font-weight: 600;">\1.</span> ',
        text,
        flags=re.MULTILINE
    )
    
    # Close numbered items at double newlines or end
    text = re.sub(r'(<div style="margin: 12px 0.*?">.*?)(\n\n|$)', r'\1</div>\2', text, flags=re.DOTALL)
    
    # Format bullet points
    text = re.sub(
        r'^[-•]\s*(.+)$',
        r'<div style="margin: 8px 0; padding-left: 16px;">• \1</div>',
        text,
        flags=re.MULTILINE
    )
    
    # Highlight key terms (words followed by colon at start of concept)
    text = re.sub(
        r'^([A-Z][a-zA-Z\s]+):',
        r'<strong style="color: #A371F7;">\1:</strong>',
        text,
        flags=re.MULTILINE
    )
    
    # Convert remaining newlines to proper spacing
    text = text.replace('\n\n', '</p><p style="margin: 12px 0; color: #C9D1D9; line-height: 1.7;">')
    text = text.replace('\n', ' ')
    
    # Wrap in paragraph if not already structured
    if not text.startswith('<'):
        text = f'<p style="margin: 12px 0; color: #C9D1D9; line-height: 1.7;">{text}</p>'
    
    return text


# =============================================================================
# SIDEBAR
# =============================================================================
with st.sidebar:
    # Logo Area
    st.markdown("# 🎓 AURA-Learn")
    st.markdown("*AI-Powered Career Architect*")
    
    st.markdown("---")
    
    # Navigation
    st.markdown("### Navigation")
    
    if st.button("🏠  Home", use_container_width=True, key="nav_home"):
        navigate_to("home")
    
    if st.button("🚀  Get Started", use_container_width=True, key="nav_planner"):
        navigate_to("planner")
    
    if st.button("📚  Learn", use_container_width=True, key="nav_learn"):
        navigate_to("learn")
    
    if st.button("📖  About", use_container_width=True, key="nav_about"):
        navigate_to("about")
    
    st.markdown("---")
    
    # System Status
    st.markdown("### System Status")
    
    # Check backend on sidebar load
    status = check_backend_health()
    st.session_state.backend_status = status
    
    if status == "online":
        st.markdown("""
        <div class="status-online">
            <span class="status-dot"></span>
            All Systems Operational
        </div>
        """, unsafe_allow_html=True)
    else:
        st.error("⚠️ Backend Offline")
        st.caption("Start the backend server.")
    
    st.markdown("---")
    st.caption("v2.2 • GenAI Hackathon 2026")

# =============================================================================
# PAGE: HOME
# =============================================================================
def render_home_page():
    # Hero Section
    st.markdown("""
    <div class="hero-container">
        <h1 style="font-size: 3.5rem; margin-bottom: 1rem;">
            Architect Your Future
        </h1>
        <p class="hero-tagline">
            Stop guessing your learning path. AURA-Learn uses advanced AI agents 
            grounded in verified knowledge to build personalized, hallucination-free 
            roadmaps tailored to your exact career goals.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # CTA Button
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🚀 Start Your Journey", use_container_width=True, key="home_cta"):
            navigate_to("planner")
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Features Section
    st.markdown("## Why AURA-Learn?")
    st.markdown("<br>", unsafe_allow_html=True)
    
    f1, f2, f3 = st.columns(3)
    
    with f1:
        st.markdown("""
        <div class="custom-card">
            <div class="feature-icon">🎯</div>
            <div class="card-title">Grounded Knowledge</div>
            <div class="card-body">
                Every recommendation is backed by verified educational content 
                from curated knowledge bases. No hallucinations, only facts.
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with f2:
        st.markdown("""
        <div class="custom-card">
            <div class="feature-icon">🤖</div>
            <div class="card-title">Agentic Intelligence</div>
            <div class="card-body">
                Multiple specialized AI agents collaborate to analyze your goals, 
                decompose skills, and construct optimized learning architectures.
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with f3:
        st.markdown("""
        <div class="custom-card">
            <div class="feature-icon">🔍</div>
            <div class="card-title">Full Transparency</div>
            <div class="card-body">
                Understand exactly why each skill was recommended. Our explainability 
                engine reveals the AI's reasoning and confidence levels.
            </div>
        </div>
        """, unsafe_allow_html=True)

# =============================================================================
# PAGE: PLANNER (Main Functionality)
# =============================================================================
def render_planner_page():
    st.markdown("# 🚀 Learning Path Generator")
    st.markdown("Complete your profile below, and our AI agents will construct a personalized roadmap.")
    
    st.markdown("---")
    
    # Wrap everything in a form to avoid "Press Enter to apply"
    with st.form(key="planner_form", clear_on_submit=False):
        # User Profile Form
        st.markdown("### 👤 Your Profile")
        
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input(
                "Full Name",
                value=st.session_state.user_profile.get("name", ""),
                placeholder="Enter your name"
            )
            
            degree = st.text_input(
                "Current Qualification",
                value=st.session_state.user_profile.get("degree", ""),
                placeholder="e.g., B.Tech in Computer Science"
            )
        
        with col2:
            role = st.selectbox(
                "Professional Category",
                options=["Student", "University Faculty", "Working Professional", "Researcher", "Career Changer"],
                index=0
            )
            
            knowledge_level = st.selectbox(
                "Current Knowledge Level",
                options=["Beginner (Just starting)", "Intermediate (Some experience)", "Advanced (Solid foundation)", "Expert (Deep expertise)"],
                index=0
            )
        
        st.markdown("---")
        st.markdown("### 🎯 Learning Objective")
        
        goal = st.text_input(
            "What skill or role do you want to master?",
            value=st.session_state.user_profile.get("goal", ""),
            placeholder="e.g., Master backend development with Python and cloud technologies"
        )
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Form Submit Button (no need to press Enter for each field)
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            generate_clicked = st.form_submit_button(
                "✨ Generate My Learning Path",
                use_container_width=True
            )
    
    # Handle Form Submission (outside the form block)
    if generate_clicked:
        if not goal.strip():
            st.error("⚠️ Please enter a learning objective.")
        else:
            # Save profile to session
            st.session_state.user_profile = {
                "name": name,
                "degree": degree,
                "role": role,
                "level": knowledge_level,
                "goal": goal
            }
            
            # Construct enriched prompt for backend
            enriched_input = (
                f"User Profile: {name}, {role}, {knowledge_level}, "
                f"Background: {degree}. "
                f"Learning Goal: {goal}"
            )
            
            # Call API with progress indicator
            with st.spinner("🔄 Orchestrating AI Agents... This may take up to 30 seconds."):
                result = call_orchestrate_api(enriched_input)
            
            if result["success"]:
                st.session_state.api_response = result["data"]
                st.success("✅ Learning path generated successfully!")
            else:
                st.error(f"❌ Error: {result['error']}")
                st.session_state.api_response = None
    
    # Display Results if Available
    if st.session_state.api_response:
        render_results_section(st.session_state.api_response)

def render_results_section(data: dict):
    """Render the learning path results."""
    st.markdown("---")
    st.markdown("## 📊 Your Personalized Learning Architecture")
    
    learning_plan = data.get("learning_plan", {})
    
    # Check for errors
    if learning_plan.get("status") != "success":
        error_message = learning_plan.get("message", "Unable to generate a learning path.")
        st.error(f"🚫 {error_message}")
        return
    
    roadmap = learning_plan.get("learning_path", {})
    skills_identified = learning_plan.get("skills_identified", [])
    
    # Skills Overview
    if skills_identified:
        st.markdown("### 🏷️ Skills Identified")
        skills_html = "".join([f'<span class="skill-tag">{skill}</span>' for skill in skills_identified[:15]])
        st.markdown(f'<div style="margin-bottom: 1.5rem;">{skills_html}</div>', unsafe_allow_html=True)
    
    # Learning Stages
    st.markdown("### 📚 Learning Stages")
    
    c1, c2, c3 = st.columns(3)
    
    with c1:
        foundation_skills = roadmap.get("foundation", [])
        skills_list = "".join([f"<li>{s}</li>" for s in foundation_skills]) if foundation_skills else "<li>No prerequisites needed</li>"
        st.markdown(f"""
        <div class="custom-card stage-foundation">
            <div class="card-title">🏗️ Foundation</div>
            <div class="card-body">
                <ul style="padding-left: 1.2rem; margin: 0;">{skills_list}</ul>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with c2:
        intermediate_skills = roadmap.get("intermediate", [])
        skills_list = "".join([f"<li>{s}</li>" for s in intermediate_skills]) if intermediate_skills else "<li>Build on foundations</li>"
        st.markdown(f"""
        <div class="custom-card stage-growth">
            <div class="card-title">🚀 Growth</div>
            <div class="card-body">
                <ul style="padding-left: 1.2rem; margin: 0;">{skills_list}</ul>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with c3:
        advanced_skills = roadmap.get("advanced", [])
        skills_list = "".join([f"<li>{s}</li>" for s in advanced_skills]) if advanced_skills else "<li>Achieve mastery</li>"
        st.markdown(f"""
        <div class="custom-card stage-mastery">
            <div class="card-title">🏆 Mastery</div>
            <div class="card-body">
                <ul style="padding-left: 1.2rem; margin: 0;">{skills_list}</ul>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Cross-Domain Impact
    cross_domain = data.get("cross_domain_impact", {})
    if cross_domain:
        st.markdown("### 🌐 Cross-Domain Applications")
        
        domain_icons = {"health": "🏥", "finance": "💹", "agriculture": "🌾"}
        
        d1, d2, d3 = st.columns(3)
        domains = list(cross_domain.items())
        cols = [d1, d2, d3]
        
        for idx, (domain, impact) in enumerate(domains[:3]):
            icon = domain_icons.get(domain.lower(), "🔗")
            with cols[idx]:
                st.markdown(f"""
                <div class="custom-card">
                    <div class="card-title">{icon} {domain.capitalize()}</div>
                    <div class="card-body">{impact}</div>
                </div>
                """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Explainability Section
    explanation = data.get("explanation", {})
    if explanation:
        with st.expander("🧠 **Understanding the AI's Reasoning**", expanded=False):
            st.markdown(f"**Summary:** {explanation.get('summary', 'No summary available.')}")
            st.markdown(f"**Confidence Level:** `{explanation.get('confidence', 'N/A')}`")
            
            assumptions = explanation.get("assumptions", [])
            if assumptions:
                st.markdown("**Key Assumptions:**")
                for assumption in assumptions:
                    st.markdown(f"- {assumption}")
    
    # =========================================================================
    # FEEDBACK SECTION - User Feedback Loop
    # =========================================================================
    st.markdown("---")
    st.markdown("### 🔄 Refine Your Learning Path")
    st.markdown("""
    <div style="background: rgba(88, 166, 255, 0.1); border: 1px solid #30363D; border-radius: 8px; padding: 1rem; margin-bottom: 1rem;">
        <span style="color: #58A6FF;">💡</span>
        <span style="color: #8B949E;">Help the AI improve your path! Rate each skill below to get a personalized refinement.</span>
    </div>
    """, unsafe_allow_html=True)
    
    # Collect all skills from the path
    all_skills = []
    all_skills.extend([(s, "Foundation") for s in roadmap.get("foundation", [])])
    all_skills.extend([(s, "Growth") for s in roadmap.get("intermediate", [])])
    all_skills.extend([(s, "Mastery") for s in roadmap.get("advanced", [])])
    
    if all_skills:
        with st.expander("📝 **Rate Skills & Provide Feedback**", expanded=True):
            st.markdown("##### Rate each skill:")
            st.markdown("""
            <div style="font-size: 0.85rem; color: #8B949E; margin-bottom: 1rem;">
                <span style="color: #3FB950;">✅ Keep</span> • 
                <span style="color: #58A6FF;">📚 Already Know</span> • 
                <span style="color: #F0883E;">⚡ Too Advanced</span> • 
                <span style="color: #F85149;">❌ Not Relevant</span> • 
                <span style="color: #A371F7;">🔍 Want More</span>
            </div>
            """, unsafe_allow_html=True)
            
            # Create columns for skill ratings
            feedback_options = ["✅ Keep", "📚 Already Know", "⚡ Too Advanced", "❌ Not Relevant", "🔍 Want More"]
            feedback_map = {
                "✅ Keep": "keep",
                "📚 Already Know": "already_known",
                "⚡ Too Advanced": "too_advanced",
                "❌ Not Relevant": "not_relevant",
                "🔍 Want More": "want_more"
            }
            
            # Group by stage
            for stage_name, stage_color in [("Foundation", "#58A6FF"), ("Growth", "#A371F7"), ("Mastery", "#3FB950")]:
                stage_skills = [s for s, stg in all_skills if stg == stage_name]
                if stage_skills:
                    st.markdown(f'<div style="color: {stage_color}; font-weight: 600; margin-top: 0.5rem;">🔹 {stage_name}</div>', unsafe_allow_html=True)
                    
                    for skill in stage_skills:
                        col1, col2 = st.columns([2, 3])
                        with col1:
                            st.markdown(f"<div style='padding: 0.5rem 0; color: #C9D1D9;'>{skill}</div>", unsafe_allow_html=True)
                        with col2:
                            current_rating = st.session_state.skill_feedback.get(skill, "✅ Keep")
                            rating = st.selectbox(
                                f"Rate {skill}",
                                options=feedback_options,
                                index=feedback_options.index(current_rating) if current_rating in feedback_options else 0,
                                key=f"feedback_{skill}",
                                label_visibility="collapsed"
                            )
                            st.session_state.skill_feedback[skill] = rating
            
            st.markdown("---")
            st.markdown("##### General Feedback (Optional):")
            general_feedback = st.text_area(
                "Share any additional thoughts or preferences",
                placeholder="e.g., I prefer practical projects over theory, I'm interested in cloud deployment...",
                height=100,
                key="general_feedback_text"
            )
            
            # Refine Button
            st.markdown("<br>", unsafe_allow_html=True)
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.button("🔄 Refine My Learning Path", use_container_width=True, key="refine_btn"):
                    # Prepare feedback data
                    skill_ratings = {}
                    for skill, rating in st.session_state.skill_feedback.items():
                        mapped_rating = feedback_map.get(rating, "keep")
                        if mapped_rating != "keep":  # Only include non-keep ratings
                            skill_ratings[skill] = mapped_rating
                    
                    feedback_data = {
                        "skill_feedback": skill_ratings,
                        "general_feedback": general_feedback
                    }
                    
                    original_goal = st.session_state.user_profile.get("goal", "")
                    
                    with st.spinner("🔄 AI is refining your path based on feedback..."):
                        result = call_refine_api(learning_plan, feedback_data, original_goal)
                    
                    if result["success"]:
                        st.session_state.refined_path = result["data"].get("refined_path", {})
                        st.session_state.feedback_changes = result["data"].get("changes_made", [])
                        st.success("✅ Learning path refined successfully!")
                        st.rerun()
                    else:
                        st.error(f"❌ Error: {result['error']}")
    
    # Display Refined Path if Available
    if st.session_state.refined_path:
        st.markdown("---")
        st.markdown("### ✨ Refined Learning Path")
        
        # Show changes made
        if st.session_state.feedback_changes:
            st.markdown("""
            <div style="background: rgba(63, 185, 80, 0.1); border: 1px solid #3FB950; border-radius: 8px; padding: 1rem; margin-bottom: 1rem;">
                <div style="color: #3FB950; font-weight: 600; margin-bottom: 0.5rem;">📋 Changes Made:</div>
            """, unsafe_allow_html=True)
            for change in st.session_state.feedback_changes:
                st.markdown(f"<div style='color: #8B949E; padding-left: 1rem;'>• {change}</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
        
        # Display refined path
        refined = st.session_state.refined_path
        r1, r2, r3 = st.columns(3)
        
        with r1:
            refined_foundation = refined.get("foundation", [])
            skills_list = "".join([f"<li>{s}</li>" for s in refined_foundation]) if refined_foundation else "<li>No changes</li>"
            st.markdown(f"""
            <div class="custom-card stage-foundation">
                <div class="card-title">🏗️ Foundation (Refined)</div>
                <div class="card-body">
                    <ul style="padding-left: 1.2rem; margin: 0;">{skills_list}</ul>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with r2:
            refined_intermediate = refined.get("intermediate", [])
            skills_list = "".join([f"<li>{s}</li>" for s in refined_intermediate]) if refined_intermediate else "<li>No changes</li>"
            st.markdown(f"""
            <div class="custom-card stage-growth">
                <div class="card-title">🚀 Growth (Refined)</div>
                <div class="card-body">
                    <ul style="padding-left: 1.2rem; margin: 0;">{skills_list}</ul>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with r3:
            refined_advanced = refined.get("advanced", [])
            skills_list = "".join([f"<li>{s}</li>" for s in refined_advanced]) if refined_advanced else "<li>No changes</li>"
            st.markdown(f"""
            <div class="custom-card stage-mastery">
                <div class="card-title">🏆 Mastery (Refined)</div>
                <div class="card-body">
                    <ul style="padding-left: 1.2rem; margin: 0;">{skills_list}</ul>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Button to apply refined path
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("✅ Apply Refined Path", use_container_width=True, key="apply_refined"):
                # Update the main response with refined path
                st.session_state.api_response["learning_plan"]["learning_path"] = st.session_state.refined_path
                st.session_state.refined_path = None
                st.session_state.feedback_changes = []
                st.session_state.skill_feedback = {}
                st.success("✅ Refined path applied!")
                st.rerun()
    
    # Raw Data (Debug)
    with st.expander("📋 **View Raw API Response**", expanded=False):
        st.json(data)

# =============================================================================
# PAGE: ABOUT
# =============================================================================
def render_about_page():
    st.markdown("# 📖 About AURA-Learn")
    
    st.markdown("""
    **AURA** (Agentic Universal Reasoning Architecture) is an advanced AI system 
    designed to revolutionize personalized learning. Unlike traditional AI chatbots, 
    AURA uses a multi-agent architecture where specialized components collaborate 
    to produce grounded, explainable, and actionable learning paths.
    """)
    
    st.markdown("---")
    
    st.markdown("## 🏗️ System Architecture")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### Core Agents
        
        **🎯 Orchestrator Agent**
        - Interprets user goals
        - Coordinates other agents
        - Manages the planning lifecycle
        
        **📚 Education Agent**
        - Retrieves from Knowledge Base
        - Extracts & validates skills
        - Structures learning paths
        """)
    
    with col2:
        st.markdown("""
        ### Support Agents
        
        **🌐 Cross-Domain Agent**
        - Maps skills to other fields
        - Identifies transfer opportunities
        - Expands impact analysis
        
        **🔍 Explainability Agent**
        - Documents reasoning
        - Reveals assumptions
        - Provides confidence scores
        """)
    
    st.markdown("---")
    
    st.markdown("## 🛠️ Technology Stack")
    
    t1, t2, t3 = st.columns(3)
    
    with t1:
        st.markdown("""
        **Backend**
        - Python / FastAPI
        - AWS Bedrock
        - Amazon Nova Premier
        """)
    
    with t2:
        st.markdown("""
        **Knowledge**
        - Bedrock Knowledge Bases
        - OpenSearch Serverless
        - Vector Embeddings
        """)
    
    with t3:
        st.markdown("""
        **Frontend**
        - Streamlit
        - Custom CSS
        - Responsive Design
        """)
    
    st.markdown("---")
    st.info("🏆 Built for GenAI Hackathon 2026 • AWS Bedrock Category")

# =============================================================================
# PAGE: LEARN (Interactive Learning)
# =============================================================================
def render_learn_page():
    st.markdown("# 📚 Interactive Learning")
    
    # Get roadmap data
    roadmap = {}
    all_skills = []
    if st.session_state.api_response:
        learning_plan = st.session_state.api_response.get("learning_plan", {})
        roadmap = learning_plan.get("learning_path", {})
        all_skills.extend(roadmap.get("foundation", []))
        all_skills.extend(roadmap.get("intermediate", []))
        all_skills.extend(roadmap.get("advanced", []))
    
    # Two-column layout: Main content (left) | Learning Path (right)
    main_col, path_col = st.columns([7, 3])
    
    # ===== RIGHT COLUMN: Learning Path Reference =====
    with path_col:
        st.markdown("### 🗺️ Your Roadmap")
        
        if roadmap and any([roadmap.get("foundation"), roadmap.get("intermediate"), roadmap.get("advanced")]):
            # Foundation
            st.markdown("""
            <div style="background: rgba(88, 166, 255, 0.1); border-left: 3px solid #58A6FF; padding: 12px; margin-bottom: 12px; border-radius: 0 8px 8px 0;">
                <div style="color: #58A6FF; font-weight: 600; margin-bottom: 8px;">🏗️ Foundation</div>
            """, unsafe_allow_html=True)
            for skill in roadmap.get("foundation", [])[:5]:
                selected = "→ " if skill == st.session_state.selected_skill else ""
                color = "#58A6FF" if skill == st.session_state.selected_skill else "#8B949E"
                st.markdown(f'<div style="color: {color}; font-size: 0.85rem; padding: 2px 0;">{selected}{skill}</div>', unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Intermediate
            st.markdown("""
            <div style="background: rgba(163, 113, 247, 0.1); border-left: 3px solid #A371F7; padding: 12px; margin-bottom: 12px; border-radius: 0 8px 8px 0;">
                <div style="color: #A371F7; font-weight: 600; margin-bottom: 8px;">🚀 Growth</div>
            """, unsafe_allow_html=True)
            for skill in roadmap.get("intermediate", [])[:5]:
                selected = "→ " if skill == st.session_state.selected_skill else ""
                color = "#A371F7" if skill == st.session_state.selected_skill else "#8B949E"
                st.markdown(f'<div style="color: {color}; font-size: 0.85rem; padding: 2px 0;">{selected}{skill}</div>', unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Advanced
            st.markdown("""
            <div style="background: rgba(63, 185, 80, 0.1); border-left: 3px solid #3FB950; padding: 12px; margin-bottom: 12px; border-radius: 0 8px 8px 0;">
                <div style="color: #3FB950; font-weight: 600; margin-bottom: 8px;">🏆 Mastery</div>
            """, unsafe_allow_html=True)
            for skill in roadmap.get("advanced", [])[:5]:
                selected = "→ " if skill == st.session_state.selected_skill else ""
                color = "#3FB950" if skill == st.session_state.selected_skill else "#8B949E"
                st.markdown(f'<div style="color: {color}; font-size: 0.85rem; padding: 2px 0;">{selected}{skill}</div>', unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
        else:
            st.info("Generate a learning path first to see your roadmap here.")
            if st.button("Go to Planner", key="goto_planner"):
                st.session_state.current_page = "planner"
                st.rerun()
    
    # ===== LEFT COLUMN: Main Learning Area =====
    with main_col:
        st.markdown("Select a skill from your roadmap or enter any topic to learn.")
        st.markdown("---")
        
        # # Skill Selection Buttons
        # if all_skills:
        #     st.markdown("#### 🎯 Quick Select")
        #     cols = st.columns(4)
        #     for idx, skill in enumerate(all_skills[:8]):
        #         with cols[idx % 4]:
        #             btn_type = "primary" if skill == st.session_state.selected_skill else "secondary"
        #             if st.button(skill, key=f"skill_{idx}", use_container_width=True):
        #                 st.session_state.selected_skill = skill
        #                 st.session_state.learning_content = None
        #                 st.rerun()
        
        # Manual Entry
        st.markdown("#### ✏️ Enter Topic")
        input_col1, input_col2, input_col3 = st.columns([3, 1, 1])
        with input_col1:
            manual_skill = st.text_input("Topic", placeholder="e.g., REST APIs, Docker", label_visibility="collapsed")
        with input_col2:
            user_level = st.selectbox("Level", ["Beginner", "Intermediate", "Advanced"], label_visibility="collapsed")
        with input_col3:
            generate_clicked = st.button("📖 Learn", use_container_width=True)
        
        if generate_clicked:
            skill_to_learn = manual_skill.strip() if manual_skill.strip() else st.session_state.selected_skill
            if skill_to_learn:
                st.session_state.selected_skill = skill_to_learn
                with st.spinner(f"Generating lesson for '{skill_to_learn}'..."):
                    result = call_learn_api(skill_to_learn, user_level)
                    if result["success"]:
                        st.session_state.learning_content = result["data"]
                    else:
                        st.error(f"Error: {result['error']}")
            else:
                st.warning("Please select or enter a skill first.")
        
        # ===== Display Structured Learning Content =====
        if st.session_state.learning_content:
            content_data = st.session_state.learning_content
            if content_data.get("status") == "success":
                st.markdown("---")
                st.markdown(f"## 📖 {content_data.get('skill')}")
                st.caption(f"Level: {content_data.get('level')}")
                
                raw_content = content_data.get('content', '')
                
                # Parse and display structured content
                # The LLM returns sections like **Introduction**, **Key Concepts**, etc.
                sections = {
                    "Introduction": {"icon": "📌", "color": "#58A6FF"},
                    "Key Concepts": {"icon": "🔑", "color": "#A371F7"},
                    "Practical Example": {"icon": "💻", "color": "#3FB950"},
                    "Common Mistakes": {"icon": "⚠️", "color": "#F85149"},
                    "Next Steps": {"icon": "🚀", "color": "#F778BA"}
                }
                
                # Try to split content by sections
                current_section = None
                section_content = {}
                lines = raw_content.split('\n')
                
                for line in lines:
                    # Check if line is a section header
                    found_section = False
                    for section_name in sections.keys():
                        if section_name.lower() in line.lower() and ('**' in line or '#' in line or line.strip().startswith(str(list(sections.keys()).index(section_name) + 1))):
                            current_section = section_name
                            section_content[current_section] = []
                            found_section = True
                            break
                    
                    if not found_section and current_section:
                        section_content[current_section].append(line)
                
                # Display each section in a styled card
                if section_content:
                    for section_name, config in sections.items():
                        if section_name in section_content and section_content[section_name]:
                            content_text = '\n'.join(section_content[section_name]).strip()
                            if content_text:
                                # Apply professional formatting
                                formatted_content = format_lesson_content(content_text)
                                st.markdown(f"""
                                <div style="background: linear-gradient(135deg, rgba(22, 27, 34, 0.95) 0%, rgba(13, 17, 23, 0.95) 100%); border: 1px solid #30363D; border-left: 4px solid {config['color']}; border-radius: 8px; padding: 20px; margin: 16px 0; box-shadow: 0 4px 12px rgba(0,0,0,0.3);">
                                    <div style="color: {config['color']}; font-weight: 700; font-size: 1.1rem; margin-bottom: 14px; display: flex; align-items: center; gap: 8px;">
                                        <span style="font-size: 1.3rem;">{config['icon']}</span> {section_name}
                                    </div>
                                    <div style="color: #C9D1D9; line-height: 1.8; font-size: 0.95rem;">
                                        {formatted_content}
                                    </div>
                                </div>
                                """, unsafe_allow_html=True)
                else:
                    # Fallback: Display raw content with formatting
                    formatted_raw = format_lesson_content(raw_content)
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, rgba(22, 27, 34, 0.95) 0%, rgba(13, 17, 23, 0.95) 100%); border: 1px solid #30363D; border-radius: 8px; padding: 20px; margin: 16px 0; box-shadow: 0 4px 12px rgba(0,0,0,0.3);">
                        <div style="color: #C9D1D9; line-height: 1.8; font-size: 0.95rem;">
                            {formatted_raw}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
            else:
                st.error(content_data.get("message", "Failed to generate content."))
        
        st.markdown("---")
        
        # ===== Chat with AI Tutor =====
        st.markdown("### 💬 Ask Your AI Tutor")
        
        chat_col1, chat_col2 = st.columns([5, 1])
        with chat_col1:
            chat_input = st.text_input(
                "Question",
                placeholder="Ask anything about the topic...",
                key="chat_input",
                label_visibility="collapsed"
            )
        with chat_col2:
            send_clicked = st.button("Send", key="send_chat", use_container_width=True)
        
        if send_clicked and chat_input.strip():
            st.session_state.chat_messages.append({"role": "user", "content": chat_input})
            skill_context = st.session_state.selected_skill or "General programming"
            with st.spinner("AURA is thinking..."):
                result = call_chat_api(chat_input, skill_context)
                if result["success"]:
                    ai_response = result["data"].get("response", "I couldn't generate a response.")
                    st.session_state.chat_messages.append({"role": "assistant", "content": ai_response})
                else:
                    st.session_state.chat_messages.append({"role": "assistant", "content": f"Error: {result['error']}"})
            st.rerun()
        
        # Display chat history
        if st.session_state.chat_messages:
            for msg in st.session_state.chat_messages:
                if msg["role"] == "user":
                    st.markdown(f"""
                    <div style="background: #1E3A5F; padding: 12px; border-radius: 8px; margin: 8px 0;">
                        <strong style="color: #58A6FF;">You:</strong>
                        <p style="color: #F0F6FC; margin: 4px 0 0 0;">{msg['content']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div style="background: #2D1B4E; padding: 12px; border-radius: 8px; margin: 8px 0;">
                        <strong style="color: #A371F7;">AURA:</strong>
                        <p style="color: #F0F6FC; margin: 4px 0 0 0; white-space: pre-wrap;">{msg['content']}</p>
                    </div>
                    """, unsafe_allow_html=True)
            
            if st.button("Clear Chat", key="clear_chat"):
                st.session_state.chat_messages = []
                st.rerun()


# =============================================================================
# MAIN ROUTER
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
