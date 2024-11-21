import os
import asyncio
import logging
from typing import Dict, Any, List

from grami_ai.agents import AsyncAgent
from grami_ai.memory import InMemoryAbstractMemory
from grami_ai.llms import GeminiLLMProvider

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set Google API Key
os.environ['GOOGLE_API_KEY'] = 'api_key'

# Pure Python function tools with clear, descriptive signatures
def calculate(operation: str, a: str, b: str) -> str:
    """
    Perform mathematical calculations.
    
    Args:
        operation (str): Type of mathematical operation
        a (str): First numeric value
        b (str): Second numeric value
    
    Returns:
        str: Calculation result
    """
    try:
        x, y = float(a), float(b)
        
        if operation == 'add':
            return str(x + y)
        elif operation == 'subtract':
            return str(x - y)
        elif operation == 'multiply':
            return str(x * y)
        elif operation == 'divide':
            return str(x / y) if y != 0 else "Error: Division by zero"
        else:
            return f"Error: Unsupported operation {operation}"
    except ValueError:
        return "Error: Invalid numeric input"

def analyze_market_potential(company_data: Dict[str, str]) -> str:
    """
    Analyze market potential based on company data.
    
    Args:
        company_data (Dict[str, str]): Company financial and strategic information
    
    Returns:
        str: Market potential analysis
    """
    try:
        revenue = float(company_data.get('revenue', '0'))
        employees = int(company_data.get('employees', '0'))
        strategic_plans = company_data.get('strategic_plans', '')
        
        # Simple market potential scoring
        market_score = 0
        if revenue > 1000000:
            market_score += 3
        if employees > 50:
            market_score += 2
        if 'new markets' in strategic_plans.lower():
            market_score += 2
        
        potential_categories = {
            0: "Low Potential",
            1: "Limited Potential",
            2: "Moderate Potential",
            3: "Good Potential",
            4: "High Potential",
            5: "Excellent Potential"
        }
        
        return potential_categories.get(market_score, "Unknown Potential")
    except Exception as e:
        return f"Analysis Error: {str(e)}"

class EnterpriseAgent:
    """Enterprise agent with AI-driven analysis."""
    
    def __init__(self):
        """Initialize enterprise agent with Gemini provider."""
        # Create Gemini LLM provider
        gemini_provider = GeminiLLMProvider(
            api_key=os.environ['GOOGLE_API_KEY'],
            model_name="models/gemini-1.5-flash",
            system_instruction="You are an advanced enterprise AI analyst. "
                               "Use the provided tools to analyze company data comprehensively. "
                               "Break down complex problems and provide insightful recommendations."
        )
        
        # Initialize agent with Gemini provider and tools
        self.agent = AsyncAgent(
            tools=[calculate, analyze_market_potential],  
            memory=InMemoryAbstractMemory(),
            llm_provider=gemini_provider
        )
    
    async def analyze_enterprise_data(self, sensitive_data: Dict[str, Any]) -> str:
        """
        Analyze enterprise data using AI-driven approach.
        
        Args:
            sensitive_data (Dict[str, Any]): Confidential enterprise data
        
        Returns:
            str: Comprehensive enterprise analysis
        """
        try:
            logger.info("Initiating enterprise data analysis...")
            
            # Prepare task for AI analysis
            task = {
                'objective': 'Perform a comprehensive analysis of the company\'s financial and strategic position',
                'context': 'You have access to financial data and strategic plans. Use the available tools to gain insights.',
                'content': f"""
Analyze the following company data:
Financial Details:
- Revenue: ${sensitive_data['company_financials']['revenue']}
- Expenses: ${sensitive_data['company_financials']['expenses']}
- Number of Employees: {sensitive_data['company_financials']['employees']}

Strategic Plans:
{', '.join(sensitive_data['strategic_plans'])}

Use the available tools (calculate and analyze_market_potential) to:
1. Perform financial calculations
2. Assess market potential
3. Provide strategic recommendations
4. Explain your reasoning and tool usage
""",
                'data': sensitive_data,
                'instructions': [
                    'Analyze the financial performance',
                    'Assess market potential',
                    'Provide strategic recommendations',
                    'Explain your reasoning and tool usage'
                ]
            }
            
            # Execute task using AI agent
            result = await self.agent.execute_task(task)
            
            logger.info("Enterprise data analysis completed successfully")
            return result
        
        except Exception as e:
            logger.error(f"Error in enterprise data processing: {e}", exc_info=True)
            return "Analysis failed due to processing error."

async def main():
    """
    Main async function to demonstrate AI-driven enterprise analysis.
    """
    try:
        # Simulated sensitive enterprise data
        sensitive_data = {
            'company_financials': {
                'revenue': '1500000', 
                'expenses': '1200000', 
                'employees': '50'
            },
            'strategic_plans': [
                'Expand to new markets',
                'Develop proprietary technology', 
                'Increase R&D investment'
            ]
        }
        
        # Initialize enterprise agent
        enterprise_agent = EnterpriseAgent()
        
        # Analyze sensitive data
        result = await enterprise_agent.analyze_enterprise_data(sensitive_data)
        
        print("\nEnterprise Analysis Result:")
        print(result)
        
        logger.info("Enterprise analysis complete, AI-driven processing finished")
    
    except Exception as e:
        logger.error(f"Critical error in enterprise data processing: {e}", exc_info=True)

if __name__ == "__main__":
    # Run the example
    asyncio.run(main())
