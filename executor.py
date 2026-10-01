from mcp_client import execute_tool


async def execute_action(action, client):

    result = await execute_tool(
        client,
        action
    )

    if hasattr(result, "content"):

        if result.content:
            texts = []
            for item in result.content:
                if hasattr(item, "text") and item.text is not None:
                    texts.append(str(item.text))
                elif isinstance(item, str):
                    texts.append(item)
            if texts:
                return "\n".join(texts)

    return str(result)
