from pathlib import Path
import re, json

# Robust content builder: searches recursively, accepts .md and .markdown (case-insensitive),
# prints diagnostics for debugging when "Built 0" occurs.

BASE = Path(__file__).resolve().parent.parent
CONTENT = BASE / "content"
OUT = BASE / "site" / "assets" / "content-manifest.js"

FRONT_MATTER_RE = re.compile(r"^\ufeff?---\s*\n(.*?)\n---\s*\n([\s\S]*)$", re.DOTALL | re.MULTILINE)

def parse(text):
    m = FRONT_MATTER_RE.search(text)
    if not m:
        return {}, text
    meta = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            meta[k.strip()] = v.strip().strip('"').strip("'")
    return meta, m.group(2).strip()

items = []
found_files = []
if CONTENT.exists():
    # recursive search for markdown files
    for f in sorted(CONTENT.rglob("*")):
        if f.is_file() and f.suffix.lower() in (".md", ".markdown"):
            found_files.append(f)

# Diagnostic output to help when nothing is found
print(f"Content directory: {CONTENT}")
print(f"Found {len(found_files)} candidate markdown file(s):")
for f in found_files:
    print(f" - {f.relative_to(BASE)}")

for f in found_files:
    try:
        text = f.read_text(encoding="utf-8")
    except Exception:
        text = f.read_text(encoding="latin-1")
    meta, body = parse(text)
    if not meta.get("title") or not meta.get("slug"):
        print(f"Skipping {f.relative_to(BASE)}: missing title or slug in front matter")
        continue
    item = {**meta, "markdown": body}
    # normalize commonly used fields
    if "division" in item:
        item["division"] = item["division"].strip()
    items.append(item)

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text("window.TLG_CONTENT = "+json.dumps(items, ensure_ascii=False, indent=2)+";\n", encoding="utf-8")
print(f"Built {len(items)} Markdown document(s). Output: {OUT}")
