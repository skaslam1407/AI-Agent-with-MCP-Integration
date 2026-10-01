from openai import OpenAI
from dotenv import load_dotenv
import os

from loader import thinking

load_dotenv()

client = OpenAI(
    base_url=os.getenv("BASE_URL"),
    api_key=os.getenv("API_KEY")
)


def build_tool_descriptions(tools):

    descriptions = ""

    for tool in tools:

        descriptions += f"""
Tool:
{tool.name}

Description:
{tool.description}

----------------------------
"""

    return descriptions

def planner(state, tools):

    tool_descriptions = build_tool_descriptions(tools)

    prompt = f"""
You are an AI Planner.

Your job is to decide ONLY the next action.

User Request:
{state["user_request"]}

Completed Actions:
{state["actions"]}

Previous Observations:
{state["observations"]}

Available Tools:
{tool_descriptions}

Rules:

1. Choose only ONE next action.
2. Never repeat an action that has already been completed.
3. Use the observations to decide what is still required.
4. If the user's request has been completely satisfied, return FINISH.
5. If the request needs NO tool (general question, greeting, math,
   explanation, or no available tool fits), return FINISH immediately.
6. Return ONLY the exact tool name or FINISH.
7. Do not explain your answer.
8. Do not add quotes, markdown, or extra words.

Next Action:
"""

    with thinking("Planning next action..."):
        response = client.chat.completions.create(
            model=os.getenv("MODEL"),
            messages=[
                {
                    "role": "system",
                    "content": "You are an AI planner."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

    return response.choices[0].message.content.strip()

