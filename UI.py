from GUI.py import *
from config.py import *
from main.py import *
from plots.py  import *
from session.py import *
from wdc.py import *
from fastf1 import *

SESSION_PLOTS = {
    "1": ("Speed tracks",      speed_tracks),
    "2": ("Position changes",  position_changes),
    "3": ("Gear shifts",       gear_shifts),
    "4": ("Qualifying result", qualifying_result),
    "5": ("Speed on track",    speed_on_track),
    "6": ("Speed traces",      speed_traces),
    "7": ("Tyre strategy",     plot_strategy),
    "8": ("Team pace ranking", team_pace_ranking),
}

current_session = None

print(BANNER)

    open_count = sum(plt.fignum_exists(f.number) for f in open_figures)
    if open_count:
        print(CYAN + f"  [{open_count} window(s) currently open]\n" + RESET)

    if current_session:
        ev = current_session.event
        print(GREEN + f"  ✓ Session: {ev['EventName']} {ev.year} — {current_session.name}\n" + RESET)
    else:
        print(YELLOW + "  No session loaded — press (s) to choose year / race / session.\n" + RESET)

    for key, (label, _) in SESSION_PLOTS.items():
        print(f"   {key}) {label}")
    print(f"\n   9) WDC standings")
    print(f"   s) {BOLD}Select year / race / session{RESET}")
    print(f"   c) Close all windows")
    print(f"   q) Quit\n")

    choice = input(RESET + "   Choice: ").strip().lower()

    if choice == "s":
        current_session = pick_session()

    elif choice in SESSION_PLOTS:
        if current_session is None:
            print(RED + "\n  Please load a session first (press s).\n" + RESET)
        else:
            SESSION_PLOTS[choice][1](current_session)

    elif choice == "9":
        wdc()

    elif choice == "c":
        close_all()

    elif choice == "q":
        close_all()
        print(YELLOW + "\n  Thanks for using FastF1 Explorer! Bye!\n" + RESET)
        break

    else:
        print(RED + "  Invalid choice, please try again.\n" + RESET)
