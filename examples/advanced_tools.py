import asyncio
from grami_ai.tools import StringManipulationTool, WebScraperTool

async def demonstrate_advanced_tools():
    # String Manipulation Tool Demonstration
    print("🔤 String Manipulation Tool:")
    string_tool = StringManipulationTool()
    
    # Clean text
    cleaned_text = await string_tool.execute("  Hello   World!  ")
    print(f"Cleaned Text: '{cleaned_text}'")
    
    # Count words
    word_count = await string_tool.execute("The quick brown fox", operation='count_words')
    print(f"Word Count: {word_count}")
    
    # Reverse text
    reversed_text = await string_tool.execute("Hello, World!", operation='reverse')
    print(f"Reversed Text: '{reversed_text}'")
    
    # Capitalize text
    capitalized = await string_tool.execute(
        "hello world", 
        operation='capitalize', 
        mode='all'
    )
    print(f"Capitalized Text: '{capitalized}'")
    
    # Web Scraper Tool Demonstration (commented out to avoid network dependency)
    print("\n🌐 Web Scraper Tool:")
    # web_tool = WebScraperTool()
    
    # # Fetch content from a sample website
    # try:
    #     content = await web_tool.execute('https://example.com')
    #     print("Website Content Fetched Successfully")
    #     
    #     # Parse and extract text
    #     parsed_text = await web_tool.execute(
    #         'https://example.com', 
    #         operation='parse'
    #     )
    #     print("Parsed Text (first 100 chars):", parsed_text[:100])
    # except Exception as e:
    #     print(f"Web scraping error: {e}")

if __name__ == "__main__":
    asyncio.run(demonstrate_advanced_tools())
