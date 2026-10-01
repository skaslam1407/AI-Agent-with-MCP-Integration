from state import (
    create_state,
    add_action,
    record_observation,
    next_step,
    can_continue,
    finish
)
from loader import thinking


def _normalize_action(raw_action, tools):
    """Normalize planner output to an exact tool name or FINISH.

    Small models often return extra words, quotes, markdown fences,
    different casing, or 'Tool: <name>'. This maps that back to the
    canonical tool name so the loop doesn't try to execute garbage
    and doesn't loop forever without ever hitting FINISH.
    """
    if raw_action is None:
        return ""

    cleaned = str(raw_action).strip()

    # Remove markdown code fences like ```current_time```
    if "```" in cleaned:
        # take content inside fences if present, else drop fences
        parts = cleaned.split("```")
        # prefer the longest non-empty part (usually the code)
        non_empty = [p.strip(" \n\r\t`") for p in parts if p.strip(" \n\r\t`")]
        if non_empty:
            cleaned = max(non_empty, key=len)
        else:
            cleaned = cleaned.replace("```", "")

    # Take first line only, strip surrounding quotes/backticks/whitespace
    cleaned = cleaned.splitlines()[0].strip().strip("\"'` ").strip()
    # Take first whitespace-separated token to drop explanations
    # e.g. "current_time please" -> "current_time"
    if " " in cleaned and cleaned.upper() != "FINISH":
        first = cleaned.split()[0].strip("\"'`(),.:;")
        # If the token looks like a tool name keep it
        if first:
            cleaned = first

    # FINISH check (case-insensitive, tolerant of trailing period)
    if cleaned.strip("\"'` .,;:!").upper() == "FINISH":
        return "FINISH"

    # Exact match first
    for tool in tools:
        if cleaned == tool.name:
            return tool.name

    # Case-insensitive match
    lowered = cleaned.lower()
    for tool in tools:
        if lowered == tool.name.lower():
            return tool.name

    # Substring match for outputs like "Tool: current_time"
    for tool in tools:
        if tool.name.lower() in lowered:
            return tool.name

    return cleaned


async def run_agent_loop(
    user_request,
    planner,
    execute_action,
    format_answer,
    tools,
    client
):

    state = create_state(user_request)
# While can_continue: "This is the heart of our agent.“

    valid_names = [t.name for t in tools]

    while can_continue(state):
#The planner decides what to do next.

        try:
            raw_action = planner(state, tools)
        except Exception as e:
            record_observation(
                state,
                "planner_error",
                f"Planner failed: {e}. If the request is satisfied, return FINISH."
            )
            next_step(state)
            continue

        action = _normalize_action(raw_action, tools)

        print("Planner Selected:", action)

        if action == "FINISH":

            answer = format_answer(state)

            finish(state, answer)

            break

        # Enforce "never repeat" in code, not just in the prompt
        # (small models ignore the prompt and repeat the same tool).
        if action in state["actions"]:
            record_observation(
                state,
                action,
                f"Tool '{action}' was already executed. "
                f"Do NOT select it again. "
                f"Choose a different tool from {valid_names} "
                f"or return FINISH if the request is satisfied."
            )
            next_step(state)
            continue

        # Reject unknown tool names instead of crashing.
        if action not in valid_names:
            record_observation(
                state,
                str(raw_action)[:100],
                f"Unknown tool '{action}'. "
                f"Available tools: {valid_names}. "
                f"Return ONLY the exact tool name or FINISH."
            )
            next_step(state)
            continue

# We execute that action.

        try:
            with thinking(f"Running '{action}'..."):
                observation = await execute_action(
                    action,
                    client
                )
        except Exception as e:
            observation = f"Error executing '{action}': {e}"
# We add that action in state

        add_action(
            state,
            action
        )
#    	We remember what happened.

        record_observation(
            state,
            action,
            observation
        )
#	We move to the next iteration.
     

        next_step(state)

    # Guarantee an answer: if the planner never returned FINISH
    # (e.g. repeated the same tool until max_steps), still answer
    # from whatever observations we have instead of returning "".
    if not state["finished"]:
        try:
            answer = format_answer(state)
        except Exception as e:
            answer = (
                f"I was unable to format a full answer. "
                f"Actions: {state['actions']}. "
                f"Observations: {state['observations']}. "
                f"Error: {e}"
            )
        finish(state, answer)

    return state
