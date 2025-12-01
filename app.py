import streamlit as st
import os
import sys
import io
import time
from contextlib import redirect_stdout
from dotenv import load_dotenv
from crewai import Crew, Process
from src.agents import ResearchAgents
from src.tasks import ResearchTasks
from src.tools import initialize_tools, clear_db, get_db_path

# Load environment variables
load_dotenv()

# Page Config
st.set_page_config(
    page_title="Agentic Research Assistant",
    page_icon="🕵️‍♂️",
    layout="wide"
)

# Title and Description
st.title("🕵️‍♂️ Agentic Research Assistant")
st.markdown("An autonomous multi-agent system that conducts deep, structured research and synthesizes citable reports.")

# Initialize Tools (Lazy Load)
@st.cache_resource
def get_resources():
    return initialize_tools()

# Load resources once
resources = get_resources()

# Sidebar Configuration
with st.sidebar:
    st.header("Configuration")
    
    # Model Selection - only show available models based on API keys
    current_model = os.getenv("LLM_MODEL", "groq/llama-3.1-8b-instant")
    
    # Build available models list based on API keys
    model_options = []
    if os.getenv("GROQ_API_KEY"):
        model_options.extend([
            "groq/llama-3.1-8b-instant",
            "groq/llama3-70b-8192",
            "groq/mixtral-8x7b-32768",
        ])
    if os.getenv("OPENAI_API_KEY"):
        model_options.extend([
            "openai/gpt-4o",
            "openai/gpt-4-turbo"
        ])
    if os.getenv("GOOGLE_API_KEY"):
        model_options.extend([
            "gemini/gemini-1.5-flash",
            "gemini/gemini-1.5-pro",
        ])
    
    # Fallback if no API keys configured
    if not model_options:
        st.warning("⚠️ No API keys configured! Please set GROQ_API_KEY, OPENAI_API_KEY, or GOOGLE_API_KEY in your .env file")
        model_options = ["groq/llama-3.1-8b-instant"]  # Default fallback
    
    # Add current model if not in options
    if current_model not in model_options:
        model_options.insert(0, current_model)
        
    selected_model = st.selectbox(
        "Select LLM Model",
        options=model_options,
        index=model_options.index(current_model) if current_model in model_options else 0
    )
    
    # Update env var for this session (Note: this affects the process env)
    os.environ["LLM_MODEL"] = selected_model
    
    st.divider()
    
    # Clear DB Toggle
    clear_db_toggle = st.checkbox("Clear Knowledge Base before run?", value=True)
    
    if st.button("Clear Database Now"):
        clear_db(resources['vector_store'])
        st.success("Database cleared!")

# Main Input
topic = st.text_input("Enter Research Topic:", placeholder="e.g., The Future of Quantum Computing")

if st.button("Start Research"):
    if not topic:
        st.warning("Please enter a topic first.")
    else:
        # Create a placeholder for logs/status
        status_container = st.container()
        
        with status_container:
            st.info(f"Starting research on: **{topic}**")
            
            # 0. Clear DB if requested
            if clear_db_toggle:
                clear_db(resources['vector_store'])
                st.write("✅ Knowledge Base cleared.")
            
            # 1. Instantiate Agents
            with st.spinner("Initializing Agents..."):
                agents = ResearchAgents(resources)
                project_manager = agents.project_manager()
                researcher = agents.research_agent()
                analyst = agents.analysis_agent()
                writer = agents.reporter_agent()
                verifier = agents.citations_agent()
            
            # 2. Instantiate Tasks
            tasks = ResearchTasks()
            
            # Generate dynamic filename
            timestamp = time.strftime("%Y%m%d-%H%M%S")
            safe_topic = "".join([c for c in topic if c.isalnum() or c in (' ', '-', '_')]).strip().replace(' ', '_')
            report_file = f"report_{safe_topic}_{timestamp}.md"
            
            task_research = tasks.research_task(researcher, topic)
            task_analysis = tasks.analysis_task(analyst, context=[task_research])
            task_verification = tasks.verification_task(verifier, context=[task_analysis])
            task_reporting = tasks.reporting_task(writer, context=[task_analysis, task_verification], output_file=report_file)
            
            # 3. Create Crew
            crew = Crew(
                agents=[researcher, analyst, verifier, writer],
                tasks=[task_research, task_analysis, task_verification, task_reporting],
                process=Process.hierarchical,
                manager_agent=project_manager,
                verbose=True
            )
            
            # 4. Kickoff with progress tracking and log capture
            st.write("🚀 **Crew started!**")
            
            # Create expandable section for live logs
            log_expander = st.expander("📋 View Agent Activity Logs", expanded=True)
            log_container = log_expander.empty()
                
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            try:
                # Capture stdout to display in Streamlit
                captured_output = io.StringIO()
                
                # Update status
                status_text.text("🔍 Research phase in progress...")
                progress_bar.progress(25)
                
                # Kickoff the crew with output capture
                with redirect_stdout(captured_output):
                    result = crew.kickoff()
                
                # Display captured logs
                logs = captured_output.getvalue()
                if logs:
                    log_container.code(logs, language="text")
                else:
                    log_container.info("No detailed logs captured. Check terminal for verbose output.")
                
                # Update progress
                progress_bar.progress(100)
                status_text.text("✅ All tasks completed!")
                
                st.success("Research Completed!")
                
                st.subheader("📄 Final Report")
                st.markdown(result)
                
                # Download Button
                st.download_button(
                    label="📥 Download Report",
                    data=str(result),
                    file_name=report_file,
                    mime="text/markdown"
                )
                
                # Show the generated file path
                st.info(f"Report saved to: `{report_file}`")
                
            except Exception as e:
                progress_bar.empty()
                status_text.empty()
                st.error(f"❌ An error occurred: {e}")
                
                # Show more detailed error info
                with st.expander("🔍 Error Details"):
                    st.code(str(e))


st.divider()
st.caption("Powered by CrewAI, LangChain, and Streamlit")
