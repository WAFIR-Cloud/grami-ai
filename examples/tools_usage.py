import asyncio
from grami_ai.tools import CalculatorTool, JSONParserTool

async def demonstrate_tools_usage():
    # Calculator Tool Example
    print("🧮 Calculator Tool Example:")
    calculator = CalculatorTool()
    
    try:
        result = await calculator.execute('2 + 3 * 4')
        print(f"Calculation: 2 + 3 * 4 = {result}")
        
        complex_calc = await calculator.execute('(10 + 5) / 3')
        print(f"Complex Calculation: (10 + 5) / 3 = {complex_calc}")
    except ValueError as e:
        print(f"Calculation Error: {e}")
    
    # JSON Parser Tool Example
    print("\n📦 JSON Parser Tool Example:")
    json_tool = JSONParserTool()
    
    # Parsing JSON
    json_data = '{"name": "John Doe", "age": 30, "city": "New York"}'
    parsed_data = await json_tool.execute(json_data)
    print("Parsed Data:", parsed_data)
    
    # JSON Validation
    try:
        is_valid = await json_tool.execute(json_data, operation='validate')
        print("JSON Validation:", is_valid)
    except ValueError as e:
        print(f"Validation Error: {e}")
    
    # JSON Transformation
    transformed_data = await json_tool.execute(
        json_data, 
        operation='transform', 
        filter_keys=['name', 'age']
    )
    print("Transformed Data:", transformed_data)

if __name__ == "__main__":
    asyncio.run(demonstrate_tools_usage())
