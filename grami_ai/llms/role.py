from enum import Enum, auto

class Role(Enum):
    """
    Enumeration of conversation roles in the AI framework.
    
    Defines standard roles for messages in conversational AI systems.
    """
    SYSTEM = auto()    # System-level instructions or context
    USER = auto()      # User input or query
    ASSISTANT = auto() # AI assistant's response
    TOOL = auto()      # Tool execution result
