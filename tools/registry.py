
from typing import Any, Callable

from tools.calculator import calculate
from tools.web_search import web_search
from tools.weather import get_weather


class ToolRegistry:
    """Register, discover, and execute agent tools."""

    def __init__(self):
        self._tools: dict[str, dict[str, Any]] = {}

    def register(
        self,
        name: str,
        description: str,
        function: Callable,
        parameters: dict[str, Any],
    ) -> None:
        """Register a callable tool and its JSON argument schema."""

        if name in self._tools:
            raise ValueError(f"Tool '{name}' is already registered.")

        if not callable(function):
            raise TypeError("Tool function must be callable.")

        self._tools[name] = {
            "name": name,
            "description": description,
            "function": function,
            "parameters": parameters,
        }

    def get_tool_schemas(self) -> list[dict[str, Any]]:
        """Return tool definitions suitable for Ollama tool calling."""
        return [
            {
                "type": "function",
                "function": {
                    "name": tool["name"],
                    "description": tool["description"],
                    "parameters": tool["parameters"],
                },
            }
            for tool in self._tools.values()
        ]

    def list_tools(self) -> list[dict[str, str]]:
        """List tool names and descriptions."""
        return [
            {
                "name": tool["name"],
                "description": tool["description"],
            }
            for tool in self._tools.values()
        ]

    def execute(
        self,
        name: str,
        arguments: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Execute a registered tool with validated basic arguments."""

        tool = self._tools.get(name)

        if tool is None:
            return {
                "success": False,
                "error": f"Unknown tool: {name}",
            }

        if arguments is None:
            arguments = {}

        if not isinstance(arguments, dict):
            return {
                "success": False,
                "error": "Tool arguments must be a JSON object.",
            }

        try:
            result = tool["function"](**arguments)

            if not isinstance(result, dict):
                return {
                    "success": True,
                    "result": result,
                }

            return result

        except TypeError as exc:
            return {
                "success": False,
                "error": f"Invalid arguments for '{name}': {exc}",
            }

        except Exception as exc:
            return {
                "success": False,
                "error": f"Tool '{name}' failed: {exc}",
            }


def create_default_registry() -> ToolRegistry:
    """Create a registry containing the built-in tools."""

    registry = ToolRegistry()

    registry.register(
        name="calculator",
        description=(
            "Calculate mathematical expressions. "
            "Use for arithmetic, percentages, and powers."
        ),
        function=calculate,
        parameters={
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": (
                        "Mathematical expression, e.g. '(25 * 4) + 100 / 2'."
                    ),
                }
            },
            "required": ["expression"],
            "additionalProperties": False,
        },
    )

    registry.register(
        name="web_search",
        description=(
            "Search the web for information, recent developments, "
            "and relevant webpages."
        ),
        function=web_search,
        parameters={
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The topic or question to search for.",
                },
                "max_results": {
                    "type": "integer",
                    "description": "Number of results, from 1 to 10.",
                    "minimum": 1,
                    "maximum": 10,
                },
            },
            "required": ["query"],
            "additionalProperties": False,
        },
    )

    registry.register(
        name="get_weather",
        description=(
            "Get current weather and a daily forecast for a city."
        ),
        function=get_weather,
        parameters={
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "City name, e.g. Multan or London.",
                },
                "forecast_days": {
                    "type": "integer",
                    "description": "Number of forecast days, from 1 to 7.",
                    "minimum": 1,
                    "maximum": 7,
                },
            },
            "required": ["city"],
            "additionalProperties": False,
        },
    )

    return registry


# Ready-to-use shared registry.
tool_registry = create_default_registry()
