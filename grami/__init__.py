"""
GRAMI: A Dynamic AI Agent Framework

This framework provides tools and abstractions for building intelligent,
asynchronous AI agents that can interact with various LLM providers.
"""

import warnings
from .agents import AsyncAgent, BaseAgent

# For backward compatibility
try:
    from .agent import AsyncAgent as LegacyAsyncAgent
    # Only warn if someone imports from the legacy path
    if LegacyAsyncAgent:
        warnings.warn(
            "Importing AsyncAgent directly from grami.agent is deprecated. "
            "Please use 'from grami.agents import AsyncAgent' instead.",
            DeprecationWarning,
            stacklevel=2
        )
except ImportError:
    pass

__version__ = "0.3.133"

__all__ = [
    'AsyncAgent',
    'BaseAgent',
    # Legacy exports
    'LegacyAsyncAgent'
]
