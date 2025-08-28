from .agents import (
    doctor_agent,
    patient_agent,
    conversation_init_agent,
    final_report_agent,
)
from google.adk.agents import LoopAgent, SequentialAgent, BaseAgent, InvocationContext
from google.adk.events import Event, EventActions
from typing import AsyncGenerator


class FinalReportEscalationCheck(BaseAgent):
    """Checks research evaluation and escalates to stop the loop if grade is 'pass'."""

    def __init__(self, name: str):
        super().__init__(name=name)

    async def _run_async_impl(
        self, ctx: InvocationContext
    ) -> AsyncGenerator[Event, None]:
        conclusion = ctx.session.state.get("conclusion")
        if conclusion:
            yield Event(author=self.name, actions=EventActions(escalate=True))
        else:
            # Yielding an event without content or actions just lets the flow continue.
            yield Event(author=self.name)


class DocumentSaver(BaseAgent):
    """Extract document and put it in the state"""

    def __init__(self, name: str):
        super().__init__(name=name)

    async def _run_async_impl(
        self, ctx: InvocationContext
    ) -> AsyncGenerator[Event, None]:
        document = None
        for part in ctx.user_content.parts:
            if part.text:
                document = part.text
        # Yielding an event without content or actions just lets the flow continue.
        yield Event(
            author=self.name,
            actions=EventActions(state_delta={"document": document}),
        )


root_agent = SequentialAgent(
    name="root_agent",
    description="Root agent",
    sub_agents=[
        LoopAgent(
            name="doctor_patient_loop",
            description="Core doctor ask, patient answer loop",
            sub_agents=[],
            max_iterations=3,
        ),
    ],
)
