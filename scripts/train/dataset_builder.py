import json
import os
from pathlib import Path

"""
Build a simple instruction-tuning dataset from existing n8n workflows.
Output: data/dataset.jsonl with lines: {"prompt": str, "workflow": {...}}
"""

WORKFLOWS_DIR = Path("workflows")
OUTPUT_DIR = Path("data")
OUTPUT_FILE = OUTPUT_DIR / "dataset.jsonl"


def infer_prompt_from_workflow(wf: dict) -> str:
    name = wf.get("name")
    if name and isinstance(name, str) and len(name.strip()) > 8:
        return name.strip()

    nodes = wf.get("nodes", [])
    if not nodes:
        return "Create a simple automation"

    # Try to derive trigger and action names
    trigger = None
    actions = []
    for n in nodes:
        t = n.get("type", "")
        if "Trigger" in n.get("name", "") or t.endswith("Trigger") or \
           t.endswith(".webhook") or t.endswith(".manualTrigger"):
            trigger = n
        else:
            actions.append(n)

    def clean_name(n):
        return n.get("name", "Node").replace("Node ", "").strip()

    if trigger and actions:
        tname = clean_name(trigger)
        anames = ", ".join(clean_name(a) for a in actions[:2])
        return f"{anames} when {tname} fires"

    # Fallback: list two nodes
    listed = ", ".join(clean_name(n) for n in nodes[:2])
    return f"Connect {listed} in a simple workflow"


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    count = 0
    with OUTPUT_FILE.open("w", encoding="utf-8") as out:
        for root, _, files in os.walk(WORKFLOWS_DIR):
            for fname in files:
                if not fname.lower().endswith(".json"):
                    continue
                fpath = Path(root) / fname
                try:
                    with open(fpath, "r", encoding="utf-8") as f:
                        data = json.load(f)
                    # Some files may wrap the workflow differently; try keys
                    wf = data
                    if isinstance(data, dict) and "nodes" not in data and "workflow" in data:
                        wf = data["workflow"]
                    if not isinstance(wf, dict) or "nodes" not in wf:
                        continue
                    prompt = infer_prompt_from_workflow(wf)
                    out.write(json.dumps({"prompt": prompt, "workflow": wf}, ensure_ascii=False) + "\n")
                    count += 1
                except Exception:
                    # Ignore malformed files
                    continue
    print(f"Wrote {count} examples to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
