from agents.core.call_api import get_one_api
from agents.modules.dispatcher import dispatch_methods, dispatch_params, build_request
from typing import Dict, Any

from rubric_mqm.metric.core import engine


async def run_single_async(
    cfg: Dict[str, Any],
    row: Dict[str, Any],
    task: str,
    ):
    # Different settings for different tasks
    assert task in ("translate", "postedit", "proofread"), f"Unsupported task: {task}"
    
    # Skip processing if translation is already provided and configured to skip
    # This applies to postedit and proofread tasks
    # Note: Both tasks require an existing translation in 'target' to process
    # When skip is enabled, we return the existing translation without further processing
    if task in ("postedit", "proofread"):
        skip_processing = bool(
            cfg.get("skip_translate_if_provided", False) and
            row.get("target") and
            isinstance(row.get("target"), str) and
            row.get("target").strip()
        )
        if skip_processing:
            return row["target"]

    # Generate prompt and make API request
    # Note: postedit uses Rubric-MQM engine for automatic post-editing,
    # while translate and proofread use OpenAI API with different prompts
    if task == "postedit":
        response = engine.run_single(row=row, cfg=cfg)
        return response["data"]["text"]
    else:
        prompter, parser = dispatch_methods(task)
        params = dispatch_params(task, cfg)
        request = build_request(
            src_lang=row["src_lang"],
            tgt_lang=row["tgt_lang"],
            src_text=row["src_text"],
            target=row.get("target", None),
            domain=row.get("domain", None),
            model=cfg["model"]["name"],
            temperature=cfg["model"]["temperature"],
            max_tokens=cfg["model"]["max_tokens"],
            prompter=prompter,
            **params,
        )

        response = await get_one_api(request)
        if task == "translate":
            return response.get("content", "")
        else:
            return parser.parse_response(response, row["target"])