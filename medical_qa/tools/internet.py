import os
from typing import Literal, Optional
import requests
from tavily import TavilyClient

web_pages: dict[str, str] = {}


def search(
    query: str,
    topic: Literal["general", "news", "finance"] = "general",
    time_range: Optional[Literal["day", "week", "month", "year"]] = None,
    limit: int = 5,
) -> dict[str, dict[str, str]]:
    """Perform a search ont the internet and return top search results with titles, url and snippet. Use this tool to access up-to-date information from the web or when responding to the user requires information about their location. Some examples of when to use the this tool include:

    - Local Information: weather, local businesses, events.
    - Freshness: if up-to-date information on a topic could change or enhance the answer.
    - Niche Information: detailed info not widely known or understood (found on the internet).
    - Accuracy: if the cost of outdated information is high, use web sources directly.

    This tool only return a snippet of the web page, to get the full content of the web page, use the visit-web-page tool

        Args:
            query (str): The search query.
            time_range (enum): Time range for results ('day', 'week', 'month', 'year').
            topic (enum): Topic filter ('general', 'news', 'finance').
            limit (int): Number of result
        Returns:
            dict: The search results as a dictionary.
    """
    client = TavilyClient(api_key=os.environ.get("TAVILY_API_KEY"))
    try:
        results = client.search(
            query=query,
            time_range=time_range,
            topic=topic,
            search_depth="advanced",
            max_results=limit,
            include_raw_content="text",
            chunks_per_source=5,
        )
        items = results.get("results", [])
        if not items:
            return {"error": {"detail": "No results found"}}
        res = {}
        for k, item in enumerate(items):
            res[str(k)] = {
                "title": item.get("title", ""),
                "url": item.get("url", ""),
                "content": item.get("content", ""),
            }
            if "url" in item:
                web_pages[item["url"]] = item.get("raw_content", "")

        return res
    except Exception as e:
        return {"error": {"details": f"Search failed: {e}"}}


def visit_web_page(url: str) -> str:
    """
    Visit a webpage at the given url and reads its content as markdown string. Use this to browse webpages.

    Args:
        url (str): The URL of the web page.
    Returns:
        str: The summarized content of the web page.
    """
    if url in web_pages:
        return web_pages[url]
    api_url = f"https://r.jina.ai/{url}"
    headers = {
        "Authorization": f"Bearer {os.environ.get('JINA_API_KEY')}",
        "X-Retain-Images": "none",
    }
    response = requests.get(api_url, headers=headers, timeout=300)
    if response.status_code == 200:
        return response.text[:4000] + "..."
    return f"Failed to visit web page. Status code: {response.status_code}."
