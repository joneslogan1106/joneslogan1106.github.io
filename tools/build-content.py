from pathlib import Path
import re, json

CONTENT=Path("content")
OUT=Path("site/assets/content-manifest.js")

def parse(text):
    m=re.match(r"^---\s*\n(.*?)\n---\s*\n([\s\S]*)$",text)
    if not m:return {},text
    meta={}
    for line in m.group(1).splitlines():
        if ":" in line:
            k,v=line.split(":",1)
            meta[k.strip()]=v.strip().strip('"').strip("'")
    return meta,m.group(2).strip()

items=[]
for f in sorted(CONTENT.glob("*.md")):
    meta,body=parse(f.read_text(encoding="utf-8"))
    if not meta.get("title") or not meta.get("slug"): continue
    items.append({**meta,"markdown":body})
OUT.write_text("window.TLG_CONTENT = "+json.dumps(items,ensure_ascii=False,indent=2)+";\n",encoding="utf-8")
print(f"Built {len(items)} Markdown document(s).")
