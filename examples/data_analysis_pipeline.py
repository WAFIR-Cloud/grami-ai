import asyncio
import json
from typing import List, Dict, Any

from grami_ai.memory import AsyncInMemoryMemory
from grami_ai.tools import (
    CalculatorTool, 
    JSONParserTool, 
    StringManipulationTool, 
    WebScraperTool
)

class DataAnalysisPipeline:
    """
    An async data analysis pipeline demonstrating 
    tool composition and memory management
    """
    
    def __init__(self):
        # Initialize async tools and memory
        self.memory = AsyncInMemoryMemory(max_size=50)
        self.calculator = CalculatorTool()
        self.json_parser = JSONParserTool()
        self.string_tool = StringManipulationTool()
        self.web_scraper = WebScraperTool()
    
    async def analyze_stock_data(self, stock_symbol: str) -> Dict[str, Any]:
        """
        Comprehensive stock data analysis pipeline
        
        Args:
            stock_symbol: Stock ticker symbol
        
        Returns:
            Analyzed stock data report
        """
        # Fetch stock data from web
        stock_data = await self._fetch_stock_data(stock_symbol)
        
        # Process and clean data
        processed_data = await self._process_stock_data(stock_data)
        
        # Perform statistical analysis
        analysis_results = await self._analyze_stock_performance(processed_data)
        
        # Store results in memory
        await self.memory.add_item(f'{stock_symbol}_analysis', analysis_results)
        
        return analysis_results
    
    async def _fetch_stock_data(self, symbol: str) -> List[Dict[str, Any]]:
        """
        Fetch stock data from a financial API or web source
        
        Args:
            symbol: Stock ticker symbol
        
        Returns:
            Raw stock data
        """
        # Simulated web scraping of financial data
        financial_urls = [
            f"https://finance.yahoo.com/quote/{symbol}",
            f"https://www.marketwatch.com/investing/stock/{symbol}"
        ]
        
        stock_data = []
        for url in financial_urls:
            try:
                # Extract financial data
                raw_content = await self.web_scraper.execute(url, operation='parse')
                
                # Parse potential JSON content
                try:
                    parsed_content = await self.json_parser.execute(raw_content)
                    stock_data.append(parsed_content)
                except ValueError:
                    # Fallback to text processing
                    processed_text = await self.string_tool.execute(raw_content)
                    stock_data.append({'raw_text': processed_text})
            
            except Exception as e:
                print(f"Error fetching data from {url}: {e}")
        
        return stock_data
    
    async def _process_stock_data(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Process and clean stock data
        
        Args:
            data: Raw stock data
        
        Returns:
            Processed stock data
        """
        processed_data = []
        for item in data:
            # Clean and standardize data
            cleaned_item = {}
            for key, value in item.items():
                # Use string tool to clean keys and values
                cleaned_key = await self.string_tool.execute(str(key), operation='clean')
                cleaned_value = await self.string_tool.execute(str(value), operation='clean')
                
                cleaned_item[cleaned_key] = cleaned_value
            
            processed_data.append(cleaned_item)
        
        return processed_data
    
    async def _analyze_stock_performance(self, processed_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Perform statistical analysis on stock data
        
        Args:
            processed_data: Cleaned stock data
        
        Returns:
            Stock performance analysis
        """
        # Extract numeric values for analysis
        numeric_values = []
        for item in processed_data:
            for value in item.values():
                try:
                    # Attempt to convert to float for calculation
                    numeric_value = float(value.replace(',', '').replace('$', ''))
                    numeric_values.append(numeric_value)
                except (ValueError, AttributeError):
                    pass
        
        # Perform calculations using calculator tool
        if numeric_values:
            total = sum(numeric_values)
            count = len(numeric_values)
            
            average = await self.calculator.execute(f'{total} / {count}')
            
            return {
                'total_value': total,
                'average_value': average,
                'data_points': count,
                'raw_data': processed_data
            }
        
        return {'error': 'No numeric data found'}

async def main():
    # Demonstrate the Data Analysis Pipeline
    pipeline = DataAnalysisPipeline()
    
    # Analyze stock data for a sample stock
    analysis_results = await pipeline.analyze_stock_data('AAPL')
    
    # Pretty print results
    print(json.dumps(analysis_results, indent=2))

if __name__ == "__main__":
    asyncio.run(main())
