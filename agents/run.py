import argparse
import pandas as pd
import yaml
import asyncio

from agents.core.engine import run_batch_async


def main():
    parser = argparse.ArgumentParser(
        description="Multi-agent MT system"
    )
    parser.add_argument(
        "--task",
        choices=["translate", "postedit", "proofread", "multi"],
        required=True,
        help="Running task: single-task (translate, postedit, proofread) or multi-task (multi)",
    )
    parser.add_argument("--input", required=True, help="Input CSV")
    parser.add_argument("--output", required=True, help="Output file (csv/jsonl)")
    parser.add_argument("--config", default="metric/config/default.yaml")
    args = parser.parse_args()

    with open(args.config, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)

    df = pd.read_csv(args.input)

    asyncio.run(
        run_batch_async(
            df=df, 
            cfg=cfg,
            task=args.task,
            output_path=args.output,
        )
    )

if __name__ == "__main__":
    main()