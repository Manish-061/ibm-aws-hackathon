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
    
    # Submit Button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        generate_clicked = st.button(
            "✨ Generate My Learning Path",
            use_container_width=True,
            key="generate_btn"
        )
    
    # Handle Form Submission
    if generate_clicked:
        if not goal.strip():
            st.error("⚠️ Please enter a learning objective.")
            return
        
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
# MAIN ROUTER
# =============================================================================
if st.session_state.current_page == "home":
    render_home_page()
elif st.session_state.current_page == "planner":
    render_planner_page()
elif st.session_state.current_page == "about":
    render_about_page()
else:
    render_home_page()
