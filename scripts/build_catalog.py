import json, re, sys

sp = sys.argv[1]
rows = {r["id"]: r for r in json.load(open(sp + "/sessions.json"))}
DAY = {"11-08": "sun", "11-09": "mon", "11-10": "tue", "11-11": "wed", "11-12": "thu"}

# (id, track, suggested, why)
SPEC = [
 ("1289834", "DR", 0, "Stateful database DR background."),
 ("1289875", "DR", 1, "Chaos testing for failover. Same room as your talk."),
 ("1289881", "DR", 1, "Cross-cluster traffic failover, right before your talk."),
 ("1289885", "Multicluster", 1, "Placement and failover, two minutes after your talk. Stay in the room."),
 ("1289909", "DR", 1, "Storage replication."),
 ("1289913", "DR", 1, "Backup and restore."),
 ("1334788", "Fleet scale", 1, "Cluster lifecycle as an API, in the Showcase hall next to the kiosks."),
 ("1250350", "Fleet scale", 0, "Cluster allocation and utilization."),
 ("1223002", "GitOps", 1, "GitOps at fleet scale."),
 ("1247848", "Multicluster", 1, "Meet the speakers. A kubectl proxy over a hub-managed fleet. Ask what ports to OCM."),
 ("1243723", "Multicluster", 1, "AMA with August Simonelli (OCM) and Laura Lorenz (SIG-Multicluster)."),
 ("1250559", "Fleet scale", 1, "Blast radius of a GitOps prune across 39 clusters."),
 ("1289629", "DR", 0, "DR community contacts. Overlaps GitOps Meltdown."),
 ("1360829", "GitOps", 1, "Fleet GitOps in 5 minutes, same area as the 11:50 session."),
 ("1247840", "Fleet scale", 1, "Safe rollout across clusters."),
 ("1289700", "DR", 0, "Outage resilience. Overlaps Ship Faster."),
 ("1247641", "Fleet scale", 1, "Fixing 5,000+ nodes in minutes (5 min), in the Hyatt. Leave by 3:05 to reach the kiosk by 3:20."),
 ("1229970", "Fleet scale", 0, "An LLM driving 30 EKS clusters. Overlaps your kiosk arrival."),
 ("1249894", "Multicluster", 0, "Placement across clusters for one GPU pool. Overlaps your kiosk shift."),
 ("1289702", "Multicluster", 0, "Karmada, full session. Overlaps your kiosk shift."),
 ("1336101", "Multicluster", 0, "Istio multicluster discovery. Overlaps your kiosk shift."),
 ("1362689", "DR", 0, "Day 2 stateful data services demo. Overlaps your kiosk shift."),
 ("1293929", "Fleet scale", 1, "Cluster API in 5 minutes, just before your OCM kiosk."),
 ("1248788", "Fleet scale", 0, "1000 clusters at Salesforce. Overlaps your OCM kiosk, so read the slides."),
 ("1248779", "Multicluster", 0, "Cross-cluster discovery after failover. Overlaps your OCM kiosk."),
 ("1289712", "Multicluster", 0, "SIG-Multicluster. Starts 5 min before your OCM kiosk ends and runs into your 12:15 arrival."),
 ("1249027", "Multicluster", 0, "Unified workload API for multi-cluster. Overlaps the last 10 min of your kiosk."),
 ("1289726", "DR", 1, "DR and backup standards. After your KubeVela shift."),
 ("1289722", "DR", 1, "Storage replication deep dive."),
 ("1375121", "Multicluster", 0, "The schedule text mentions Open Cluster Management."),
]

def clean(t):
    return re.sub(r"\s+", " ", t).strip()

def loc(room):
    return clean(re.sub(r"\s*\|\s*", ", ", room))

cat = []
for sid, track, pick, why in SPEC:
    r = rows[sid]
    d = DAY[r["start"][5:10]]
    cat.append({
        "id": sid, "day": d, "start": r["start"][11:16], "end": r["end"][11:16],
        "title": clean(r["title"]), "loc": loc(r["room"]), "why": why,
        "track": track, "pick": bool(pick),
    })
order = {"sun": 0, "mon": 1, "tue": 2, "wed": 3, "thu": 4}
cat.sort(key=lambda c: (order[c["day"]], c["start"]))

js = "const C=" + json.dumps(cat, ensure_ascii=False, indent=0) + ";\n"
js += "const CAT=Object.fromEntries(C.map(s=>[s.id,s]));\n"
js += "const PICKS=new Set(C.filter(s=>s.pick).map(s=>s.id));\n"
js += "const LINK=id=>\"https://events.linuxfoundation.org/kubecon-cloudnativecon-north-america/program/schedule/?id=\"+id;\n"
open(sp + "/catalog.js", "w", encoding="utf8").write(js)
print(len(cat), "catalog entries,", sum(1 for c in cat if c["pick"]), "suggested")
