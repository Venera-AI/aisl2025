from google.adk.agents import Agent
from ..config import config

final_report_agent = Agent(
    name="conversation_init",
    model=config.conversation_init.get_model(),
    description="This agent will provide the patient with the final conclusion from the doctor and some advices",
    instruction="""You are a health care AI assistant. Your job is to provide the patient with theirs""".strip(),
)
