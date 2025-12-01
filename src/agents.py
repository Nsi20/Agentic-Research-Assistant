# src/agents.py
import os

from crewai import Agent
from langchain_groq import ChatGroq


def _get_llm():
    """Lazy-load LLM to avoid initialization errors during app startup."""
    model_name = os.getenv("LLM_MODEL", "groq/llama-3.1-8b-instant").replace("groq/", "")
    return ChatGroq(
        model=model_name,
        api_key=os.getenv("GROQ_API_KEY"),
        max_retries=5
    )


class ResearchAgents:
    def __init__(self, tools):
        self.tools = tools

    def project_manager(self):
        return Agent(
            role="Senior Project Manager",
            goal="Orchestrate the research process and ensure the final report is delivered on time.",
            backstory="Leader of a high-performance research crew, expert in delegation and quality control.",
            llm=_get_llm(),
            verbose=True,
            allow_delegation=True,
            max_rpm=10
        )

    def research_agent(self):
        return Agent(
            role="Deep-Dive Research Analyst",
            goal="Gather comprehensive, citable information using web search.",
            backstory="Meticulous analyst responsible for populating the knowledge base.",
            llm=_get_llm(),
            tools=[self.tools['research_tool'], self.tools['store_knowledge_tool']],
            verbose=True,
            allow_delegation=False,
            max_rpm=10
        )

    def analysis_agent(self):
        return Agent(
            role="Data Synthesis Expert",
            goal="Analyze and synthesize stored facts into structured insights.",
            backstory="Brilliant strategist using the retrieval tool to create clear, thesis-driven arguments.",
            llm=_get_llm(),
            tools=[self.tools['retrieval_tool']],
            verbose=True,
            allow_delegation=False,
            max_rpm=10
        )

    def reporter_agent(self):
        return Agent(
            role="Professional Report Writer",
            goal="Draft a polished research report and save it using the file writer tool.",
            backstory="Experienced technical writer transforming analysis into compelling narrative content.",
            llm=_get_llm(),
            tools=[self.tools['file_writer_tool']],
            verbose=True,
            allow_delegation=False,
            max_rpm=10
        )

    def citations_agent(self):
        return Agent(
            role="Fact and Citation Verifier",
            goal="Verify key facts and ensure all sources are accurate and trustworthy.",
            backstory="Final line of defense against misinformation using specialized search tool.",
            llm=_get_llm(),
            tools=[self.tools['citation_tool']],
            verbose=True,
            allow_delegation=False,
            max_rpm=10
        )
