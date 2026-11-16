# US Midterm Elections 2026 · Live Results

> Live results dashboard for the 2026 US midterm elections (Nov 3, 2026): Senate, House and governors, state map, key races and remaining-vote analysis. Plain HTML/JS, no dependencies.

**Author:** Paulo C. Coimbra · **License:** MIT

**Keywords:** 2026 midterm elections, US midterms, live election results, election night, Senate, House, governors, election map.

## What it shows
Control scoreboard (Senate: majority is 51, or 50 with the vice president's vote; governors: 26 of 50; House: 218 of 435), geographic map and tile-grid map by state (click a state to open its county map), key races, full table, party flips, surprises against consensus, paths to Senate control, remaining votes in races being counted, timeline of calls and the poll-closing schedule (ET and the visitor's local time). The first-polls countdown ends when counting starts.

## Publish on GitHub Pages
1. The repository is https://github.com/pauloccoimbra/2026-us-midterm-elections (create it empty on GitHub and push these files, see below).
2. Settings > Pages > Deploy from a branch > `main` / `(root)`.
3. Address: `https://pauloccoimbra.github.io/2026-us-midterm-elections/`

```bash
cd 2026-us-midterm-elections
git init -b main
git add .
git commit -m "US Midterm Elections 2026: first version"
git remote add origin https://github.com/pauloccoimbra/2026-us-midterm-elections.git
git push -u origin main
```

## Visit counter
The page uses GoatCounter (code `2026-us-midterm-elections`, dashboard at https://2026-us-midterm-elections.goatcounter.com). GoatCounter sets no cookies and stores no personal data. Create the site with that code at goatcounter.com before publishing.

## Feeding it data
The page re-reads `data/results.json` every 20 s. Ways to update it:

| Path | How |
|---|---|
| AP collector (needs a paid key) | `export AP_API_KEY=...; bash publish_loop.sh` (collects and runs `git push` every 60 s) |
| GitHub Actions | `.github/workflows/collect.yml`: create the `AP_API_KEY` secret and the variable `COLLECT_ENABLED=true` |
| Manual entry | "Sources and data" panel on the page itself (stays in the browser only) |
| Another source | A JSON URL in the panel, or import a file |

County results are optional: add `"counties": {"<5-digit FIPS>": {"pct": 88, "cands": [...]}}` to a race and its county map is shaded by the leader's margin.

JSON format (keys `S-ST`, `G-ST`, `H-ST-NN`; `p` = D, R or I):

```json
{ "updated": "2026-11-03T23:45:00Z",
  "races": { "S-GA": { "pct": 41.2, "cands": [{"n":"Jon Ossoff","p":"D","v":812345},{"n":"Mike Collins","p":"R","v":790120}], "called": null } } }
```

Optional extras in the same file: a race can carry `"note": "..."` (shown in its detail panel), and the top level can carry `"houseTotals": {"D":258,"R":177,"source":"NBC News","asOf":"..."}` to display a media-projected House total instead of counting only the districts listed.

## Data snapshot included (Nov 16, 2026)
`data/results.json` was compiled by hand from published news coverage (AP figures as relayed by news sites), not from the AP feed:
- Senate: 34 of 35 races called; Alaska was not called by the AP in the latest source (Peltola 49.9% x Sullivan 46.0%, ~97% counted, Nov 13). Democrats 55, Republicans 44.
- Governors: all 36 called (Democrats 30, Republicans 20 including seats not up). Vote counts for 15 states are from Nov 4 (about 9:25 AM ET) and are partial; the other states have calls only.
- House: totals from the AP count as of Nov 14, 12:01 AM ET (D 256, R 169, 10 uncalled), plus 21 individually entered districts.
Replace the file with a fresh feed or certified results whenever available; confirm every number at the state election authorities.

## Rehearsal
In the "Sources and data" panel, turn on **Demo** (fictional data, with a permanent warning) and drag the timeline.

## Limitations
- "Calls" are media/AP projections, not official results. Official results come after each state certifies; there is no single national portal.
- `ap_collector.py` and the AP v3 reader have not been tested with a real key.
- Consensus = numeric average of forecasters' ratings (Wikipedia, Sept. 2026). Candidates checked on Nov 2, 2026 (Rhode Island: Foulkes, Guckian and Block).
- Remaining votes: estimate based on the declared % reporting, ignoring geographic differences.
- The House only counts called districts (no baseline).
- State links go to the election authorities' sites; confirm them on election night.
