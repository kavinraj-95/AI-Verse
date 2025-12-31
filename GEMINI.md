# Project Overview

This project, "ai-verse," is an AI-powered career development assistant. It's designed to help users achieve their career goals by analyzing their profiles, identifying relevant market trends, creating personalized learning roadmaps, and even automating job applications.

The system is built in Python and leverages the LangChain framework for orchestrating AI agents, with a potential terminal-based user interface using Textual. It appears to be designed to work with local models via Ollama.

## Architecture

The system follows an agent-based architecture where different specialized agents collaborate by reading and writing to a central "Global State."

The key agents are:

*   **Profiler Agent:** Ingests and analyzes the user's resume and online profiles (like GitHub) to build a detailed skills profile.
*   **Market Strategist Agent:** Scrapes job boards and analyzes market trends to identify in-demand skills and opportunities relevant to the user's goals.
*   **Roadmap Planner Agent:** Creates a personalized, actionable roadmap of skills to learn and projects to build.
*   **Executive Agent:** Autonomously searches for and applies to relevant opportunities (jobs, internships, hackathons) on behalf of the user.
*   **Critic Reflector Agent:** Parses feedback from application outcomes (especially rejections) to extract insights and update the user's profile and roadmap.

This entire process is designed as a continuous feedback loop, allowing the system to adapt and refine its strategy over time.

# Building and Running

## Dependencies

The project's dependencies are listed in `pyproject.toml` and managed by `uv`. Key libraries include:
*   `langchain`
*   `langchain-community`
*   `langchain-ollama`
*   `textual`

## Installation

To install the dependencies, you can use `uv`:

```bash
uv pip install -e .
```

## Running the Application

The entry point for the application is likely `main.py`.

```bash
# TODO: Confirm the exact run command.
python main.py
```

## Testing

TODO: Add instructions on how to run tests once they are available.

# Development Conventions

The codebase is structured into several directories:

*   `agents/`: Contains the logic for each individual AI agent.
*   `tools/`: Likely holds utility functions and tools that agents can use (e.g., web scrapers, parsers).
*   `data/`: Intended for storing persistent data, such as the user's profile, memory, and vector stores.

The current source files are mostly placeholders. Development should focus on implementing the logic for each agent as described in the `System_Architecture.md` and `process_flow.md` documents.
