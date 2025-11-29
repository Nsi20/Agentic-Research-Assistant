# API Documentation

## Environment Variables

### Required Variables

#### GROQ_API_KEY
- **Type**: String
- **Required**: Yes (if using Groq models)
- **Description**: API key for Groq LLM service
- **Get it**: https://console.groq.com/
- **Example**: `gsk_xxxxxxxxxxxxxxxxxxxxx`

#### TAVILY_API_KEY
- **Type**: String
- **Required**: Yes
- **Description**: API key for Tavily web search
- **Get it**: https://tavily.com/
- **Example**: `tvly-xxxxxxxxxxxxxxxxxxxxx`

### Optional Variables

#### OPENAI_API_KEY
- **Type**: String
- **Required**: No (only if using OpenAI models)
- **Description**: API key for OpenAI GPT models
- **Get it**: https://platform.openai.com/
- **Example**: `sk-xxxxxxxxxxxxxxxxxxxxx`

#### LLM_MODEL
- **Type**: String
- **Required**: No
- **Default**: `groq/llama-3.1-8b-instant`
- **Description**: Default LLM model to use
- **Options**:
  - `groq/llama-3.1-8b-instant`
  - `groq/llama3-70b-8192`
  - `groq/mixtral-8x7b-32768`
  - `openai/gpt-4o`
  - `openai/gpt-4-turbo`

## Python API

### Agents Module (`src/agents.py`)

#### ResearchAgents Class

```python
class ResearchAgents:
    def __init__(self, tools: dict):
        """
        Initialize the research agents with tools.
        
        Args:
            tools (dict): Dictionary containing initialized tools
                - research_tool: TavilySearchTool
                - citation_tool: TavilySearchTool
                - file_writer_tool: FileWriterTool
                - store_knowledge_tool: StoreKnowledgeTool
                - retrieval_tool: RetrievalToolClass
                - vector_store: Chroma instance
                - embeddings: HuggingFaceEmbeddings instance
        """
```

**Methods**:

```python
def project_manager(self) -> Agent:
    """Returns the Project Manager agent"""

def research_agent(self) -> Agent:
    """Returns the Research Agent with search and storage tools"""

def analysis_agent(self) -> Agent:
    """Returns the Analysis Agent with retrieval tool"""

def reporter_agent(self) -> Agent:
    """Returns the Report Writer agent with file writer tool"""

def citations_agent(self) -> Agent:
    """Returns the Citations Verifier agent with citation tool"""
```

### Tasks Module (`src/tasks.py`)

#### ResearchTasks Class

```python
class ResearchTasks:
    def research_task(self, agent: Agent, topic: str) -> Task:
        """
        Create a research task.
        
        Args:
            agent: The agent to assign the task to
            topic: The research topic
            
        Returns:
            Task: Research task instance
        """

    def analysis_task(self, agent: Agent, context: list) -> Task:
        """
        Create an analysis task.
        
        Args:
            agent: The agent to assign the task to
            context: List of previous tasks for context
            
        Returns:
            Task: Analysis task instance
        """

    def verification_task(self, agent: Agent, context: list) -> Task:
        """
        Create a verification task.
        
        Args:
            agent: The agent to assign the task to
            context: List of previous tasks for context
            
        Returns:
            Task: Verification task instance
        """

    def reporting_task(self, agent: Agent, context: list, output_file: str) -> Task:
        """
        Create a reporting task.
        
        Args:
            agent: The agent to assign the task to
            context: List of previous tasks for context
            output_file: Path to save the report
            
        Returns:
            Task: Reporting task instance
        """
```

### Tools Module (`src/tools.py`)

#### Functions

```python
def initialize_tools() -> dict:
    """
    Initialize and return all tools and resources.
    
    Returns:
        dict: Dictionary containing:
            - research_tool: TavilySearchTool (max 8 results)
            - citation_tool: TavilySearchTool (max 3 results)
            - file_writer_tool: FileWriterTool
            - store_knowledge_tool: StoreKnowledgeTool
            - retrieval_tool: RetrievalToolClass
            - vector_store: Chroma instance
            - embeddings: HuggingFaceEmbeddings instance
    """

def clear_db(vector_store: Chroma) -> None:
    """
    Clear the vector database.
    
    Args:
        vector_store: Chroma vector store instance
    """

def get_db_path() -> str:
    """
    Get the database path.
    
    Returns:
        str: Path to the ChromaDB directory
    """
```

#### Custom Tools

##### StoreKnowledgeTool

```python
class StoreKnowledgeTool(BaseTool):
    name: str = "Knowledge Storage Tool"
    description: str = "Stores research findings, facts, and data into the internal vector database."
    
    def _run(self, content: str) -> str:
        """
        Store content in the knowledge base.
        
        Args:
            content: Text content to store
            
        Returns:
            str: Confirmation message
        """
```

##### RetrievalToolClass

```python
class RetrievalToolClass(BaseTool):
    name: str = "Internal Knowledge Retrieval Tool"
    description: str = "Search and retrieve research snippets from the internal knowledge base."
    
    def _run(self, query: str) -> str:
        """
        Retrieve relevant information from knowledge base.
        
        Args:
            query: Search query
            
        Returns:
            str: Concatenated content from top 5 relevant documents
        """
```

## Streamlit API

### Cached Resources

```python
@st.cache_resource
def get_resources() -> dict:
    """
    Get initialized tools and resources (cached).
    
    Returns:
        dict: Tools and resources from initialize_tools()
    """
```

### UI Components

The Streamlit app provides:

- **Sidebar**:
  - Model selection dropdown
  - Clear database checkbox
  - Clear database button

- **Main Area**:
  - Topic input field
  - Start Research button
  - Progress bar
  - Status text
  - Agent activity logs (expandable)
  - Final report display
  - Download button

## CLI Usage

### Using run_crew.py

```python
from src.agents import ResearchAgents
from src.tasks import ResearchTasks
from src.tools import initialize_tools
from crewai import Crew, Process

# Initialize
tools = initialize_tools()
agents = ResearchAgents(tools)
tasks = ResearchTasks()

# Create agents
pm = agents.project_manager()
researcher = agents.research_agent()
analyst = agents.analysis_agent()
writer = agents.reporter_agent()
verifier = agents.citations_agent()

# Create tasks
topic = "Your research topic"
task_research = tasks.research_task(researcher, topic)
task_analysis = tasks.analysis_task(analyst, context=[task_research])
task_verification = tasks.verification_task(verifier, context=[task_analysis])
task_reporting = tasks.reporting_task(
    writer, 
    context=[task_analysis, task_verification],
    output_file="report.md"
)

# Create and run crew
crew = Crew(
    agents=[researcher, analyst, verifier, writer],
    tasks=[task_research, task_analysis, task_verification, task_reporting],
    process=Process.hierarchical,
    manager_agent=pm,
    verbose=True
)

result = crew.kickoff()
print(result)
```

## Rate Limits

### Groq (Free Tier)
- **Tokens per minute**: 6,000 TPM
- **Requests per minute**: Varies by model
- **Solution**: Wait for rate limit reset or upgrade tier

### Tavily (Free Tier)
- **Requests per month**: 1,000
- **Solution**: Monitor usage or upgrade plan

### OpenAI
- Varies by account tier
- Check: https://platform.openai.com/account/limits

## Error Handling

### Common Errors

#### RateLimitError
```python
litellm.RateLimitError: RateLimitError: GroqException
```
**Solution**: Wait 30 seconds or switch models

#### ModuleNotFoundError
```python
ModuleNotFoundError: No module named 'langchain_huggingface'
```
**Solution**: Activate venv and install dependencies

#### API Key Errors
```python
AuthenticationError: Invalid API key
```
**Solution**: Check `.env` file for correct API keys

## Best Practices

1. **Always use virtual environment**
2. **Keep API keys in `.env` file**
3. **Monitor rate limits**
4. **Clear knowledge base between unrelated topics**
5. **Use appropriate model for task complexity**
6. **Check generated reports for accuracy**
