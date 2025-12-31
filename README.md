# 🚀 AI-Verse

**An Agentic Career Development Assistant powered by Multi-Agent Architecture**

AI-Verse is an intelligent career development platform that uses a multi-agent system to analyze your resume, identify market opportunities, create personalized learning roadmaps, and autonomously assist with job applications. Built with LangGraph and powered by Google Gemini AI.

---

## 📋 Table of Contents

- [Features](#-features)
- [Architecture](#-architecture)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Usage](#-usage)
- [Project Structure](#-project-structure)
- [Agents](#-agents)
- [Tools](#-tools)
- [Testing](#-testing)
- [Technology Stack](#-technology-stack)
- [Documentation](#-documentation)
- [Contributing](#-contributing)
- [License](#-license)

---

## ✨ Features

- **🤖 Multi-Agent System**: Five specialized agents working in harmony
- **📄 Resume Analysis**: Intelligent parsing and skill extraction from PDF resumes
- **📊 Market Intelligence**: Real-time opportunity discovery from Reddit and other sources
- **🗺️ Personalized Roadmaps**: AI-generated learning paths tailored to your profile
- **⚡ Autonomous Applications**: Executive agent handles application processes
- **🔄 Adaptive Learning**: Critic reflector learns from rejections and updates strategies
- **🎨 Modern UI**: Beautiful Streamlit-based web interface

---

## 🏗️ Architecture

AI-Verse uses a **LangGraph-based workflow** where specialized agents collaborate:

```
User Resume → Profiler → Market Analyst → Roadmap Planner → Executive Agent
                                                                    ↓
                                                          Critic Reflector (Feedback Loop)
```

### System Flow

1. **Ingestion**: Profiler parses resume and identifies skills, experience, and gaps
2. **Market Analysis**: Market Strategist scans live job listings and trends
3. **Planning**: Roadmap Planner creates personalized learning sprints
4. **Execution**: Executive Agent identifies opportunities and drafts applications
5. **Reflection**: Critic Reflector processes feedback and adapts strategy

For detailed architecture diagrams, see [`System_Architecture.md`](System_Architecture.md) and [`process_flow.md`](process_flow.md).

---

## 🚀 Installation

### Prerequisites

- Python 3.13 or higher
- [uv](https://github.com/astral-sh/uv) package manager (recommended)

### Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd AI-Verse
   ```

2. **Install dependencies**
   ```bash
   uv sync
   ```

   Or using pip:
   ```bash
   pip install -e .
   ```

3. **Set up environment variables**
   
   Create a `.env` file in the root directory:
   ```env
   GOOGLE_API_KEY=your_google_api_key_here
   REDDIT_CLIENT_ID=your_reddit_client_id
   REDDIT_CLIENT_SECRET=your_reddit_client_secret
   REDDIT_USER_AGENT=your_reddit_user_agent
   ```

---

## ⚙️ Configuration

### API Keys Required

- **Google API Key**: For Gemini AI model access
  - Get it from [Google AI Studio](https://makersuite.google.com/app/apikey)

- **Reddit API Credentials**: For job opportunity scraping
  - Create an app at [Reddit Apps](https://www.reddit.com/prefs/apps)
  - You'll need:
    - Client ID
    - Client Secret
    - User Agent (format: `platform:app_id:version (by /u/username)`)

---

## 💻 Usage

### Running the Application

1. **Start the Streamlit app**
   ```bash
   streamlit run main.py
   ```

2. **Access the web interface**
   - Open your browser to `http://localhost:8501`

3. **Using the Application**
   - Enter your API credentials in the sidebar
   - Upload your resume (PDF format)
   - Click **"🚀 INITIALIZE ANALYSIS"**
   - View your profile, roadmap, and opportunities
   - Use the feedback loop to simulate rejections and adaptive learning

### Command Line Usage

You can also interact with agents programmatically:

```python
from graph import app
from langgraph.checkpoint.memory import MemorySaver

# Initialize state
initial_state = {
    "file_content": your_resume_file,
    "agent_logs": [],
    "feedback_loop_count": 0
}

# Run the workflow
config = {"configurable": {"thread_id": "1"}}
for event in app.stream(initial_state, config=config):
    print(event)
```

---

## 📁 Project Structure

```
AI-Verse/
├── agents/                  # Multi-agent system components
│   ├── profiler.py         # Resume analysis and profile extraction
│   ├── market_analyst.py   # Market opportunity discovery
│   ├── roadmap_planner.py  # Learning path generation
│   ├── executive_agent.py  # Autonomous application handling
│   └── critic_reflector.py # Feedback analysis and adaptation
│
├── tools/                   # Utility tools and scrapers
│   ├── resume_parser.py    # PDF resume parsing
│   ├── reddit_scraper.py   # Reddit job opportunity scraping
│   ├── linkedin_scraper.py # LinkedIn integration (future)
│   └── application_automator.py # Application automation
│
├── tests/                   # Test suite
│   ├── test_profiler_agent.py
│   ├── test_market_analyst_agent.py
│   ├── test_roadmap_planner_agent.py
│   ├── test_executive_agent.py
│   ├── test_critic_reflector_agent.py
│   └── ...
│
├── frontend/                # UI styling
│   └── style.css           # Custom CSS for Streamlit
│
├── graph.py                # LangGraph workflow definition
├── main.py                 # Streamlit application entry point
├── pyproject.toml          # Project dependencies and metadata
├── System_Architecture.md  # Architecture documentation
└── process_flow.md         # Process flow documentation
```

---

## 🤖 Agents

### 1. **Profiler Agent** (`agents/profiler.py`)
- Parses resume PDFs using `resume_parser` tool
- Extracts skills, experience, and implied interests
- Identifies skill gaps and areas for improvement
- Returns structured user profile JSON

### 2. **Market Analyst Agent** (`agents/market_analyst.py`)
- Scrapes Reddit for job opportunities using keywords
- Ranks opportunities by relevance to user profile
- Uses LLM to analyze and score opportunities
- Returns ranked list of opportunities

### 3. **Roadmap Planner Agent** (`agents/roadmap_planner.py`)
- Creates personalized learning roadmaps
- Bridges skill gaps identified by Profiler
- Incorporates market trends from Market Analyst
- Generates actionable learning sprints

### 4. **Executive Agent** (`agents/executive_agent.py`)
- Identifies best-fit opportunities
- Drafts tailored cover letters
- Handles application processes autonomously
- Manages application workflow

### 5. **Critic Reflector Agent** (`agents/critic_reflector.py`)
- Analyzes rejection feedback
- Extracts actionable insights
- Updates user profile with new priorities
- Triggers adaptive learning cycles

---

## 🛠️ Tools

### Resume Parser (`tools/resume_parser.py`)
- Extracts text from PDF resumes
- Parses structured information
- Returns clean text for LLM processing

### Reddit Scraper (`tools/reddit_scraper.py`)
- Searches Reddit for job opportunities
- Filters by relevance keywords
- Returns structured opportunity data

### LinkedIn Scraper (`tools/linkedin_scraper.py`)
- LinkedIn integration (future feature)
- Job listing discovery
- Company research

### Application Automator (`tools/application_automator.py`)
- Automates application processes
- Form filling and submission
- Follow-up management

---

## 🧪 Testing

Run the test suite:

```bash
# Run all tests
pytest tests/

# Run specific test file
pytest tests/test_profiler_agent.py

# Run with coverage
pytest tests/ --cov=agents --cov=tools
```

### Test Files

- `test_profiler_agent.py` - Tests resume parsing and profile extraction
- `test_market_analyst_agent.py` - Tests opportunity discovery
- `test_roadmap_planner_agent.py` - Tests roadmap generation
- `test_executive_agent.py` - Tests application automation
- `test_critic_reflector_agent.py` - Tests feedback processing
- `test_graph.py` - Tests workflow orchestration

---

## 🛠️ Technology Stack

- **Framework**: [LangGraph](https://github.com/langchain-ai/langgraph) - Multi-agent orchestration
- **LLM**: [Google Gemini](https://ai.google.dev/) - AI model (gemini-2.5-flash)
- **Web Framework**: [Streamlit](https://streamlit.io/) - UI/UX
- **PDF Processing**: [pypdf](https://pypdf.readthedocs.io/) - Resume parsing
- **Reddit API**: [PRAW](https://praw.readthedocs.io/) - Reddit scraping
- **Language**: Python 3.13+
- **Package Manager**: [uv](https://github.com/astral-sh/uv) (recommended)

### Key Dependencies

- `langchain` - LLM framework
- `langchain-google-genai` - Google Gemini integration
- `langgraph` - Multi-agent workflow
- `streamlit` - Web interface
- `praw` - Reddit API client
- `pypdf` - PDF processing

See [`pyproject.toml`](pyproject.toml) for complete dependency list.

---

## 📚 Documentation

- **[System Architecture](System_Architecture.md)** - Detailed architecture diagrams
- **[Process Flow](process_flow.md)** - Workflow and agent interactions
- **Agent Documentation** - See individual agent files for detailed docstrings

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 style guidelines
- Add tests for new features
- Update documentation as needed
- Ensure all tests pass before submitting PR

---

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 🙏 Acknowledgments

- Built with [LangGraph](https://github.com/langchain-ai/langgraph) for agent orchestration
- UI built with [Streamlit](https://streamlit.io/)

---

## 📧 Contact

For questions, issues, or contributions, please open an issue on GitHub.

---

**Version**: 2.0  
**Status**: Active Development 🚀

