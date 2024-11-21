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

## 🚀 Comprehensive Examples

Grami AI provides rich, real-world example scripts to demonstrate the framework's capabilities:

### 1. 🔬 AI Research Assistant
`examples/ai_research_assistant.py`

A sophisticated research workflow that showcases:
- Async tool composition
- Web scraping
- Text processing
- Memory management
- Complex research automation

```python
async def main():
    research_assistant = AIResearchAssistant()
    research_results = await research_assistant.research_topic(
        "Artificial Intelligence in Scientific Research"
    )
```

### 2. 📊 Data Analysis Pipeline
`examples/data_analysis_pipeline.py`

An advanced data analysis tool demonstrating:
- Stock data retrieval
- Web scraping
- JSON parsing
- Statistical calculations
- Async data processing

```python
async def main():
    pipeline = DataAnalysisPipeline()
    analysis_results = await pipeline.analyze_stock_data('AAPL')
```

### 3. 🌐 Multi-Tool Global Trend Analysis
`examples/multi_tool_workflow.py`

A complex workflow showcasing:
- Parallel topic research
- Async data gathering
- Comprehensive trend analysis
- Tool interaction and synthesis

```python
async def main():
    workflow = MultiToolWorkflow()
    global_trends = await workflow.analyze_global_trends([
        "Artificial Intelligence",
        "Climate Change",
        "Renewable Energy"
    ])
```

### 🖥️ Running Examples

To run the example scripts, ensure you have the necessary dependencies:

```bash
# Install optional dependencies for web scraping
pip install aiohttp beautifulsoup4

# Run specific example scripts
python examples/ai_research_assistant.py
python examples/data_analysis_pipeline.py
python examples/multi_tool_workflow.py
```

**Note**: Some examples involve web scraping and may require:
- Active internet connection
- Handling potential network-related exceptions
- Respecting website terms of service

### 🎓 Learning Paths

These examples demonstrate different aspects of the Grami AI framework:
- **Beginners**: Start with individual tool usage
- **Intermediate**: Explore tool composition
- **Advanced**: Study complex async workflows

### 🚀 Quick Start

1. Clone the repository
2. Install dependencies
3. Explore and run example scripts
4. Modify and adapt to your use cases

```bash
git clone https://github.com/grami-ai/framework.git
cd grami-ai
pip install -e .
python examples/ai_research_assistant.py
```

## 💡 Example Highlights

- **Async-First Design**: Non-blocking, high-performance operations
- **Modular Architecture**: Easily extensible and customizable
- **Tool Composition**: Seamless integration of multiple tools
- **Memory Management**: Efficient context tracking
- **Error Handling**: Robust and informative error management

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
