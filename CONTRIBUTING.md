# 🤝 Contributing to GRAMI AI

First off, thank you for considering contributing to GRAMI AI! It's people like you that make GRAMI AI such a great tool.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Process](#development-process)
- [Pull Request Process](#pull-request-process)
- [Style Guidelines](#style-guidelines)
- [Testing](#testing)
- [Documentation](#documentation)
- [Community](#community)

## 📜 Code of Conduct

This project and everyone participating in it is governed by our [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

## 🚀 Getting Started

1. Fork the repository
2. Clone your fork:
```bash
git clone https://github.com/yourusername/grami-ai.git
cd grami-ai
```

3. Set up development environment:
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -e ".[dev,test,docs]"
```

4. Create a branch:
```bash
git checkout -b feature/your-feature-name
```

## 💻 Development Process

1. **Pick an Issue**
   - Look for issues labeled `good first issue` or `help wanted`
   - Comment on the issue to let others know you're working on it
   - Ask questions if anything is unclear

2. **Make Changes**
   - Write clean, maintainable code
   - Follow our [style guidelines](#style-guidelines)
   - Add tests for new functionality
   - Update documentation as needed

3. **Commit Changes**
   - Use meaningful commit messages
   - Reference issue numbers in commits
   - Keep commits focused and atomic

4. **Update Your Branch**
```bash
git fetch origin
git rebase origin/main
```

## 🔄 Pull Request Process

1. **Create Pull Request**
   - Use our PR template
   - Fill in all required sections
   - Link related issues

2. **PR Requirements**
   - [ ] Tests pass
   - [ ] Code follows style guidelines
   - [ ] Documentation updated
   - [ ] Changelog updated
   - [ ] Version bumped (if applicable)

3. **Review Process**
   - Address reviewer comments
   - Keep PR updated with main branch
   - Be responsive to feedback

## 🎨 Style Guidelines

### Python Code Style

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- Use [Black](https://github.com/psf/black) for formatting
- Use type hints
- Maximum line length: 88 characters
- Use descriptive variable names

### Example:
```python
from typing import List, Optional

async def process_data(
    input_data: List[str],
    max_items: Optional[int] = None
) -> dict:
    """Process input data and return results.
    
    Args:
        input_data: List of strings to process
        max_items: Optional limit on items to process
        
    Returns:
        Dictionary containing processed results
    """
    result = {}
    for item in input_data[:max_items]:
        result[item] = await self._process_item(item)
    return result
```

### Documentation Style

- Use Google-style docstrings
- Keep documentation up to date
- Include examples where helpful
- Document both success and error cases

## 🧪 Testing

1. **Running Tests**
```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_agents.py

# Run with coverage
pytest --cov=grami_ai
```

2. **Writing Tests**
```python
import pytest
from grami_ai import BaseAgent

@pytest.mark.asyncio
async def test_agent_initialization():
    agent = BaseAgent()
    await agent.initialize()
    assert agent.is_initialized
    assert len(agent.tools) == 0
```

## 📚 Documentation

1. **Building Docs**
```bash
# Install docs dependencies
pip install -e ".[docs]"

# Build documentation
cd docs
make html
```

2. **Documentation Guidelines**
- Keep API documentation up to date
- Add examples for new features
- Update quickstart guide as needed
- Include performance considerations

## 👥 Community

- Join our [Discord](https://discord.gg/grami-ai)
- Follow us on [Twitter](https://twitter.com/grami_ai)
- Read our [blog](https://blog.grami-ai.org)

## 🎯 Where to Contribute

1. **Code**
   - Fix bugs
   - Add features
   - Improve performance
   - Write tests

2. **Documentation**
   - Fix typos
   - Add examples
   - Clarify explanations
   - Translate content

3. **Community**
   - Answer questions
   - Review PRs
   - Write blog posts
   - Give talks

## 🏆 Recognition

Contributors will be:
- Added to CONTRIBUTORS.md
- Mentioned in release notes
- Given credit in documentation

## ❓ Questions?

- Open a [Discussion](https://github.com/yourusername/grami-ai/discussions)
- Ask in our [Discord](https://discord.gg/grami-ai)
- Email: support@grami-ai.org

Thank you for contributing to GRAMI AI! 🙏
