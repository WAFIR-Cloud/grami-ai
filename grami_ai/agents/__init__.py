"""
GRAMI AI Agents Package

This package provides the specialized AI agents that form the GRAMI digital marketing crew:

1. Strategist Agents:
   - Market Research Agent
   - Content Strategy Agent
   - Audience Analysis Agent

2. Content Creator Agents:
   - Caption Writer Agent
   - Visual Content Agent
   - Reels Strategy Agent

3. Scheduler Agents:
   - Timing Optimization Agent
   - Content Calendar Agent
   - Real-time Adjustment Agent

4. Engagement Agents:
   - Comment Response Agent
   - Community Manager Agent
   - Trend Participation Agent

5. Analytics Agents:
   - Performance Tracker Agent
   - Insight Generator Agent
   - A/B Testing Agent
"""

from .base_agent import BaseAgent
from .strategist import (
    MarketResearchAgent,
    ContentStrategyAgent,
    AudienceAnalysisAgent,
)
from .content_creator import (
    CaptionWriterAgent,
    VisualContentAgent,
    ReelsStrategyAgent,
)
from .scheduler import (
    TimingOptimizationAgent,
    ContentCalendarAgent,
    RealTimeAdjustmentAgent,
)
from .engagement import (
    CommentResponseAgent,
    CommunityManagerAgent,
    TrendParticipationAgent,
)
from .analytics import (
    PerformanceTrackerAgent,
    InsightGeneratorAgent,
    ABTestingAgent,
)

__all__ = [
    # Base Agent
    'BaseAgent',
    
    # Strategist Agents
    'MarketResearchAgent',
    'ContentStrategyAgent',
    'AudienceAnalysisAgent',
    
    # Content Creator Agents
    'CaptionWriterAgent',
    'VisualContentAgent',
    'ReelsStrategyAgent',
    
    # Scheduler Agents
    'TimingOptimizationAgent',
    'ContentCalendarAgent',
    'RealTimeAdjustmentAgent',
    
    # Engagement Agents
    'CommentResponseAgent',
    'CommunityManagerAgent',
    'TrendParticipationAgent',
    
    # Analytics Agents
    'PerformanceTrackerAgent',
    'InsightGeneratorAgent',
    'ABTestingAgent',
]