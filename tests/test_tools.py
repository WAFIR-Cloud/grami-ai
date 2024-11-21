import asyncio
import pytest

from grami_ai.tools import (
    BaseTool, 
    CalculatorTool, 
    JSONParserTool, 
    StringManipulationTool,
    WebScraperTool
)

@pytest.mark.asyncio
class TestTools:
    async def test_calculator_tool(self):
        calculator = CalculatorTool()
        
        # Test basic arithmetic
        assert await calculator.execute('2 + 3') == 5.0
        assert await calculator.execute('4 * 5') == 20.0
        assert await calculator.execute('10 / 2') == 5.0
        
        # Test complex expressions
        assert await calculator.execute('2 + 3 * 4') == 14.0
        
        # Test error handling
        with pytest.raises(ValueError):
            await calculator.execute('2 + a')
        
        with pytest.raises(ValueError):
            await calculator.execute('1 / 0')

    async def test_json_parser_tool(self):
        json_tool = JSONParserTool()
        
        # Test parsing
        parsed = await json_tool.execute('{"name": "John", "age": 30}')
        assert parsed == {"name": "John", "age": 30}
        
        # Test validation
        assert await json_tool.execute('{"test": 123}', operation='validate') is True
        
        # Test invalid JSON
        with pytest.raises(ValueError):
            await json_tool.execute('{invalid json}')
        
        # Test transformation
        transformed = await json_tool.execute(
            '{"name": "John", "age": 30, "city": "New York"}', 
            operation='transform', 
            filter_keys=['name', 'age']
        )
        assert transformed == {"name": "John", "age": 30}

    async def test_base_tool_interface(self):
        class DummyTool(BaseTool):
            def __init__(self):
                super().__init__("dummy", "A dummy tool for testing")
            
            async def execute(self, *args, **kwargs):
                return "Dummy execution"
        
        dummy_tool = DummyTool()
        
        assert dummy_tool.name == "dummy"
        assert dummy_tool.description == "A dummy tool for testing"
        
        result = await dummy_tool.execute()
        assert result == "Dummy execution"

    async def test_string_manipulation_tool(self):
        string_tool = StringManipulationTool()
        
        # Test text cleaning
        cleaned = await string_tool.execute('  Hello   World  ')
        assert cleaned == 'Hello World'
        
        # Test word counting
        word_count = await string_tool.execute('Hello World', operation='count_words')
        assert word_count == 2
        
        # Test text reversal
        reversed_text = await string_tool.execute('Hello', operation='reverse')
        assert reversed_text == 'olleH'
        
        # Test capitalization
        first_cap = await string_tool.execute('hello world', operation='capitalize')
        assert first_cap == 'Hello world'
        
        all_cap = await string_tool.execute('hello world', operation='capitalize', mode='all')
        assert all_cap == 'HELLO WORLD'

    @pytest.mark.skip(reason="Requires network connection and external service")
    async def test_web_scraper_tool(self):
        scraper = WebScraperTool()
        
        # Test fetching content (using a sample website)
        test_url = 'https://example.com'
        content = await scraper.execute(test_url)
        assert isinstance(content, str)
        assert len(content) > 0
        
        # Test parsing content
        parsed_content = await scraper.execute(test_url, operation='parse')
        assert isinstance(parsed_content, str)
        
        # Test element extraction
        extracted = await scraper.execute(
            test_url, 
            operation='extract', 
            selector='p'
        )
        assert isinstance(extracted, list)
        assert len(extracted) > 0
