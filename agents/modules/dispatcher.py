from typing import Dict, Any

from agents.prompt import translate
from agents.prompt import proofread
from agents.parser import parse as proofread_parser


def dispatch_methods(task: str) -> tuple:
    prompter_by_task = {
        "translate": translate,
        "proofread": proofread,
    }
    parser_by_task = {
        "translate": None,
        "proofread": proofread_parser,
    }

    prompter = prompter_by_task.get(task)
    parser = parser_by_task.get(task)

    if not prompter or (parser is None and task != "translate"):
        raise ValueError(f"Unsupported task: {task}")
    
    return prompter, parser


def dispatch_params(task: str, cfg: dict) -> dict:

    if task == "translate":
        return {}
    elif task == "proofread":
        return {"version": cfg["prompt"]["version"]}
    else:
        raise ValueError(f"Unsupported task: {task}")


def build_request(
    *,
    src_lang: str,
    tgt_lang: str,
    src_text: str,
    target: str,
    model: str,
    temperature: float,
    max_tokens: int,
    prompter: callable,
    **params,
) -> Dict[str, Any]:

    messages = prompter.gen_message(
        src_lang=src_lang,
        tgt_lang=tgt_lang,
        src_text=src_text,
        target=target,
        **params,
    )

    return {
        "request": {
            "model": model,
            "messages": messages,
        },
        "temperature": temperature,
        "max_tokens": max_tokens,
    }