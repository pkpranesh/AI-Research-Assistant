# AI Research Assistant

A Streamlit-based AI research assistant that uses a LangGraph ReAct agent to search the web and generate concise research reports.

## Features

- Topic-based research workflow
- Real-time web search using DuckDuckGo (`ddgs`)
- Tool-using AI agent with:
  - Web search
  - Calculator
  - Current date tool
- Downloadable research reports from the UI
- Quick-start topic buttons for common AI trends

## Tech Stack

- Python
- Streamlit
- LangGraph
- LangChain (Groq integration)
- DuckDuckGo Search (`ddgs`)

## Project Structure

```text
.
├── research_app.py
└── README.md
```

## Prerequisites

- Python 3.9+
- A Groq API key

## Installation

1. Clone the repository.
2. Create and activate a virtual environment.
3. Install dependencies:

```bash
pip install streamlit langchain-groq langchain-core langgraph ddgs
```

4. Set your Groq API key:

```bash
export GROQ_API_KEY="your_api_key_here"
```

## Run the App

```bash
streamlit run research_app.py
```

Then open the local URL shown in your terminal (usually `http://localhost:8501`).

## How It Works

1. Enter a research topic (or choose a quick topic).
2. The agent searches the web for recent information.
3. The model synthesizes findings into a report.
4. Download the report as a text file.

## Notes

- The app currently defaults to `openai/gpt-oss-120b` via Groq.
- If `GROQ_API_KEY` is not set, the placeholder key in code will not work for real requests.

