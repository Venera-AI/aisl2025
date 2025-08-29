from google.adk.agents import Agent
from ..config import config
from google.genai import types as gtypes
from google.adk.agents.callback_context import CallbackContext


def remove_user_input(callback_context: CallbackContext):
    callback_context.user_content.parts[0].text = "[REDACTED]"


conversation_init_agent = Agent(
    name="conversation_init",
    model=config.conversation_init.get_model(),
    description="This agent will choose a topic for a doctor visit, and provide the first patient question to initialize the conversation.",
    instruction="""You are a helpful assistant for creating medical questions. Pretend to be a user asking question about the provied ehr. The person you are talking to doesn't know about this EHR. Think from the user's perspective. Be a bit real, don't be too formal.
Only output what the user would say and nothing else.
    """.strip(),
    output_key="question",
    after_agent_callback=remove_user_input,
)
