from agents.core.call_api import get_one_api
from agents.modules.dispatcher import dispatch_methods, dispatch_params, build_request
from typing import Dict, Any
import math

from rubric_mqm.metric.core import engine


def _is_empty_target(value) -> bool:
    """Check if target value is empty (None, empty string, whitespace-only, or NaN)"""
    if value is None:
        return True
    if isinstance(value, str) and not value.strip():
        return True
    try:
        # Check if it's NaN (works for float nan from pandas)
        if math.isnan(value):
            return True
    except (TypeError, ValueError):
        pass
    return False


async def run_single_async(
    cfg: Dict[str, Any],
    row: Dict[str, Any],
    task: str,
    ):
    # Different settings for different tasks
    assert task in ("translate", "postedit", "proofread"), f"Unsupported task: {task}"

    row_ = dict(row)  # Make a copy to avoid modifying the original

    # If target is not provided for proofread/postedit task, invoke translate agent first
    if task in ("proofread", "postedit") and _is_empty_target(row_.get("target")):
        translation = await run_single_async(cfg, row_, "translate")
        if _is_empty_target(translation):
            raise ValueError("Translate returned empty target; aborting to avoid infinite recursion.")
        row_["target"] = translation
            
    if task == "postedit":
        response = engine.run_single(row=row_, cfg=cfg)
        return response["data"]["text"]
    elif task in ("translate", "proofread"):
        prompter, parser = dispatch_methods(task)
        params = dispatch_params(task, cfg)
        request = build_request(
            src_lang=row_["src_lang"],
            tgt_lang=row_["tgt_lang"],
            src_text=row_["src_text"],
            target=row_.get("target", None),
            domain=row_.get("domain", None),
            model=cfg["model"]["name"],
            temperature=cfg["model"]["temperature"],
            max_tokens=cfg["model"]["max_tokens"],
            prompter=prompter,
            **params,
        )
    else:
        raise ValueError(f"Unsupported task: {task}")
        
    response = await get_one_api(request)
    if task == "translate":
        return response.get("content", "")
    else:
        return parser.parse_response(response, row_["target"])