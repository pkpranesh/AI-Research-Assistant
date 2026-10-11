import streamlit as st
import os
from datetime import datetime
from langchain_groq import ChatGroq
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent
from ddgs import DDGS

# ── Page Config ───────────────────────────────────────────
st.set_page_config(
    page_title = "AI Research Assistant",
    page_icon  = "🔬",
    layout     = "wide"
)

# ── LLM Setup ─────────────────────────────────────────────

# Add:


# Replace LLM setup:
llm = ChatGroq(
    model       = "openai/gpt-oss-120b",  # fast + free
    api_key     = os.getenv("GROQ_API_KEY", "YOUR_GROQ_KEY"),
    temperature = 0.3
)

# ── Tools ─────────────────────────────────────────────────
@tool
def web_search(query: str) -> str:
    """
    Search the web for current information.
    Use for finding facts, news, recent developments.
    Input: search query string
    """
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=4))
        
        if not results:
            return "No results found" 
        
        formatted = []
        for r in results:
            formatted.append(
                f"Title: {r['title']}\n"
                f"Content: {r['body']}\n"
                f"Source: {r['href']}\n"
            )
        return "\n---\n".join(formatted)
    except Exception as e:
        return f"Search error: {e}"

@tool
def calculator(expression: str) -> str:
    """
    Perform mathematical calculations.
    Input: math expression like '15 * 400 / 100'
    """
    try:
        return str(eval(expression))
    except:
        return "Calculation error"

@tool
def get_date(query: str) -> str:
    """Get today's current date."""
    return datetime.now().strftime('%B %d, %Y')

# ── Create Agent ──────────────────────────────────────────
tools = [web_search, calculator, get_date]
agent = create_react_agent(model=llm, tools=tools)

# ── Research Function ─────────────────────────────────────
def research_topic(topic: str) -> str:
    prompt = f"""
    Research this topic thoroughly: {topic}
    
    Please:
    1. Search for current information
    2. Find key facts and statistics  
    3. Identify recent developments
    4. Provide a comprehensive summary
    5. List your sources
    
    Be thorough and accurate.
    """
    
    result = agent.invoke({
        "messages": [HumanMessage(content=prompt)]
    })
    
    return result["messages"][-1].content

# ── UI ────────────────────────────────────────────────────
st.title("🔬 AI Research Assistant")
st.markdown("### Powered by AI Agents + Real Web Search")
st.markdown("---")

# Example topics
st.markdown("**Quick Research Topics:**")
col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("🤖 Latest LLMs"):
        st.session_state.topic = "Latest large language models 2026"
with col2:
    if st.button("📈 AI Job Market"):
        st.session_state.topic = "AI ML engineer job market 2026"
with col3:
    if st.button("🏥 AI in Healthcare"):
        st.session_state.topic = "AI applications in healthcare 2026"
with col4:
    if st.button("🚀 AI Startups"):
        st.session_state.topic = "Top AI startups funded 2026"

st.markdown("---")

# Custom topic input
topic = st.text_input(
    "Or enter your own research topic:",
    value = st.session_state.get('topic', ''),
    placeholder = "e.g. XGBoost vs LightGBM comparison 2026"
)

# Research button
if st.button("🔍 Start Research", type="primary", use_container_width=True):
    if not topic.strip():
        st.error("Please enter a research topic!")
    else:
        with st.spinner(f"🤖 Agent researching: {topic}..."):
            try:
                result = research_topic(topic)
                
                st.markdown("## 📊 Research Results")
                st.markdown(f"**Topic:** {topic}")
                st.markdown(f"**Date:** {datetime.now().strftime('%B %d, %Y')}")
                st.markdown("---")
                st.markdown(result)
                
                # Download button
                st.download_button(
                    label     = "📥 Download Report",
                    data      = f"Topic: {topic}\n\n{result}",
                    file_name = f"research_{topic[:30]}.txt",
                    mime      = "text/plain"
                )
                
            except Exception as e:
                st.error(f"Error: {e}")
                st.info("Gemini may be busy. Please try again!")

# ── Sidebar ───────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🤖 How This Works")
    st.markdown("""
    **AI Agent Pipeline:**
    
    1️⃣ You enter a topic
    
    2️⃣ Agent searches the web
    using DuckDuckGo
    
    3️⃣ Agent reads results
    and extracts key info
    
    4️⃣ Gemini synthesizes
    a comprehensive report
    
    5️⃣ You get accurate,
    current information!
    """)
    
    st.markdown("---")
    st.markdown("**Tech Stack:**")
    st.markdown("🔗 LangGraph Agents")
    st.markdown("🔍 DuckDuckGo Search")
    st.markdown("🤖 Gemini 2.0 Flash")
    st.markdown("🌐 Streamlit")
    st.markdown("---")
    st.markdown("**Built by Pranesh P K**")
    st.markdown("SRM IST | B.Tech ECE | 2026")

st.markdown("---")
st.markdown(
    "<p style='text-align:center; color:gray;'>"
    "AI Research Assistant | LangGraph + DuckDuckGo + Gemini | "
    "Built by Pranesh P K"
    "</p>",
    unsafe_allow_html=True
)