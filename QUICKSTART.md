# Quick Reference Guide

## Installation

```bash
# Clone and setup
git clone <repo-url>
cd Agentic-Research-Assistant
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt

# Configure
cp .env.example .env
# Edit .env with your API keys
```

## Running the App

### Streamlit UI (Recommended)
```bash
.venv\Scripts\streamlit.exe run app.py
```
Then open: http://localhost:8501

### Command Line
```bash
python run_crew.py
```

## Common Commands

### Verify Setup
```bash
python verify_setup.py
```

### Clear Knowledge Base
```python
from src.tools import initialize_tools, clear_db
tools = initialize_tools()
clear_db(tools['vector_store'])
```

### Install New Package
```bash
pip install package-name
pip freeze > requirements.txt
```

## API Keys

Get your API keys from:
- **Groq**: https://console.groq.com/
- **Tavily**: https://tavily.com/
- **OpenAI**: https://platform.openai.com/ (optional)

## Supported Models

### Groq (Free)
- `groq/llama-3.1-8b-instant` ⚡ Fastest
- `groq/llama3-70b-8192` 🧠 Smarter
- `groq/mixtral-8x7b-32768` 🎯 Best

### OpenAI (Paid)
- `openai/gpt-4o` 🚀 Latest
- `openai/gpt-4-turbo` 💪 Powerful

## File Structure

```
├── app.py              # Streamlit UI
├── run_crew.py         # CLI
├── src/
│   ├── agents.py       # Agent definitions
│   ├── tasks.py        # Task definitions
│   └── tools.py        # Tools & utilities
├── .env                # API keys (create this)
└── requirements.txt    # Dependencies
```

## Troubleshooting

### App won't start
```bash
# Make sure you're in venv
.venv\Scripts\activate
# Reinstall dependencies
pip install -r requirements.txt
```

### Rate limit error
- Wait 30 seconds
- Switch to different model
- Upgrade API tier

### Module not found
```bash
# Use venv's streamlit
.venv\Scripts\streamlit.exe run app.py
```

### No output in UI
- Check "Agent Activity Logs" section
- Check terminal for verbose logs
- Ensure stdout capture is working

## Quick Tips

✅ **DO**:
- Use virtual environment
- Keep API keys in `.env`
- Clear DB between unrelated topics
- Monitor rate limits
- Check generated reports

❌ **DON'T**:
- Commit `.env` file
- Run without activating venv
- Use same DB for different topics
- Ignore rate limit warnings

## Keyboard Shortcuts (Streamlit)

- `R` - Rerun app
- `C` - Clear cache
- `Ctrl+C` - Stop server

## Environment Variables

```env
# Required
GROQ_API_KEY=gsk_...
TAVILY_API_KEY=tvly_...

# Optional
OPENAI_API_KEY=sk_...
LLM_MODEL=groq/llama-3.1-8b-instant
```

## Example Research Topics

- "The impact of AI on healthcare"
- "Sustainable energy solutions"
- "Future of quantum computing"
- "Blockchain in supply chain"
- "Climate change mitigation strategies"

## Output Files

Reports saved as:
```
report_<topic>_<timestamp>.md
```

Example:
```
report_Quantum_Computing_20241129-183045.md
```

## Performance Tips

1. **First run**: Downloads model (~90MB)
2. **Subsequent runs**: Uses cached model
3. **Clear cache**: Delete `chroma_db/` folder
4. **Faster model**: Use `llama-3.1-8b-instant`
5. **Better quality**: Use `mixtral-8x7b-32768`

## Getting Help

1. Check [README.md](README.md)
2. Check [ARCHITECTURE.md](ARCHITECTURE.md)
3. Check [API.md](API.md)
4. Open an issue on GitHub

## Useful Links

- **CrewAI Docs**: https://docs.crewai.com/
- **LangChain Docs**: https://python.langchain.com/
- **Streamlit Docs**: https://docs.streamlit.io/
- **Groq Console**: https://console.groq.com/
- **Tavily Docs**: https://docs.tavily.com/

## Version Info

Check versions:
```bash
python --version
pip list | grep crewai
pip list | grep langchain
pip list | grep streamlit
```

## Updates

Update dependencies:
```bash
pip install --upgrade -r requirements.txt
```

## Backup

Backup knowledge base:
```bash
# Copy chroma_db folder
cp -r chroma_db chroma_db_backup
```

## Clean Install

```bash
# Remove venv
rm -rf .venv

# Remove cache
rm -rf __pycache__ src/__pycache__

# Reinstall
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

---

**Need more help?** See full documentation in README.md
