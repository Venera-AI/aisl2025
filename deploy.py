import vertexai
from vertexai.preview import reasoning_engines
from medical_qa import root_agent  # modify this if your agent is not in agent.py
import toml

# TODO: Fill in these values for your project
PROJECT_ID = "venerian"
LOCATION = "us-central1"  # For other options, see https://cloud.google.com/vertex-ai/generative-ai/docs/agent-engine/overview#supported-regions
STAGING_BUCKET = "gs://venera-aisl2025"

# Initialize the Vertex AI SDK
vertexai.init(
    project=PROJECT_ID,
    location=LOCATION,
    staging_bucket=STAGING_BUCKET,
)


# Wrap the agent in an AdkApp object
app = reasoning_engines.AdkApp(
    agent=root_agent,
    enable_tracing=True,
)
from vertexai import agent_engines

remote_app = agent_engines.create(
    agent_engine=app, requirements=["google-cloud-aiplatform[adk,agent_engines]"]
)

print(f"Deployment finished!")
print(f"Resource Name: {remote_app.resource_name}")
# Resource Name: "projects/{PROJECT_NUMBER}/locations/{LOCATION}/reasoningEngines/{RESOURCE_ID}"
