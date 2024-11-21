# 🤖 Grami AI: Async AI Agent Framework

## 🌟 Overview

Grami AI is a cutting-edge, flexible Python framework for building intelligent, asynchronous AI agents with comprehensive Language Model (LLM) integration.

## 🚀 Key Features

- 🔄 Fully Asynchronous Design
- 🧩 Modular Architecture
- 🔒 Thread-Safe Operations
- 📦 Multiple Backend Support
- 🛠 Extensible Tool Ecosystem

## 📦 Installation

```bash
pip install grami-ai
```

## 🛠 Tools Ecosystem

### Base Tools

Grami AI provides a robust set of async tools for various operations:

#### Calculator Tool
```python
from grami_ai.tools import CalculatorTool

async def calculate():
    calculator = CalculatorTool()
    result = await calculator.execute('2 + 3 * 4')  # Returns 14.0
```

#### JSON Parser Tool
```python
from grami_ai.tools import JSONParserTool

async def parse_json():
    json_tool = JSONParserTool()
    parsed = await json_tool.execute('{"name": "John"}')
    filtered = await json_tool.execute(
        '{"name": "John", "age": 30}', 
        operation='transform', 
        filter_keys=['name']
    )
```

#### String Manipulation Tool
```python
from grami_ai.tools import StringManipulationTool

async def manipulate_string():
    string_tool = StringManipulationTool()
    
    # Clean text
    cleaned = await string_tool.execute("  Hello   World!  ")
    
    # Count words
    word_count = await string_tool.execute("Text", operation='count_words')
    
    # Reverse text
    reversed_text = await string_tool.execute("Hello", operation='reverse')
    
    # Capitalize text
    capitalized = await string_tool.execute(
        "hello world", 
        operation='capitalize', 
        mode='all'
    )
```

#### Web Scraper Tool
```python
from grami_ai.tools import WebScraperTool

async def scrape_web():
    web_tool = WebScraperTool()
    
    # Fetch content
    content = await web_tool.execute('https://example.com')
    
    # Parse text
    parsed_text = await web_tool.execute(
        'https://example.com', 
        operation='parse'
    )
```

### Memory Providers

#### In-Memory Memory
```python
from grami_ai.memory import AsyncInMemoryMemory

async def use_memory():
    memory = AsyncInMemoryMemory(max_size=100)
    await memory.add_item('conversation_1', {'role': 'user', 'content': 'Hello'})
    items = await memory.get_items('conversation_1')
```

#### Redis Memory
```python
from grami_ai.memory import AsyncRedisMemory

async def use_redis_memory():
    memory = AsyncRedisMemory(redis_url='redis://localhost:6379')
    await memory.add_item('conversation_1', {'role': 'user', 'content': 'Hello'})
    items = await memory.get_items('conversation_1')
```

## 📋 Requirements

- Python 3.8+
- asyncio
- aioredis (optional)
- aiohttp (optional)
- beautifulsoup4 (optional)

## 🔧 Development

### Setup
```bash
git clone https://github.com/grami-ai/framework.git
cd grami-ai
pip install -e .[dev]
```

### Running Tests
```bash
pytest
```

## 🤝 Contributing

We welcome contributions! Please see our contribution guidelines.

## 📄 License

MIT License

## 🌐 Project Links

- Documentation: [GitHub README](https://github.com/grami-ai/framework/blob/main/README.md)
- Source Code: [GitHub Repository](https://github.com/grami-ai/framework)
- Issue Tracker: [GitHub Issues](https://github.com/grami-ai/framework/issues)

## 💡 Future Roadmap

- Expand LLM provider implementations
- Enhance tool ecosystem
- Develop more memory backends
- Improve documentation
- Add comprehensive testing
- Performance optimization
- More example use cases
