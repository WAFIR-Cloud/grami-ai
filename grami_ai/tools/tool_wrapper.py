from typing import Any, Callable, Dict


class GramiTool:
    """
    A wrapper for defining and managing tools for Gemini function calling.
    """

    def __init__(self, function: Callable, **kwargs):
        """
        Initializes a GramiTool.

        Args:
            function: The Python function to be called.
            **kwargs: Additional keyword arguments to define tool properties:
                - name (str): The name of the tool (defaults to the function name).
                - description (str): A description of the tool's purpose.
                - parameters (dict): A dictionary defining the tool's parameters
                                    (following the OpenAPI schema).
        """
        self.function = function
        self.name = kwargs.get("name", function.__name__)
        self.description = kwargs.get("description", function.__doc__ or "")
        self.parameters = kwargs.get("parameters", {})

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the tool definition to a dictionary compatible with the Gemini API.
        """
        return {
            "name": self.name,
            "description": self.description,
            "parameters": self.parameters,
        }
