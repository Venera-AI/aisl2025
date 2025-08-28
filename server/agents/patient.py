from google.adk.agents import Agent
from ..config import config
from google.genai import types as gtypes
from google.adk.agents.callback_context import CallbackContext


def change_role_to_user(callback_context: CallbackContext) -> gtypes.Content:
    return gtypes.Content(
        parts=[gtypes.Part(text=callback_context.state.get("question"))], role="user"
    )


patient_agent = Agent(
    name="patient",
    model=config.patient.get_model(),
    description="This agent act as a patient",
    instruction="""You are a patient talking to a doctor, your job is to answer the doctor's answer using a real EHR from a real patient provided in <EHR></EHR> tags.
If the doctor ask you to do take an exam, but the results is not in the EHR, you must provide the exam results as if that real patient have taken the exam.

You should response in Vietnamese.

<EHR>{document}</EHR>
""".strip(),
)
