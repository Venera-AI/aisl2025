from .agents import (
    doctor_agent,
    patient_agent,
    conversation_init_agent,
)
from google.adk.agents import LoopAgent, SequentialAgent, BaseAgent, InvocationContext
from google.adk.events import Event, EventActions
from typing import AsyncGenerator
import json

MAX_TURN = 3


class TurnCheck(BaseAgent):
    def __init__(self, name: str):
        super().__init__(name=name)

    async def _run_async_impl(
        self, ctx: InvocationContext
    ) -> AsyncGenerator[Event, None]:
        turn_left = ctx.session.state.get("turn", 0)
        if turn_left == 0:
            yield Event(author=self.name, actions=EventActions(escalate=True))
        else:
            # Yielding an event without content or actions just lets the flow continue.
            yield Event(
                author=self.name,
                actions=EventActions(state_delta={"turn": turn_left - 1}),
            )


class ParseUserRequest(BaseAgent):

    def __init__(self, name: str):
        super().__init__(name=name)

    async def _run_async_impl(
        self, ctx: InvocationContext
    ) -> AsyncGenerator[Event, None]:
        user_req = {}
        for part in ctx.user_content.parts:
            if part.text:
                user_req = json.loads(part.text)
        # Yielding an event without content or actions just lets the flow continue.
        yield Event(
            author=self.name,
            actions=EventActions(
                state_delta={
                    "document": user_req["document"],
                    "turn": user_req.get("turn", MAX_TURN),
                }
            ),
        )


root_agent = SequentialAgent(
    name="root_agent",
    description="Root agent",
    sub_agents=[
        ParseUserRequest("ehr_extractor"),
        conversation_init_agent,
        LoopAgent(
            name="doctor_patient_loop",
            description="Core doctor ask, patient answer loop",
            sub_agents=[
                doctor_agent,
                TurnCheck("turn_check"),
                patient_agent,
            ],
            max_iterations=MAX_TURN,
        ),
        doctor_agent.clone(),
    ],
)
