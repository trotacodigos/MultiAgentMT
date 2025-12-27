import json
from pathlib import Path

def load_instruction(
    *,
    version: str,
    role: str,
    template: Path = None,
) -> str:
    if template is None:
        template = Path(__file__) / "template.json"

    with open(template, "r", encoding="utf-8") as f:
        record = json.load(f)

    if record.get("version") != version:
        raise ValueError(f"Version mismatch: {version}")

    if role not in record:
        raise ValueError(f"No instruction for role={role}")

    return record[role]