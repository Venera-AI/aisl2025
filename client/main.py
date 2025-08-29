import requests
from uuid import uuid4
import json
import typer
from ehr_read import get_ehrs
import asyncio
import tqdm.asyncio
from vertexai import agent_engines


async def run_agent_loop_and_collect_data(
    agent_engine: agent_engines.AgentEngine, ehr: dict
):
    app_name = "server"
    # Create a new session
    user_id = uuid4().hex
    session = agent_engine.create_session(user_id=user_id)
    session_id = session["id"]
    return list(
        agent_engine.stream_query(
            user_id=user_id,
            session_id=session_id,
            message=json.dumps({"document": ehr}),
        )
    )


from functools import wraps

app = typer.Typer()


@app.command()
@lambda f: wraps(f)(lambda *a, **kw: asyncio.run(f(*a, **kw)))
async def main(resource_name: str):
    ehrs = get_ehrs()[:2]
    agent_engine = agent_engines.get(resource_name)
    results = await tqdm.asyncio.tqdm_asyncio.gather(
        *[run_agent_loop_and_collect_data(agent_engine, ehr) for ehr in ehrs]
    )
    with open("output.jsonl", "w") as f:
        for result in results:
            json.dump(result, f, ensure_ascii=False)
            f.write("\n")


if __name__ == "__main__":
    app()
