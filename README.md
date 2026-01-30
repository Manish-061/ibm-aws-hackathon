<p align="center">
  <img src="https://img.shields.io/badge/AWS-Bedrock-FF9900?style=for-the-badge&logo=amazon-aws&logoColor=white" alt="AWS Bedrock"/>
  <img src="https://img.shields.io/badge/Amazon-Nova_Premier-232F3E?style=for-the-badge&logo=amazon-aws&logoColor=white" alt="Nova Premier"/>
  <img src="https://img.shields.io/badge/Python-FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI"/>
  <img src="https://img.shields.io/badge/Frontend-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" alt="Streamlit"/>
</p>

<h1 align="center">🎓 AURA-Learn</h1>
<h3 align="center">Agentic Universal Reasoning Architecture for Personalized Learning</h3>

<p align="center">
  <strong>An AI-powered career architect that uses multi-agent collaboration to build personalized, hallucination-free learning roadmaps grounded in verified knowledge.</strong>
</p>

<p align="center">
  <em>Built for GenAI Hackathon 2026 • AWS Bedrock Category</em>
</p>

---

## 🌟 Overview

**AURA-Learn** is an advanced agentic AI system that revolutionizes personalized learning by moving beyond traditional chatbots. Instead of simply answering questions, AURA-Learn uses a **multi-agent architecture** where specialized AI components collaborate to:

- **Interpret user goals** with context-aware understanding
- **Retrieve grounded knowledge** from curated educational content
- **Generate structured learning paths** with proper skill progression
- **Map cross-domain applications** (Health, Finance, Agriculture)
- **Provide transparent explanations** for every recommendation

### 🚫 What Makes This Different from a Chatbot?

| Traditional Chatbot | AURA-Learn |
|---------------------|------------|
| Single-turn responses | Multi-agent orchestration |
| May hallucinate content | RAG-grounded knowledge only |
| No reasoning transparency | Full explainability layer |
| Static recommendations | Adaptive, goal-aware planning |
| Domain-specific | Cross-domain skill transfer |

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                         AURA-Learn System                           │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌─────────────────┐    ┌────────────────────────────────────────┐  │
│  │    Frontend     │    │           Backend (FastAPI)            │  │
│  │   (Streamlit)   │───▶│                                        │ │
│  │                 │    │  ┌──────────────────────────────────┐  │ │
│  │  • Home Page    │    │  │      Orchestrator Agent          │  │ │
│  │  • Planner      │    │  │  (Central planning & coordination)│  │ │
│  │  • Learn        │    │  └─────────────┬────────────────────┘  │ │
│  │  • About        │    │                │                       │ │
│  └─────────────────┘    │  ┌─────────────┴────────────────────┐  │ │
│                         │  │                                   │  │ │
│                         │  │  ┌───────────┐ ┌───────────────┐  │  │ │
│                         │  │  │ Education │ │  Cross-Domain │  │  │ │
│                         │  │  │   Agent   │ │     Agent     │  │  │ │
│                         │  │  │  (RAG)    │ │  (KB Grounded)│  │  │ │
│                         │  │  └───────────┘ └───────────────┘  │  │ │
│                         │  │                                   │  │ │
│                         │  │  ┌──────────────────────────────┐ │  │ │
│                         │  │  │   Explainability Agent       │ │  │ │
│                         │  │  │  (Reasoning transparency)    │ │  │ │
│                         │  │  └──────────────────────────────┘ │  │ │
│                         │  │                                   │  │ │
│                         │  └───────────────────────────────────┘  │ │
│                         │                                        │ │
│                         │  ┌──────────────────────────────────┐  │ │
│                         │  │        AWS Integration           │  │ │
│                         │  │  • Bedrock Client (Nova Premier) │  │ │
│                         │  │  • Knowledge Base Client (RAG)   │  │ │
│                         │  └──────────────────────────────────┘  │ │
│                         └────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 🤖 Agent Roles & Responsibilities

### 🎯 Orchestrator Agent
**Role:** Central planning and coordination  
**Responsibilities:**
- Interprets user goals with context extraction
- Coordinates the execution flow between agents
- Manages the planning lifecycle (plan → act → observe)
- Aggregates outputs into final response

### 📚 Education Agent
**Role:** RAG-powered curriculum design  
**Responsibilities:**
- Retrieves content from AWS Bedrock Knowledge Base
- Validates content relevance against user goals
- Extracts specific technical skills from documents
- Structures learning paths (Foundation → Intermediate → Advanced)

### 🌐 Cross-Domain Agent
**Role:** Skill transfer mapping  
**Responsibilities:**
- Retrieves domain-specific content from Knowledge Base
- Maps educational skills to Health, Finance, and Agriculture
- Generates grounded, factual cross-domain applications
- Uses KB content as primary source (no hallucination)

### 🔍 Explainability Agent
**Role:** Decision transparency  
**Responsibilities:**
- Documents reasoning for every recommendation
- Identifies assumptions made by the system
- Provides confidence scores (High/Medium/Low)
- Enables trust through transparency

### 🔄 Feedback Agent
**Role:** Continuous path refinement  
**Responsibilities:**
- Processes user feedback on skills (already known, too advanced, not relevant, want more)
- Retrieves additional content from KB for topics user wants to explore
- Generates refined learning paths with clear change explanations
- Implements the feedback loop for adaptive learning

---

## 📁 Project Structure

```
auralearn/
├── README.md
├── auralearn-backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                 # FastAPI application entry point
│   │   ├── agents/
│   │   │   ├── orchestrator.py     # Central coordination agent
│   │   │   ├── education_agent.py  # RAG-based learning path generator
│   │   │   ├── cross_domain_agent.py # KB-grounded skill transfer
│   │   │   ├── feedback_agent.py   # User feedback processing & path refinement
│   │   │   └── explainability.py   # Reasoning transparency
│   │   ├── api/
│   │   │   └── routes.py           # API endpoints
│   │   ├── aws/
│   │   │   ├── bedrock_client.py   # Amazon Bedrock LLM integration
│   │   │   └── kb_client.py        # Knowledge Base retrieval
│   │   ├── core/
│   │   │   └── config.py           # Environment configuration
│   │   ├── schemas/                # Request/Response models
│   │   ├── services/               # Business logic services
│   │   └── utils/                  # Helper utilities
│   ├── requirements.txt
│   └── .env                        # AWS credentials (not committed)
└── frontend/
    └── app.py                      # Streamlit application
```

---

## 🛠️ Technology Stack

| Layer | Technology | Purpose |
|-------|------------|---------|
| **LLM** | Amazon Nova Premier | Reasoning, generation, orchestration |
| **Knowledge Base** | AWS Bedrock KB + OpenSearch | Vector storage, semantic retrieval |
| **Backend** | Python + FastAPI | REST API, agent coordination |
| **Frontend** | Streamlit | Interactive web interface |
| **Cloud** | AWS | Bedrock, IAM, OpenSearch Serverless |

---

## 📡 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | System health check |
| `/orchestrate` | POST | Main orchestration endpoint - generates complete learning path |
| `/refine` | POST | Refine learning path based on user feedback |
| `/learn` | POST | Generate educational content for a specific skill |
| `/chat` | POST | Interactive chat with AI tutor |
| `/test-kb` | GET | Test Knowledge Base retrieval |

---

## 🗄️ Knowledge Base Contents

The system uses a curated knowledge base with the following documents:

| File | Purpose |
|------|---------|
| `education_to_health.txt` | Skill transfer mappings for Healthcare domain |
| `education_to_finance.txt` | Skill transfer mappings for Finance domain |
| `education_to_agriculture.txt` | Skill transfer mappings for Agriculture domain |
| `backend_skills_outcomes.txt` | Technical skills and expected outcomes |
| `cross_domain_constraints.txt` | Rules and constraints for domain mapping |

---

## 🚀 Getting Started

### Prerequisites

- Python 3.9+
- AWS Account with Bedrock access
- Bedrock Knowledge Base configured

### 1. Clone the Repository

```bash
git clone https://github.com/Manish-061/ibm-aws-hackathon.git
cd ibm-aws-hackathon
```

### 2. Backend Setup

```bash
cd auralearn-backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
.\venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure Environment

Create a `.env` file in `auralearn-backend/`:

```env
AWS_REGION=us-east-1
BEDROCK_MODEL_ID=us.amazon.nova-premier-v1:0
BEDROCK_KB_ID=your-knowledge-base-id
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
```

### 4. Run the Backend

```bash
python app/main.py
```

Backend will start at `http://localhost:8000`

### 5. Run the Frontend

```bash
cd ../frontend
streamlit run app.py
```

Frontend will start at `http://localhost:8501`

---

## 🎮 Usage Flow

1. **Open the Application** - Navigate to `http://localhost:8501`
2. **Enter Your Profile** - Provide name, qualification, and experience level
3. **Define Your Goal** - Enter what skill or role you want to master
4. **Generate Learning Path** - Click "Generate My Learning Path"
5. **Review Results**:
   - Skills identified from knowledge base
   - Structured learning stages (Foundation → Growth → Mastery)
   - Cross-domain applications (Health, Finance, Agriculture)
   - AI reasoning explanation
6. **Learn Interactively** - Click on any skill to dive deeper
7. **Provide Feedback** - Rate each skill using the feedback options
8. **Refine Path** - Submit feedback to get an AI-refined learning path

---

## 🔄 Feedback Loop Feature

The feedback loop allows you to refine your learning path based on your personal knowledge and preferences.

### How It Works

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│  Initial Path   │───▶│  User Feedback   │───▶│  Refined Path   │
│  Generated      │    │  Collection      │    │  Displayed      │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                              │
                              ▼
                    ┌──────────────────┐
                    │  Feedback Agent  │
                    │  • Process Ratings│
                    │  • Query KB      │
                    │  • Refine Path   │
                    └──────────────────┘
```

### Feedback Options

| Rating | Icon | Action |
|--------|------|--------|
| **Keep** | ✅ | Skill remains in the path (no change) |
| **Already Know** | 📚 | Skill is removed from path completely |
| **Too Advanced** | ⚡ | Skill moves to later stage or prerequisites added |
| **Not Relevant** | ❌ | Skill is removed from path completely |
| **Want More** | 🔍 | Related advanced skills are added from KB |

### Behind the Scenes

1. **Categorization** - User ratings are grouped by action type
2. **KB Retrieval** - For "Want More" topics, additional content is fetched from Knowledge Base
3. **LLM Refinement** - The AI generates a new path following refinement rules
4. **Transparency** - All changes are explained in plain language
5. **Apply Changes** - User can review and apply the refined path

---

## 🔒 Trust & Safety

### Grounding & Hallucination Prevention
- All recommendations come from verified Knowledge Base content
- Education Agent validates content relevance before extraction
- Cross-Domain Agent uses KB as primary source with fallback messages
- Clear indication when knowledge is insufficient

### Explainability
- Every recommendation includes reasoning
- Assumptions are explicitly listed
- Confidence scores provided
- Full decision trace available in raw API response

---

## 📊 Demo Screenshots

### Learning Path Generation
*User enters their goal and receives a personalized, staged learning roadmap*

### Cross-Domain Applications
*Skills are mapped to Health, Finance, and Agriculture using KB-grounded content*

### AI Reasoning
*Full transparency into why recommendations were made*

---

## 🎯 Key Differentiators

| Feature | Implementation |
|---------|---------------|
| **Agentic Architecture** | 5 specialized agents with clear boundaries |
| **Grounded Knowledge** | RAG with AWS Bedrock Knowledge Bases |
| **Cross-Domain Impact** | KB-grounded skill transfer mapping |
| **Full Explainability** | Reasoning, assumptions, and confidence |
| **Feedback Loop** | User-driven path refinement with KB expansion |
| **AWS Native** | 100% AWS services (Bedrock, OpenSearch) |

---

## ⚠️ Known Limitations

1. **Knowledge Scope** - Limited to curated content in Knowledge Base
2. **Latency** - Multi-agent orchestration takes 15-30 seconds
3. **Cold Start** - First request may be slower due to model initialization
4. **Domain Coverage** - Cross-domain limited to Health, Finance, Agriculture

---

## 🔮 Future Roadmap

- [ ] Add progress tracking and completion status
- [x] Implement user feedback loop for path refinement ✅
- [ ] Expand Knowledge Base with more domains
- [ ] Add resource recommendations (courses, books, projects)
- [ ] Implement learning analytics dashboard
- [ ] Enable multi-language support

---

## 📄 License

This project is built for the Agentic AI Hackathon 2026.

---

<p align="center">
  <strong>🏆 Built with ❤️ for Agentic AI Hackathon 2026</strong><br>
  <em>Demonstrating the power of Agentic AI with AWS Bedrock</em>
</p>