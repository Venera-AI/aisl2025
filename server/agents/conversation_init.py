from google.adk.agents import Agent

patient_init_agent = Agent(
    name="conversation_init",
    description="This agent will choose a topic for a doctor visit, and provide the first patient question to initialize the conversation.",
    instruction="""Patient init agent instruction""".strip(),
)
