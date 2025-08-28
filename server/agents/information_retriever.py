from google.adk.agents import Agent
from ..config import config
from ..tools import search, visit_web_page

information_retriever_agent = Agent(
    name="information_retriever",
    model=config.information_retriever.get_model(),
    description="This agent will find all information related to the current conversation and maybe EHR to help doctor make decisions",
    instruction="""""".strip(),
    tools=[search, visit_web_page],
)
