# Contributing to GRAMI-AI 🤝

## 🌟 Welcome Contributors!

GRAMI-AI is an open-source AI agent framework developed by YAFATek Solutions. We're excited to have you contribute to our project and help shape the future of AI-powered solutions!

## 🎯 Our Vision

To create a flexible, powerful async AI agent framework that:
- Empowers developers to build intelligent solutions
- Provides modular, extensible architecture
- Supports multiple LLM providers
- Enables seamless integration of AI tools

## 🚀 Ways to Contribute

### 1. Code Contributions
- Implement new features
- Fix bugs
- Improve documentation
- Enhance performance
- Add new LLM providers
- Create additional tools

### 2. Non-Code Contributions
- Report bugs
- Suggest improvements
- Write tutorials
- Improve documentation
- Share use cases
- Provide feedback

## 🛠 Development Setup

### Prerequisites
- Python 3.9+
- Git
- Virtual environment support

### Environment Setup
```bash
# Clone the repository
git clone https://github.com/YAFATek/grami-ai.git
cd grami-ai

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

## 🧪 Development Workflow

### 1. Find an Issue
- Check [GitHub Issues](https://github.com/YAFATek/grami-ai/issues)
- Look for "good first issue" or "help wanted" labels

### 2. Fork and Branch
```bash
# Fork on GitHub
# Clone your fork
git clone https://github.com/your-username/grami-ai.git
cd grami-ai

# Create a descriptive branch
git checkout -b feature/add-new-llm-provider
```

### 3. Coding Guidelines
- Follow PEP 8 style guide
- Use type hints
- Write comprehensive docstrings
- Maintain async programming patterns
- Add unit tests for new functionality

### 4. Code Checks
```bash
# Run linters
ruff check .

# Type checking
mypy grami_ai

# Run tests
pytest tests/

# Check test coverage
coverage run -m pytest
coverage report
```

### 5. Commit and Push
```bash
# Stage changes
git add .

# Commit with descriptive message
git commit -m "Add new LLM provider: X with async support"

# Push to your fork
git push origin feature/add-new-llm-provider
```

### 6. Create Pull Request
- Open a PR against the `main` branch
- Describe changes thoroughly
- Link related issues
- Pass all CI checks

## 📋 Contribution Types

### 1. Bug Reports
- Use GitHub Issues
- Provide detailed description
- Include reproduction steps
- Share error logs and environment details

### 2. Feature Requests
- Explain the use case
- Describe proposed implementation
- Discuss potential impact

### 3. Documentation
- Improve docstrings
- Update README
- Create tutorials and examples
- Translate documentation

### 4. Performance Improvements
- Optimize async operations
- Reduce memory consumption
- Improve tool execution speed

## 🤝 Code of Conduct

1. Be respectful and inclusive
2. Provide constructive feedback
3. Collaborate openly
4. Prioritize community well-being

## 💡 Review Process

- PRs reviewed by maintainers
- Automated CI checks
- Code quality assessment
- Performance and security evaluation

## 🏆 Recognition

Contributors will be:
- Credited in documentation
- Featured in release notes
- Considered for future opportunities

## 📞 Contact

- Email: contribute@yafatek.com
- Discord: [GRAMI-AI Community](https://discord.gg/your-discord-link)
- GitHub Discussions

## 📄 License

By contributing, you agree to license your contributions under the MIT License.

---

🌈 Thank you for helping make GRAMI-AI better!
