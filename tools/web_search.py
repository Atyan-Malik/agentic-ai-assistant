
import os

from dotenv import load_dotenv
from tavily import TavilyClient

load_dotenv()


def web_search(
    query: str,
    max_results: int = 5,
) -> dict:
    """Search the web using Tavily."""

    if not isinstance(query, str) or not query.strip():
        return {
            "success": False,
            "error": "A search query is required.",
            "results": [],
        }

    if (
        not isinstance(max_results, int)
        or isinstance(max_results, bool)
        or not 1 <= max_results <= 10
    ):
        return {
            "success": False,
            "error": "max_results must be an integer from 1 to 10.",
            "results": [],
        }

    api_key = os.getenv("TAVILY_API_KEY")

    if not api_key:
        return {
            "success": False,
            "error": "TAVILY_API_KEY is missing from your .env file.",
            "results": [],
        }

    try:
        client = TavilyClient(api_key=api_key)

        response = client.search(
            query=query.strip(),
            max_results=max_results,
            search_depth="basic",
            include_answer=False,
        )

        results = [
            {
                "title": item.get("title", ""),
                "url": item.get("url", ""),
                "snippet": item.get("content", ""),
                "score": item.get("score"),
            }
            for item in response.get("results", [])
        ]

        return {
            "success": True,
            "query": query,
            "results": results,
        }

    except Exception as exc:
        return {
            "success": False,
            "query": query,
            "error": f"Tavily search failed: {exc}",
            "results": [],
        }
