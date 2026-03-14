# FastF1 Explorer 🏎️

A terminal-based Formula 1 data visualisation tool powered by the [FastF1](https://docs.fastf1.dev/) library. Browse any season, pick any race, and generate detailed plots — all from an interactive console menu.

---

## Features

| # | Plot | Description |
|---|------|-------------|
| 1 | **Speed tracks** | Fastest lap speed trace with corner annotations |
| 2 | **Position changes** | Driver positions across every lap of the race |
| 3 | **Gear shifts** | Track map coloured by gear for the fastest lap |
| 4 | **Qualifying result** | Horizontal bar chart of gap to pole |
| 5 | **Speed on track** | Track map coloured by speed for a chosen driver |
| 6 | **Speed traces** | Head-to-head speed comparison between two drivers |
| 7 | **Tyre strategy** | Stint lengths and compound choices for all drivers |
| 8 | **Team pace ranking** | Box plot of lap time distribution per team |
| 9 | **WDC standings** | Who can still win the championship after a given round |

Multiple plot windows can be open simultaneously — loading a new plot never closes the previous ones.

---

## Project structure

```
fastf1_explorer/
├── main.py       ← Entry point — run this
├── config.py     ← ANSI colours, banner, shared state and helpers
├── session.py    ← Interactive year / race / session picker
├── plots.py      ← All 8 plot functions
└── wdc.py        ← WDC championship standings
```

---

## Requirements

- Python 3.10+
- Dependencies:

```bash
pip install fastf1 matplotlib numpy pandas seaborn timple
```

---

## Installation

```bash
git clone https://github.com/your-username/fastf1-explorer.git
cd fastf1-explorer
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install fastf1 matplotlib numpy pandas seaborn timple
```

---

## Usage

```bash
python main.py
```

On launch you will see the main menu. No session is loaded by default.

### Step 1 — Load a session

Press `s` to open the session picker:

1. **Choose a year** — seasons from 2018 to 2025
2. **Choose a race** — the full calendar for that year is fetched live, with dates
3. **Choose a session type** — Race, Qualifying, Sprint, FP1/2/3, etc.

The session is downloaded and cached locally by FastF1. Subsequent loads of the same session are instant.

### Step 2 — Pick a plot

Enter the number of the plot you want. Some plots (Speed on track, Speed traces) will ask you to select one or two drivers from a list before rendering.

### Other controls

| Key | Action |
|-----|--------|
| `s` | Load / switch session |
| `c` | Close all open plot windows |
| `q` | Quit |

---

## FastF1 cache

FastF1 caches session data locally to avoid re-downloading. By default the cache is stored in the working directory. To set a custom path, add this at the top of `main.py`:

```python
import fastf1
fastf1.Cache.enable_cache('/path/to/cache')
```

---

## Notes

- **WDC standings** (option 9) does not require a session to be loaded — it fetches data directly from the Ergast API.
- Some plots (qualifying result, gear shifts, speed traces) are designed for **Qualifying** sessions. Running them on a Race session will still work but results may be less meaningful.
- If a driver has no recorded laps (DNS / immediate DNF), they are automatically skipped in position change plots.
