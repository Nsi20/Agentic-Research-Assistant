# src/agents.py
import os

from crewai import Agent
from langchain_groq import ChatGroq

# --- LLM Configuration ---
# CrewAI uses string-based LLM configuration
llm = os.getenv("LLM_MODEL", "groq/llama-3.1-8b-instant")


class ResearchAgents:
    def __init__(self, tools):
        self.tools = tools

    def project_manager(self):
        return Agent(
            role="Senior Project Manager",
            goal="Orchestrate the research process and ensure the final report is delivered on time.",
            backstory="Leader of a high-performance research crew, expert in delegation and quality control.",
            llm=llm,
            verbose=True,
            allow_delegation=True
        )

    def research_agent(self):
        return Agent(
            role="Deep-Dive Research Analyst",
            goal="Gather comprehensive, citable information using web search.",
            backstory="Meticulous analyst responsible for populating the knowledge base.",
            llm=llm,
            tools=[self.tools['research_tool'], self.tools['store_knowledge_tool']],
            verbose=True,
            allow_delegation=False
        )

    def analysis_agent(self):
        return Agent(
            role="Data Synthesis Expert",
            goal="Analyze and synthesize stored facts into structured insights.",
            backstory="Brilliant strategist using the retrieval tool to create clear, thesis-driven arguments.",
            llm=llm,
            tools=[self.tools['retrieval_tool']],
            verbose=True,
            allow_delegation=False
        )

    def reporter_agent(self):
        return Agent(
            role="Professional Report Writer",
            goal="Draft a polished research report and save it using the file writer tool.",
            backstory="Experienced technical writer transforming analysis into compelling narrative content.",
            llm=llm,
            tools=[self.tools['file_writer_tool']],
            verbose=True,
            allow_delegation=False
        )

    def citations_agent(self):
        return Agent(
            role="Fact and Citation Verifier",
            goal="Verify key facts and ensure all sources are accurate and trustworthy.",
            backstory="Final line of defense against misinformation using specialized search tool.",
            llm=llm,
            tools=[self.tools['citation_tool']],
            verbose=True,
            allow_delegation=False
        )
