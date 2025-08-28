from google.adk.agents import Agent
from ..config import config

labtest_suggest_agent = Agent(
    name="labtest_suggest_agent",
    model=config.labtest_suggest.get_model(),
    description="This agent will suggest the relevant lab test based on the current conversation and EHR",
    instruction="""Patient init agent instruction""".strip(),
)
