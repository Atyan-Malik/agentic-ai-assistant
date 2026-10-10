
from tools import calculate, web_search, get_weather
from tools import tool_registry


def main():
    print("\n--- CALCULATOR ---")
    print(calculate("(25 * 4) + 100 / 2"))

    print("\n--- WEB SEARCH ---")
    print(web_search("Ollama Qwen 2.5", max_results=3))

    print("\n--- WEATHER ---")
    print(get_weather("Multan", forecast_days=2))

    print("\n--- REGISTERED TOOLS ---")
    print(tool_registry.list_tools())

    print("\n--- REGISTRY EXECUTION ---")
    print(
        tool_registry.execute(
            "calculator",
            {"expression": "125 * 8"},
        )
    )


if __name__ == "__main__":
    main()
