from agents.core.call_api import get_one_api
from agents.modules.singletasker import run_single_async
from agents.parser.parse import parse_response

from typing import Dict, Any


async def run_multi_async(
        cfg: Dict[str, Any],
        row: Dict[str, Any],
) -> str:
    """
    Multi-agent Framework: translate -> postedit -> proofread
    
    :param cfg: Configuration dictionary containing model and task settings
    :param row: A dictionary representing a single data row with source and target texts

    :return: Final processed text after all tasks
    """
    tasks = ("translate", "postedit", "proofread")

    for task in tasks:
        cfg["model"]["name"] = cfg["model"][task]["name"]
        cfg["model"]["temperature"] = cfg["model"][task]["temperature"]
        cfg["model"]["max_tokens"] = cfg["model"][task]["max_tokens"]

        response = await run_single_async(cfg, row)

        if not response:
            return response
        row["target"] = response
        
    return response
