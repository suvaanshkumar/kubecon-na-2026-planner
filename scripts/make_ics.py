"""Build kubecon-2026-plan.ics from the default plan inside planner.html.

Usage: python3 scripts/make_ics.py [output.ics]
Needs node. The planner's own script supplies entries(), leaveBy() and the default items,
and ics_tail.js turns them into iCalendar text (America/Denver, i.e. MST in November).
"""
import os
import re
import subprocess
import sys
import tempfile

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
out = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.path.join(root, "kubecon-2026-plan.ics")

html = open(os.path.join(root, "planner.html"), encoding="utf8").read()
js = re.search(r"<script>(.*)</script>", html, re.S).group(1)
tail = open(os.path.join(root, "scripts", "ics_tail.js"), encoding="utf8").read()
stub = (
    'const document={querySelector:()=>({innerHTML:"",textContent:"",value:"",focus(){},setSelectionRange(){}}),'
    "addEventListener(){},activeElement:null};\n"
    "const window={};const localStorage={getItem(){return null},setItem(){}};\n"
)

with tempfile.TemporaryDirectory() as tmp:
    gen = os.path.join(tmp, "gen_ics.js")
    open(gen, "w", encoding="utf8").write(stub + js + tail)
    subprocess.run(["node", gen], check=True, env={**os.environ, "ICS_OUT": out})
