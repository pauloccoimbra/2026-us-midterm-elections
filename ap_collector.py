#!/usr/bin/env python3
"""AP Elections API v3 collector -> data/results.json  (TEMPLATE, NOT TESTED: requires a paid AP key)

Usage:
  export AP_API_KEY=...            # your AP key
  python3 ap_collector.py          # loops every 30 s
  python3 ap_collector.py --once   # single collection
Publish data/results.json on the same site as the page (GitHub Pages: commit/push every cycle,
or run on a server that serves the file). The page re-reads the file every 20 s.
Adjust ENDPOINT/parameters to match the docs: https://developer.ap.org/ap-elections-api/
"""
import os, sys, json, time, urllib.request
KEY = os.environ.get("AP_API_KEY", "")
DATE = "2026-11-03"
ENDPOINT = f"https://api.ap.org/v3/elections/{DATE}?officeID=S,G,H&level=state&format=json&apiKey={KEY}"
PM = {"Dem": "D", "GOP": "R"}
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "results.json")

def fetch():
    with urllib.request.urlopen(ENDPOINT, timeout=30) as r:
        return json.load(r)

def convert(j):
    out = {"updated": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "races": {}}
    for r in j.get("races", []):
        off, st = r.get("officeID"), r.get("statePostal")
        if not st or off not in ("S", "G", "H"):
            continue
        key = f"{off}-{st}" if off != "H" else f"H-{st}-{str(r.get('seatNum') or '').zfill(2)}"
        ru = next((u for u in r.get("reportingUnits", []) if u.get("level") == "state"), None)
        if not ru:
            continue
        cands = [{"n": f"{c.get('first','')} {c.get('last','')}".strip(), "p": PM.get(c.get("party"), "I"),
                  "v": int(c.get("voteCount") or 0)} for c in ru.get("candidates", [])]
        win = next((c for c in ru.get("candidates", []) if c.get("winner") == "X"), None)
        e = {"pct": float(ru.get("precinctsReportingPct") or 0), "cands": cands,
             "called": PM.get(win.get("party"), "I") if win else None,
             "calledAt": r.get("lastUpdated") if win else None}
        if off == "H":
            e["name"] = f"{st}-{r.get('seatName','')}"
        out["races"][key] = e
    return out

def once():
    data = convert(fetch())
    tmp = OUT + ".tmp"
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(tmp, "w") as f:
        json.dump(data, f, ensure_ascii=False)
    os.replace(tmp, OUT)
    print(time.strftime("%H:%M:%S"), len(data["races"]), "races")

if __name__ == "__main__":
    if not KEY:
        sys.exit("Set AP_API_KEY")
    while True:
        try:
            once()
        except Exception as e:
            print("error:", e, file=sys.stderr)
        if "--once" in sys.argv:
            break
        time.sleep(30)
