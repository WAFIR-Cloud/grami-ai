# Grami AI Framework

## Overview

Grami AI is a flexible, multi-agent AI framework designed for advanced WebSocket communication and intelligent content generation. Built with an async-first approach, the framework provides a modular and extensible architecture for creating sophisticated AI-powered applications.

## 🚀 Key Features

- **Async-First Design**: Leveraging Python's async capabilities for high-performance operations
- **Modular Tool System**: Easily extensible tool-based architecture
- **WebSocket Communication**: Robust, real-time communication interface
- **Content Generation**: AI-powered content creation for multiple platforms
- **Flexible Configuration**: Minimal setup, environment-variable driven

## 🛠 Installation

### Prerequisites
- Python 3.12+
- pip
- Redis (for backend memory management)

### Setup
```bash
# Clone the repository
git clone https://github.com/yourusername/grami-ai.git
cd grami-ai

# Create a virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## 🏃 Quick Start

### Running the Framework

```bash
# Run Growth Manager and Client
./run_grami.py

# Or using Python
python3 run_grami.py
```

## 📦 Core Components

### Tools
- **Content Generation Tool**: Create social media content across platforms
- **Web Search Tool**: Perform comprehensive web searches
- **Extensible Tool Registry**: Add and manage custom tools easily

### Agents
- **AsyncAgent**: Base agent for async operations
- **Growth Manager**: Coordinate AI-driven growth strategies

## 🔧 Configuration

Configuration is managed through environment variables:

- `GOOGLE_SEARCH_API_KEY`: Google Custom Search API key
- `GOOGLE_SEARCH_ENGINE_ID`: Google Custom Search Engine ID
- Additional platform-specific credentials as needed

## 📝 Example: Creating a Tool

```python
from grami_ai.tools.base import AsyncBaseTool, ToolMetadata, ToolCategory

class MyCustomTool(AsyncBaseTool):
    def __init__(self):
        metadata = ToolMetadata(
            name="my_custom_tool",
            description="A custom tool for specific tasks",
            category=ToolCategory.CUSTOM
        )
        super().__init__(metadata=metadata)
    
    async def generate(self, **kwargs):
        # Implement your tool's logic here
        pass
```

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

## 📞 Contact

Your Name - your.email@example.com

Project Link: [https://github.com/yourusername/grami-ai](https://github.com/yourusername/grami-ai)