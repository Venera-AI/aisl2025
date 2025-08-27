import datetime
import os
from typing import Literal, Optional
from zoneinfo import ZoneInfo
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
import litellm
import requests
from tavily import TavilyClient

litellm.drop_params = True

# def search(query: str) -> dict[str, dict[str, str]]:
#     """
#     Search the web using Jina.ai API.

#     Args:
#         query (str): The search query.
#     Returns:
#         str: The search results as a string.
#     """
#     api_url = "https://s.jina.ai/"
#     headers = {
#         "Accept": "application/json",
#         "Authorization": f"Bearer {os.environ.get('JINA_API_KEY')}",
#     }
#     params = {"q": query}
#     response = requests.get(api_url, headers=headers, params=params, timeout=300)
#     if response.status_code == 200:
#         data = response.json()
#         results = data.get("data", [])
#         if not results:
#             return {"0": {"error": "No results found"}}
#         return {
#             str(k): {
#                 "title": item.get("title", ""),
#                 "url": item.get("url", ""),
#                 "snippet": item.get("description", ""),
#             }
#             for k, item in enumerate(results)
#         }
#     return {"0": {"error": f"Search failed with status code {response.status_code}."}}

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


mem = ["User is a male teenager"]


def add_to_memory(memo: str) -> None:
    """
    This tool allows you to persist information across conversations. Write whatever information you want to remember. The information will appear in the USER INFORMATION in future conversations.

    Args:
        memo (str): The information to persist.
    Returns:
        None
    """
    mem.append(memo)


def construct_prompt_with_memory() -> str:
    return f"""You are a web search assistant. Your job is find the information the user need using the search tool and summarize the text into a detailed, 2-4 paragraph explanation that captures the main ideas and provides a comprehensive answer to the query.
If the query is \"summarize\", you should provide a detailed summary of the text. If the query is a specific question, you should answer it in the summary.

You also have to provide citations for your summary like this:
<cite chunk_id="N">the snippet of your final answer</cite>
Where:
  - N is the chunk index.
  - The text inside <cite></cite> is part of your answer, not the original chunk text.
  - Keep your answer minimal in whitespace. Do not add extra spaces or line breaks.
  - Only add <cite> tags around the key phrases of your answer that rely on some chunk.
Remember: The text inside <cite> is your final answer's snippet, not the chunk text itself.

Example:
User's query: Who is Donald Trump?
Web search results: {{
    "0": {{"title": "Donald Trump", "url": "https://en.wikipedia.org/wiki/Donald_Trump", "content": "Donald John Trump (born June 14, 1946) is an American politician, media personality, and businessman who is the 47th president of the United States."}},
    ...
}}
Your answer should look like:
Donald Trump is <cite chunk_id="0">the 47th president of the United States</cite> 

USER INFORMATION:
{'\n'.join("- " + fact for fact in mem)}
    """.strip()


root_agent = Agent(
    name="root_agent",
    model=LiteLlm(
        "groq/moonshotai/kimi-k2-instruct",
        reasoning_effort="high",
        thinking={
            "type": "enabled",
            "budget_tokens": 8000,
        },
    ),
    # model="gemini-2.5-flash",
    description=("Agent to answer questions about the time and weather in a city."),
    instruction=construct_prompt_with_memory(),
    tools=[
        add_to_memory,
        search,
        visit_web_page,
    ],
)
