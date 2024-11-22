# Contributing to Grami AI 🤝

## Welcome Contributors! 

Grami AI is an open-source project that thrives on community collaboration. We welcome contributions from developers, researchers, and AI enthusiasts worldwide.

## 🌟 Our Vision

To create a flexible, powerful async AI agent framework that empowers developers to build intelligent solutions with ease.

## 🚀 How to Contribute

### 1. Code Contributions

#### Setting Up Your Environment
```bash
# Fork the repository
git clone https://github.com/your-username/grami-ai.git
cd grami-ai

# Create a virtual environment
python -m venv venv
source venv/bin/activate

# Install development dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

#### Development Workflow
1. Create a new branch
```bash
git checkout -b feature/your-feature-name
```

2. Make your changes
- Follow PEP 8 style guidelines
- Write comprehensive docstrings
- Add type hints
- Include unit tests

3. Run checks before committing
```bash
# Run linters
ruff check .

# Run type checking
mypy grami_ai

# Run tests
pytest tests/
```

### 2. Types of Contributions

We welcome:
- Bug fixes
- New features
- Documentation improvements
- Tool implementations
- Performance optimizations
- Test coverage enhancements

### 3. Contribution Areas

#### 🧩 Tool Development
- Create new async tools
- Improve existing tool implementations
- Add support for new platforms/services

#### 🌐 LLM Provider Integration
- Add support for new language models
- Improve existing provider implementations
- Create provider-specific optimizations

#### 📚 Documentation
- Improve README
- Create tutorials and examples
- Write API documentation

### 4. Submission Process

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Write tests
5. Ensure all checks pass
6. Submit a Pull Request

### 5. Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Collaborate openly
- Prioritize community needs

## 🏆 Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Recognized in release notes
- Potentially invited to core team discussions

## 📞 Contact

- Open an issue for bugs/suggestions
- Join our Discord community
- Email: contributors@grami-ai.org

## 🔒 Security

If you discover a security vulnerability:
1. Do NOT open a public issue
2. Email security@grami-ai.org
3. Provide detailed information
4. Expect a response within 48 hours

## 💡 Feature Requests

Have an idea? 
1. Check existing issues
2. Open a new issue with:
   - Clear description
   - Use case
   - Potential implementation approach

Thank you for helping make Grami AI amazing! 🚀
