import requests
from uuid import uuid4
import json
import sys
from ehr_read import get_ehrs
import asyncio
import tqdm.asyncio


def create_session(
    base_url: str, app_name: str, user_id: str, session_id=None, state=None, events=None
):
    """
    Create a new session for the given app and user.
    """
    url = f"{base_url}/apps/{app_name}/users/{user_id}/sessions"
    payload = {}
    if state is not None:
        payload["state"] = state
    if events is not None:
        payload["events"] = events
    if session_id:
        # Use the endpoint to create a session with a specific ID
        url = f"{base_url}/apps/{app_name}/users/{user_id}/sessions/{session_id}"
        response = requests.post(url, json=payload)
    else:
        response = requests.post(url, json=payload)
    response.raise_for_status()
    return response.json()


def run_agent_loop_and_collect_data(base_url: str, ehr: dict):
    app_name = "server"
    # Create a new session
    user_id = uuid4().hex
    session = create_session(base_url, app_name, user_id)
    session_id = (
        session["id"]
        if isinstance(session, dict) and "id" in session
        else session.get("session_id")
    )
    # Prepare payload for /run endpoint
    payload = {
        "appName": app_name,
        "userId": user_id,
        "sessionId": session_id,
        "newMessage": {"parts": [{"text": json.dumps(ehr)}]},
    }
    url = f"{base_url}/run"
    response = requests.post(url, json=payload)
    response.raise_for_status()
    return response.json()


async def main(base_url: str):
    ehrs = get_ehrs()[:2]
    results = await tqdm.asyncio.tqdm_asyncio.gather(
        *[run_agent_loop_and_collect_data(base_url, ehr) for ehr in ehrs]
    )
    with open("output.jsonl", "w") as f:
        for result in results:
            json.dump(result, f)
            f.write("\n")


if __name__ == "__main__":
    # Example user_id, replace as needed
    if len(sys.argv) > 2:
        base_url = sys.argv[1]
    else:
        base_url = "http://localhost:8000"

    asyncio.run(main(base_url))
