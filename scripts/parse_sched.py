import html, json, re, sys

src, out = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf8").read()
parts = s.split('class="sess-wrap"')[1:]
rows = []
for p in parts:
    p = p[:9000]
    m = re.search(r'data-session-id="(\d+)"', p)
    if not m:
        continue
    def g(pat, flags=re.S):
        x = re.search(pat, p, flags)
        return html.unescape(re.sub(r"<[^>]+>", " ", x.group(1))).strip() if x else ""
    times = re.findall(r'datetime="(\d{4}-\d\d-\d\dT\d\d:\d\d):\d\d"', p)
    tags = [html.unescape(t).strip() for t in re.findall(r'<span class="tag[^"]*">(.*?)</span>', p, re.S)]
    desc = g(r'class="sess__seodesc">(.*?)</div>')
    rows.append({
        "id": m.group(1),
        "title": g(r'class="sess__title">(.*?)</div>'),
        "room": g(r'class="sess__room">(.*?)</span>'),
        "speakers": g(r'class="sess__speakers">(.*?)</span>'),
        "tags": tags,
        "start": times[0] if times else "",
        "end": times[1] if len(times) > 1 else "",
        "desc": re.sub(r"\s+", " ", desc)[:400],
    })
seen = {}
for r in rows:
    seen.setdefault(r["id"], r)
rows = list(seen.values())
json.dump(rows, open(out, "w"), ensure_ascii=False, indent=1)
print(len(rows), "sessions")
