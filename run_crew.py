import os
from dotenv import load_dotenv
from crewai import Crew, Process
from src.agents import ResearchAgents
from src.tools import clear_db

# Load environment variables
load_dotenv()

# Import tasks
from src.tasks import ResearchTasks

def main():
    # 0. Clear DB for a fresh start
    clear_db()

    # 1. Instantiate Agents
    agents = ResearchAgents()
    project_manager = agents.project_manager()
    researcher = agents.research_agent()
    analyst = agents.analysis_agent()
    writer = agents.reporter_agent()
    verifier = agents.citations_agent()

    # 2. Instantiate Tasks
    tasks = ResearchTasks()

    topic = input("Enter the research topic: ")
    if not topic:
        topic = "The Future of AI Agents in 2025"

    print(f"\nStarting research on: {topic}\n")

    # Create specific tasks
    # Note: We need to pass the agents to the tasks
    task_research = tasks.research_task(researcher, topic)
    task_analysis = tasks.analysis_task(analyst, context=[task_research])
    task_verification = tasks.verification_task(verifier, context=[task_analysis])
    task_reporting = tasks.reporting_task(writer, context=[task_analysis, task_verification])

    # 3. Create Crew
    crew = Crew(
        agents=[
            researcher,
            analyst,
            verifier,
            writer
        ],
        tasks=[
            task_research,
            task_analysis,
            task_verification,
            task_reporting
        ],
        process=Process.hierarchical, # Project Manager oversees the process
        manager_agent=project_manager,
        verbose=True
    )

    # 4. Kickoff
    result = crew.kickoff()
    
    print("\n\n########################")
    print("## HERE IS THE RESULT ##")
    print("########################\n")
    print(result)

if __name__ == "__main__":
    main()
