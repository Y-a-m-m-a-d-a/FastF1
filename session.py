import fastf1
from config import (RED, YELLOW, CYAN, GREEN, WHITE, BOLD, RESET, divider)

SESSION_TYPES = {
    "1": ("Race",              "R"),
    "2": ("Qualifying",        "Q"),
    "3": ("Sprint",            "S"),
    "4": ("Sprint Qualifying", "SQ"),
    "5": ("Practice 1",        "FP1"),
    "6": ("Practice 2",        "FP2"),
    "7": ("Practice 3",        "FP3"),
}


def pick_session():
    """Interactive three-step picker: year → race → session type.
    Returns a loaded fastf1.Session, or None on failure."""

    # ── year ──────────────────────────────────────────────────────────────────
    print(f"\n{BOLD}{WHITE}  ── Select year ──{RESET}")
    years = list(range(2025, 2017, -1))
    for i, y in enumerate(years, 1):
        print(f"  {CYAN}{i:>2}{RESET}) {y}")
    divider()

    while True:
        raw = input(f"  Year (1-{len(years)}): ").strip()
        if raw.isdigit() and 1 <= int(raw) <= len(years):
            year = years[int(raw) - 1]
            break
        print(RED + "  Invalid choice." + RESET)

    # ── race ──────────────────────────────────────────────────────────────────
    print(f"\n{BOLD}{WHITE}  ── Fetching {year} calendar … ──{RESET}")
    try:
        schedule = fastf1.get_event_schedule(year, include_testing=False)
    except Exception as e:
        print(RED + f"  Could not fetch calendar: {e}" + RESET)
        return None

    events = schedule[["RoundNumber", "EventName", "EventDate", "Country"]].copy()
    events = events[events["RoundNumber"] > 0].reset_index(drop=True)

    print(f"\n{BOLD}{WHITE}  ── Select race ──{RESET}")
    for _, row in events.iterrows():
        date_str = str(row["EventDate"])[:10]
        print(f"  {CYAN}{int(row['RoundNumber']):>2}{RESET}) "
              f"{row['EventName']:<35} {RESET}{date_str}")
    divider()

    max_round = int(events["RoundNumber"].max())
    while True:
        raw = input(f"  Round (1-{max_round}): ").strip()
        if raw.isdigit() and 1 <= int(raw) <= max_round:
            round_num  = int(raw)
            event_name = events.loc[events["RoundNumber"] == round_num, "EventName"].values[0]
            break
        print(RED + "  Invalid choice." + RESET)

    # ── session type ──────────────────────────────────────────────────────────
    print(f"\n{BOLD}{WHITE}  ── Select session type ──{RESET}")
    for key, (label, _) in SESSION_TYPES.items():
        print(f"  {CYAN}{key}{RESET}) {label}")
    divider()

    while True:
        raw = input("  Session type: ").strip()
        if raw in SESSION_TYPES:
            session_label, session_code = SESSION_TYPES[raw]
            break
        print(RED + "  Invalid choice." + RESET)

    # ── load ──────────────────────────────────────────────────────────────────
    print(f"\n{YELLOW}  Loading {event_name} {year} — {session_label} …{RESET}\n")
    try:
        session = fastf1.get_session(year, round_num, session_code)
        session.load()
    except Exception as e:
        print(RED + f"  Failed to load session: {e}" + RESET)
        return None

    print(GREEN + f"  ✓ Ready: {event_name} {year} — {session_label}\n" + RESET)
    return session
