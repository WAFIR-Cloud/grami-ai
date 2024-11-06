import enum


class AgentType(str, enum.Enum):
    """Enum for Agent types, with Kafka-compatible topic names."""
    COPYWRITER = "copywriter"
    CONTENT_CREATOR_PLANNER = "content_creator_planner"
    SOCIAL_MEDIA_MANAGER = "social_media_manager"
    PHOTOGRAPHER_DESIGNER = "photographer_designer"
    CONTENT_SCHEDULER = "content_scheduler"
    HASHTAGS_MARKET_RESEARCHER = "hashtags_market_researcher"
