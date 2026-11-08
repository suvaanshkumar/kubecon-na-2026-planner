# KubeCon NA 2026 planner

A single-page planner for KubeCon + CloudNativeCon North America 2026 (Salt Lake City, Nov 9 to 12, times in MST).
It holds booth shifts, a lightning talk and the sessions you want to attend, flags overlaps and tight walks, shows
when to leave your hotel, and keeps a list of session videos to watch afterwards. Every card links to the official
session page and has an "Add to Google Calendar" link.

The default plan is one attendee's, built around the OCM lightning talk, two project kiosk shifts and sessions on
OCM, large-fleet management and disaster recovery. Edit the entries in `DEFAULT_ITEMS` and `PICKS` in `planner.html`
to make it yours.

## What is in here

| Path | What it is |
|---|---|
| `planner.html` | The page, as a fragment in the format claude.ai publishes as an Artifact. |
| `scripts/make_index.py` | Wraps `planner.html` into `index.html` so it opens from disk. |
| `scripts/make_ics.py` | Builds `kubecon-2026-plan.ics` (America/Denver) from the default plan. Needs node. |
| `scripts/parse_sched.py` | Parses the official schedule HTML into `data/sessions.json`. |
| `data/sessions.json` | 600 sessions (id, title, room, times, tags, short description) from the public schedule, pulled 2026-11-07. |
| `scripts/build_catalog.py` | Picks the sessions the planner offers from `data/sessions.json` and writes `data/catalog.js`. |
| `data/catalog.js` | The generated catalog that is pasted into `planner.html`. |

## Rebuilding

1. Download the schedule: `curl -L -o schedule.html https://events.linuxfoundation.org/kubecon-cloudnativecon-north-america/program/schedule/`
2. `python3 scripts/parse_sched.py schedule.html data/sessions.json`
3. `python3 scripts/build_catalog.py data` reads `data/sessions.json` and writes `data/catalog.js`. Paste it over the `const C=[...]` block in `planner.html` (this step is manual).
4. `python3 scripts/make_index.py` and `python3 scripts/make_ics.py`.

## Things that are estimates

- Walking and travel times. The Hyatt Regency is connected to the Salt Palace (listings give about a 1 minute walk). The hotel to venue and hotel to airport times are editable in the Trip panel.
- Session video links are YouTube searches, because recordings were not published when this was made.
- Saving to an account only works when the page is published on claude.ai. Opened from disk it keeps your plan in the browser's local storage.

The schedule data comes from the public KubeCon + CloudNativeCon NA 2026 schedule. Rooms and times can still change, so recheck the official schedule.
