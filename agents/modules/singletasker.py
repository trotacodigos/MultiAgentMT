from agents.core.call_api import get_one_api
from agents.modules.dispatcher import dispatch_methods, dispatch_params, build_request
from typing import Dict, Any

from rubric_mqm.metric.modules import ape


async def run_single_async(
    cfg: Dict[str, Any],
    row: Dict[str, Any],
    ):
    # Different settings for different tasks
    task = cfg["task"]
    assert task in ("translate", "postedit", "proofread"), f"Unsupported task: {task}"
    prompter, parser = dispatch_methods(task)
    params = dispatch_params(task, cfg)

    # Generate prompt and make API request
    if task == "postedit":
        request = ape.postedit(
            src_lang=row["src_lang"],
            tgt_lang=row["tgt_lang"],
            src_text=row["src_text"],
            target=row.get("target", None),
            model=cfg["model"]["name"],
            temperature=cfg["model"]["temperature"],
            max_tokens=cfg["model"]["max_tokens"],
            ref_text=row.get("ref_text"),
        )
    else:
        request = build_request(
            task=cfg["task"],
            src_lang=row["src_lang"],
            tgt_lang=row["tgt_lang"],
            src_text=row["src_text"],
            target=row.get("target", None),
            model=cfg["model"]["name"],
            temperature=cfg["model"]["temperature"],
            max_tokens=cfg["model"]["max_tokens"],
            prompter=prompter,
            **params,
        )

    response = await get_one_api(request)
    if task == "translate":
        return response
    else:
        return parser.parse_response(response, row["target"])