
import sys
import os

# Add project root to path
sys.path.append(os.getcwd())

from src.tools import initialize_tools
from src.agents import ResearchAgents

def verify():
    print("Initializing tools...")
    try:
        tools = initialize_tools()
        print("Tools initialized successfully.")
    except Exception as e:
        print(f"Failed to initialize tools: {e}")
        return

    print("Initializing agents...")
    try:
        agents = ResearchAgents(tools)
        pm = agents.project_manager()
        print(f"Project Manager initialized: {pm.role}")
    except Exception as e:
        print(f"Failed to initialize agents: {e}")
        return

    print("Verification successful!")

if __name__ == "__main__":
    verify()
