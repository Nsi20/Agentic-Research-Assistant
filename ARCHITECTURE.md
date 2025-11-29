# Architecture Documentation

## System Overview

The Agentic Research Assistant is a hierarchical multi-agent system designed to automate the research process from data gathering to report generation.

## Core Components

### 1. Agent Layer (`src/agents.py`)

#### Project Manager
- **Role**: Senior Project Manager
- **Responsibilities**: 
  - Orchestrates the entire research workflow
  - Delegates tasks to specialized agents
  - Ensures quality control and timely delivery
- **Capabilities**: Can delegate to all other agents

#### Research Agent
- **Role**: Deep-Dive Research Analyst
- **Responsibilities**:
  - Conducts web searches using Tavily API
  - Gathers comprehensive information
  - Stores findings in the knowledge base
- **Tools**: 
  - `research_tool` (Tavily Search)
  - `store_knowledge_tool` (Vector DB)

#### Analysis Agent
- **Role**: Data Synthesis Expert
- **Responsibilities**:
  - Queries the knowledge base
  - Synthesizes information into structured insights
  - Creates thesis-driven arguments
- **Tools**:
  - `retrieval_tool` (Vector DB Query)

#### Verification Agent
- **Role**: Fact and Citation Verifier
- **Responsibilities**:
  - Verifies key claims
  - Ensures source accuracy
  - Validates citations
- **Tools**:
  - `citation_tool` (Tavily Search)

#### Report Writer
- **Role**: Professional Report Writer
- **Responsibilities**:
  - Drafts polished research reports
  - Formats content in Markdown
  - Saves reports to disk
- **Tools**:
  - `file_writer_tool` (File I/O)

### 2. Task Layer (`src/tasks.py`)

Tasks define the work each agent must complete:

1. **Research Task**: Gather comprehensive information
2. **Analysis Task**: Synthesize insights from knowledge base
3. **Verification Task**: Verify 3-5 key claims
4. **Reporting Task**: Generate final Markdown report

Tasks are executed sequentially with context passing between them.

### 3. Tools Layer (`src/tools.py`)

#### External Tools
- **TavilySearchTool**: AI-powered web search
  - Research variant: max 8 results
  - Citation variant: max 3 results

- **FileWriterTool**: Saves reports to disk

#### Custom Tools

##### Knowledge Storage Tool
```python
class StoreKnowledgeTool(BaseTool):
    """Stores research findings in ChromaDB vector database"""
    - Input: Content string
    - Output: Confirmation message
    - Storage: ChromaDB with HuggingFace embeddings
```

##### Retrieval Tool
```python
class RetrievalToolClass(BaseTool):
    """Retrieves relevant information from knowledge base"""
    - Input: Query string
    - Output: Top 5 relevant documents
    - Method: Semantic similarity search
```

### 4. Vector Database

**Technology**: ChromaDB with HuggingFace Embeddings

**Configuration**:
- Model: `all-MiniLM-L6-v2`
- Collection: `research_knowledge_base`
- Persistence: `./chroma_db/`

**Purpose**:
- Stores research findings
- Enables semantic search
- Provides context for analysis

### 5. User Interface Layer

#### Streamlit App (`app.py`)

**Features**:
- Model selection dropdown
- Knowledge base management
- Real-time progress tracking
- Log capture and display
- Report preview and download

**Key Functions**:
- `get_resources()`: Lazy-loads tools and vector store (cached)
- `clear_db()`: Clears the knowledge base
- Stdout capture: Displays agent logs in UI

## Data Flow

```
User Input (Topic)
    ↓
Project Manager
    ↓
Research Agent → Web Search → Store in Vector DB
    ↓
Analysis Agent → Query Vector DB → Synthesize Insights
    ↓
Verification Agent → Verify Claims → Check Sources
    ↓
Report Writer → Generate Report → Save to File
    ↓
Display in Streamlit UI
```

## Process Flow

### Hierarchical Process

CrewAI's hierarchical process means:
1. Project Manager receives the overall goal
2. Manager delegates tasks to appropriate agents
3. Agents execute tasks sequentially
4. Results flow back to the manager
5. Manager ensures quality and completeness

### Task Dependencies

```
research_task (no dependencies)
    ↓
analysis_task (context: research_task)
    ↓
verification_task (context: analysis_task)
    ↓
reporting_task (context: analysis_task, verification_task)
```

## Technology Stack

### Core Frameworks
- **CrewAI**: Multi-agent orchestration
- **LangChain**: LLM application framework
- **Streamlit**: Web interface

### LLM Providers
- **Groq**: Fast inference (Llama, Mixtral)
- **OpenAI**: GPT-4 models

### Storage
- **ChromaDB**: Vector database
- **HuggingFace**: Embeddings model

### APIs
- **Tavily**: AI-powered web search

## Design Decisions

### 1. Lazy Loading
Resources (embeddings, vector store) are initialized on-demand using `@st.cache_resource` to prevent blocking Streamlit startup.

### 2. Hierarchical Organization
Using a Project Manager agent allows for:
- Better task coordination
- Quality control
- Flexible delegation

### 3. RAG Architecture
Combining web search with vector storage enables:
- Comprehensive research
- Efficient information retrieval
- Context-aware analysis

### 4. Separation of Concerns
- Agents: Define roles and capabilities
- Tasks: Define work to be done
- Tools: Provide functionality
- UI: Handle user interaction

## Scalability Considerations

### Current Limitations
- Single-threaded execution
- Local vector database
- Rate limits on free API tiers

### Future Enhancements
- Parallel task execution
- Cloud-based vector store
- Caching layer for API calls
- Multi-topic research sessions
- Export to multiple formats (PDF, DOCX)

## Security Considerations

- API keys stored in `.env` file (not committed to git)
- No user authentication (local use only)
- File writes restricted to project directory
- Input sanitization for file names
