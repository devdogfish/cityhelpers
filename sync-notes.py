from pathlib import Path
from datetime import date
root = Path(__file__).resolve().parent
for source, output, title in [
    ("OBJECTIVE.md", "objective.md", "Business problem and objective"),
    ("TARGET_AUDIENCE.md", "target-audience.md", "Target audience"),
    ("CONTEXT.md", "context.md", "Business context"),
]:
    text = (root.parent / source).read_text()
    if text.startswith("# "):
        text = text.split("\n", 1)[1].lstrip()
    (root / output).write_text(f"---\ntitle: {title}\nupdated: {date.today().isoformat()}\n---\n\n{text}")
    print(f"Synced {source}")
