import csv
import json
import asyncio
from typing import Dict, Any, Optional

import pandas as pd
from tqdm import tqdm



async def run_batch_async(
    df: pd.DataFrame,
    cfg: Dict[str, Any],
    tasker: str, # "single" or "multi"
    output_path: Optional[str] = None,
    progress_callback=None,
):
    # Decide the type of agents
    if tasker == "single":
        from remote.agents.modules.singletasker import run_single_async as run_single
    if tasker == "multi":
        from remote.agents.modules.multitasker import run_multi_async as run_single
    else:
        raise ValueError(f"Unsupported tasker: {tasker}")

    required_cols = ["src_lang", "tgt_lang", "src_text", "target"]
    if tasker == "single" and cfg["task"] == "translate":
        required_cols.remove("target")

    if not all(col in df.columns for col in required_cols):
        raise ValueError(f"Missing required columns: {required_cols}")
    
    rows = [row.to_dict() for _, row in df.iterrows()]
    is_jsonl = output_path and output_path.endswith(".jsonl")

    results = []
    coros = [run_single(cfg, row) for row in rows]
    for idx, coro in enumerate(
        tqdm(
            asyncio.as_completed(coros),
            total=len(coros),
            ncols=100,
            colour="cyan",
        )
    ):
        result = await coro
        results.append(result)

        if progress_callback:
            progress_callback(idx)
        
        if output_path:
            with open(
                output_path,
                "a",
                encoding="utf-8",
                newline="" if not is_jsonl else None,
            ) as f:
                if is_jsonl:
                    f.write(json.dumps(result, ensure_ascii=False) + "\n")
                else:
                    writer = csv.DictWriter(f, fieldnames=result.keys())
                    writer.writeheader()
                    for result in results:
                        writer.writerow(result)
    return results