from agents.core.call_api import get_one_api
from agents.modules.singletasker import run_single_async
from agents.parser.parse import parse_response

from typing import Dict, Any


async def run_multi_async(
        cfg: Dict[str, Any],
        row: Dict[str, Any],
        task = "multi",
) -> str:
    """
    Multi-agent Framework: translate -> postedit -> proofread
    """
    tasks = ("translate", "postedit", "proofread")

    for task in tasks:
        cfg["model"]["name"] = cfg["model"][task]["name"]
        cfg["model"]["temperature"] = cfg["model"][task]["temperature"]
        cfg["model"]["max_tokens"] = cfg["model"][task]["max_tokens"]

        response = await run_single_async(cfg, row, task)

        if not response:
            return response
        row["target"] = response

    return response
