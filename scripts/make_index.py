"""Wrap planner.html in a full HTML document so it opens straight from disk.

planner.html is written as an artifact fragment (no <html>/<head>/<body>), which is what
claude.ai publishes. Usage: python3 scripts/make_index.py  ->  index.html
Saving to your account only works on claude.ai; opened from disk the page keeps your plan in
this browser's local storage.
"""
import os

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
body = open(os.path.join(root, "planner.html"), encoding="utf8").read()
doc = (
    '<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
    '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n'
    "</head>\n<body>\n" + body + "\n</body>\n</html>\n"
)
open(os.path.join(root, "index.html"), "w", encoding="utf8").write(doc)
print("wrote index.html")
