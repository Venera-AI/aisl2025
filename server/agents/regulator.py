from google.adk.agents import Agent
from ..config import config
from ..tools import search, visit_web_page

regulator_agent = Agent(
    name="regulator_agent",
    model=config.regulator.get_model(),
    description="This agent gather regulation related to the current conversation",
    instruction="""""".strip(),
    tools=[search, visit_web_page],
)
