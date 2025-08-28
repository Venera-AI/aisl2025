from google.adk.agents import Agent
from ..config import config
from google.genai import types as gtypes
from google.adk.agents.callback_context import CallbackContext


def change_role_to_user(callback_context: CallbackContext) -> gtypes.Content:
    return gtypes.Content(
        parts=[gtypes.Part(text=callback_context.state.get("question"))], role="user"
    )


conversation_init_agent = Agent(
    name="conversation_init",
    model=config.conversation_init.get_model(),
    description="This agent will choose a topic for a doctor visit, and provide the first patient question to initialize the conversation.",
    instruction="""You are a helpful assistant for creating medical questions. Pretend to be a user reporting about their symptom based on the provied ehr. Think from the user's perspective.
Only output what the user would say and nothing else.
    """.strip(),
    output_key="question",
)
