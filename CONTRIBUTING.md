# Contributing to Agentic Research Assistant

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## Getting Started

1. **Fork the repository**
2. **Clone your fork**
   ```bash
   git clone https://github.com/your-username/Agentic-Research-Assistant.git
   cd Agentic-Research-Assistant
   ```

3. **Set up development environment**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   pip install -r requirements.txt
   ```

4. **Create a branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Development Guidelines

### Code Style

- Follow PEP 8 style guide
- Use meaningful variable and function names
- Add docstrings to all functions and classes
- Keep functions focused and single-purpose
- Maximum line length: 100 characters

### Example:

```python
def create_research_task(agent: Agent, topic: str) -> Task:
    """
    Create a research task for the given agent and topic.
    
    Args:
        agent: The agent to assign the task to
        topic: The research topic to investigate
        
    Returns:
        Task: A configured research task instance
    """
    return Task(
        description=f"Gather comprehensive information on '{topic}'.",
        expected_output="Complete research findings with citations.",
        agent=agent
    )
```

### Project Structure

```
src/
├── agents.py      # Agent definitions
├── tasks.py       # Task definitions
└── tools.py       # Custom tools and utilities

app.py             # Streamlit UI
run_crew.py        # CLI interface
```

### Adding New Agents

1. Add agent method to `ResearchAgents` class in `src/agents.py`
2. Define the agent's role, goal, and backstory
3. Assign appropriate tools
4. Update documentation

Example:
```python
def new_agent(self):
    return Agent(
        role="Agent Role",
        goal="What the agent should achieve",
        backstory="Agent's background and expertise",
        llm=llm,
        tools=[self.tools['relevant_tool']],
        verbose=True,
        allow_delegation=False
    )
```

### Adding New Tasks

1. Add task method to `ResearchTasks` class in `src/tasks.py`
2. Define clear description and expected output
3. Set up task dependencies via context
4. Update documentation

Example:
```python
def new_task(self, agent, context=None):
    return Task(
        description="Clear description of what to do",
        expected_output="What the output should look like",
        agent=agent,
        context=context
    )
```

### Adding New Tools

1. Create tool class in `src/tools.py`
2. Inherit from `BaseTool`
3. Define name, description, and args_schema
4. Implement `_run` method
5. Add to `initialize_tools()` function

Example:
```python
from crewai.tools import BaseTool
from pydantic import BaseModel, Field

class MyToolInput(BaseModel):
    query: str = Field(description="Input description")

class MyTool(BaseTool):
    name: str = "My Tool Name"
    description: str = "What this tool does"
    args_schema: type[BaseModel] = MyToolInput
    
    def _run(self, query: str) -> str:
        # Tool implementation
        return "Result"
```

## Testing

### Manual Testing

1. Run the verification script:
   ```bash
   python verify_setup.py
   ```

2. Test the Streamlit UI:
   ```bash
   streamlit run app.py
   ```

3. Test with a simple research topic:
   - Enter: "Artificial Intelligence"
   - Verify all agents execute
   - Check report generation

### Test Checklist

- [ ] All agents initialize correctly
- [ ] Tools load without errors
- [ ] Research task completes
- [ ] Analysis task uses knowledge base
- [ ] Verification task runs
- [ ] Report is generated and saved
- [ ] Streamlit UI displays correctly
- [ ] No deprecation warnings
- [ ] Error handling works

## Submitting Changes

### Commit Messages

Use clear, descriptive commit messages:

```
feat: Add new summarization agent
fix: Resolve rate limit handling in research tool
docs: Update API documentation
refactor: Simplify tool initialization
test: Add unit tests for agents
```

Prefixes:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `refactor`: Code refactoring
- `test`: Adding tests
- `chore`: Maintenance tasks

### Pull Request Process

1. **Update documentation** if needed
2. **Test your changes** thoroughly
3. **Update CHANGELOG.md** with your changes
4. **Create pull request** with clear description:
   - What changed
   - Why it changed
   - How to test it

### Pull Request Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Refactoring

## Testing
How to test these changes

## Checklist
- [ ] Code follows style guidelines
- [ ] Documentation updated
- [ ] Tests pass
- [ ] CHANGELOG.md updated
```

## Feature Requests

### Suggesting Features

1. Check existing issues first
2. Open a new issue with:
   - Clear title
   - Detailed description
   - Use cases
   - Potential implementation approach

### Feature Ideas

Some areas for improvement:
- Additional agent types (summarizer, fact-checker, etc.)
- Support for more LLM providers
- Export to PDF/DOCX
- Multi-language support
- Parallel task execution
- Cloud vector database integration
- User authentication
- Research history tracking

## Bug Reports

### Reporting Bugs

Include:
1. **Description**: What happened vs. what should happen
2. **Steps to reproduce**
3. **Environment**:
   - OS version
   - Python version
   - Package versions
4. **Error messages**: Full stack trace
5. **Screenshots**: If UI-related

### Bug Report Template

```markdown
## Bug Description
Clear description of the bug

## Steps to Reproduce
1. Step one
2. Step two
3. Step three

## Expected Behavior
What should happen

## Actual Behavior
What actually happened

## Environment
- OS: Windows 11
- Python: 3.11.5
- CrewAI: 0.x.x

## Error Messages
```
Paste error messages here
```

## Screenshots
If applicable
```

## Code Review

### Review Checklist

When reviewing PRs:
- [ ] Code is readable and well-documented
- [ ] No unnecessary complexity
- [ ] Error handling is appropriate
- [ ] No hardcoded values (use config/env vars)
- [ ] Performance considerations addressed
- [ ] Security implications considered

## Questions?

- Open an issue for questions
- Tag with `question` label
- Be specific and provide context

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing! 🎉
