import fastf1
from fastf1.ergast import Ergast

from config import (RED, CYAN, GREEN, WHITE, GRAY, BOLD, RESET, divider)


def wdc() -> None:
    print(f"\n{BOLD}{WHITE}  ── WDC standings ──{RESET}")

    while True:
        raw = input("  Season year (2018-2025): ").strip()
        if raw.isdigit() and 2018 <= int(raw) <= 2025:
            SEASON = int(raw)
            break
        print(RED + "  Enter a year between 2018 and 2025." + RESET)

    while True:
        raw = input("  After round: ").strip()
        if raw.isdigit() and 1 <= int(raw) <= 24:
            ROUND = int(raw)
            break
        print(RED + "  Enter a round between 1 and 24." + RESET)

    try:
        ergast    = Ergast()
        standings = ergast.get_driver_standings(season=SEASON, round=ROUND).content[0]
    except Exception as e:
        print(RED + f"  Could not fetch standings: {e}" + RESET)
        return

    POINTS_FOR_SPRINT       = 8 + 25
    POINTS_FOR_CONVENTIONAL = 25

    events     = fastf1.events.get_event_schedule(SEASON, backend='ergast')
    events     = events[events['RoundNumber'] > ROUND]
    max_points = (
        len(events.loc[events["EventFormat"] == "sprint_shootout"]) * POINTS_FOR_SPRINT
        + len(events.loc[events["EventFormat"] == "conventional"]) * POINTS_FOR_CONVENTIONAL
    )

    leader_points = int(standings.loc[0]['points'])
    print(f"\n{CYAN}  WDC after Round {ROUND} — {SEASON}{RESET}")
    print(f"{GRAY}  {'Pos':<5} {'Driver':<25} {'Pts':>6} {'Max':>6} {'Can win?':>10}{RESET}")
    divider()

    for i, _ in enumerate(standings.iterrows()):
        drv        = standings.loc[i]
        driver_max = int(drv['points']) + max_points
        can_win    = GREEN + 'Yes' + RESET if driver_max >= leader_points else RED + 'No' + RESET
        full_name  = f"{drv['givenName']} {drv['familyName']}"
        print(f"  {int(drv['position']):<5} {full_name:<25} {int(drv['points']):>6} {driver_max:>6}   {can_win}")
    print()
