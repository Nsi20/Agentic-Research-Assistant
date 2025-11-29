# Changelog

All notable changes to the Agentic Research Assistant project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned
- Export reports to PDF and DOCX formats
- Multi-language support
- Research history and session management
- Parallel task execution
- Cloud vector database integration

## [1.1.0] - 2024-11-29

### Added
- Real-time progress tracking in Streamlit UI
- Agent activity log viewer (expandable section)
- Stdout capture to display crew logs in Streamlit
- Enhanced error handling with detailed error messages
- Report file path display after completion
- Improved UI with emojis and better formatting
- Comprehensive documentation (README, ARCHITECTURE, API, CONTRIBUTING)
- Verification script (`verify_setup.py`)

### Changed
- Updated to use `langchain-huggingface` instead of deprecated `langchain-community.embeddings`
- Updated to use `langchain-chroma` instead of deprecated `langchain-community.vectorstores`
- Refactored tools initialization to use lazy loading
- Improved Streamlit app startup performance
- Enhanced download button with emoji

### Fixed
- **Critical**: Fixed Streamlit app not displaying due to blocking imports
- **Critical**: Fixed module not found errors by updating requirements.txt
- Fixed deprecation warnings for HuggingFaceEmbeddings and Chroma
- Fixed crew output not appearing in Streamlit UI
- Improved error messages for rate limit issues

### Technical Details
- Implemented `@st.cache_resource` for tool initialization
- Added dependency injection for agents (tools passed via constructor)
- Refactored `clear_db()` to accept vector_store parameter
- Added `io.StringIO` and `redirect_stdout` for log capture

## [1.0.0] - 2024-11-28

### Added
- Initial release of Agentic Research Assistant
- Multi-agent system with 5 specialized agents:
  - Project Manager (orchestrator)
  - Research Agent (web search)
  - Analysis Agent (synthesis)
  - Verification Agent (fact-checking)
  - Report Writer (documentation)
- Hierarchical task execution with CrewAI
- RAG (Retrieval-Augmented Generation) architecture
- ChromaDB vector database for knowledge storage
- Tavily API integration for web search
- Support for Groq LLMs (Llama, Mixtral)
- Support for OpenAI GPT models
- Streamlit web interface
- CLI interface (`run_crew.py`)
- Environment variable configuration
- Markdown report generation
- Knowledge base management (clear/persist)

### Features
- **Research Tool**: Web search with Tavily (max 8 results)
- **Citation Tool**: Focused search for verification (max 3 results)
- **Storage Tool**: Save findings to vector database
- **Retrieval Tool**: Query knowledge base (top 5 results)
- **File Writer Tool**: Save reports to disk

### Configuration
- Model selection via sidebar
- Knowledge base clear option
- Dynamic report file naming with timestamps
- Configurable LLM model via environment variable

## Project Structure

```
Agentic-Research-Assistant/
├── app.py                 # Streamlit web interface
├── run_crew.py           # CLI interface
├── main.py               # Alternative entry point
├── requirements.txt      # Python dependencies
├── .env                  # Environment variables
├── src/
│   ├── agents.py         # Agent definitions
│   ├── tasks.py          # Task definitions
│   └── tools.py          # Custom tools
├── chroma_db/            # Vector database
└── docs/
    ├── README.md
    ├── ARCHITECTURE.md
    ├── API.md
    ├── CONTRIBUTING.md
    └── CHANGELOG.md
```

## Dependencies

### Core
- crewai
- crewai-tools
- langchain
- langchain-openai
- langchain-groq
- langchain-huggingface
- langchain-chroma

### Tools
- tavily-python
- streamlit
- chromadb

### Utilities
- python-dotenv
- pandas
- numpy

## Known Issues

### Rate Limits
- Groq free tier: 6,000 TPM limit
- Tavily free tier: 1,000 requests/month
- **Workaround**: Wait for reset or upgrade tier

### Logging
- Some verbose logs may still appear in terminal
- **Workaround**: Check both Streamlit UI and terminal

### Performance
- First run downloads HuggingFace model (~90MB)
- Subsequent runs are faster due to caching

## Migration Guide

### From 1.0.0 to 1.1.0

1. **Update dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Update imports** (if using programmatically):
   ```python
   # Old
   from src.agents import ResearchAgents
   agents = ResearchAgents()
   
   # New
   from src.tools import initialize_tools
   from src.agents import ResearchAgents
   tools = initialize_tools()
   agents = ResearchAgents(tools)
   ```

3. **Update clear_db calls**:
   ```python
   # Old
   from src.tools import clear_db
   clear_db()
   
   # New
   from src.tools import initialize_tools, clear_db
   tools = initialize_tools()
   clear_db(tools['vector_store'])
   ```

## Contributors

- Initial development and architecture
- Streamlit UI implementation
- Documentation and testing

## License

This project is licensed under the MIT License - see the LICENSE file for details.

---

For more information, see:
- [README.md](README.md) - Getting started guide
- [ARCHITECTURE.md](ARCHITECTURE.md) - System architecture
- [API.md](API.md) - API documentation
- [CONTRIBUTING.md](CONTRIBUTING.md) - Contribution guidelines
