import matplotlib.pyplot as plt

# ── ANSI colours ─────────────────────────────────────────────────────────────
RED    = "\033[91m"
ORANGE = "\033[38;5;208m"
YELLOW = "\033[93m"
CYAN   = "\033[96m"
GREEN  = "\033[92m"
WHITE  = "\033[97m"
GRAY   = "\033[90m"
BOLD   = "\033[1m"
RESET  = "\033[0m"

BANNER = f"""
        {RED} ______        _  ______  __ {RESET}
        {RED}|  ____|      | ||  ____||  |{RESET}
        {ORANGE}| |__ __ _ ___| || |__   | |{RESET}
        {ORANGE}|  __/ _` / __| ||  __|  | |{RESET}
        {YELLOW}| | | (_| \\__ \\ || |     |_|{RESET}
        {YELLOW}|_|  \\__,_|___/_||_|     (_){RESET}

{WHITE}  Formula 1 Data  {RED}●{WHITE}  Telemetry  {RED}●{WHITE}  Lap Analysis  {RED}●{WHITE}  Race Strategy{RESET}

{GRAY}───────────────────────────────────────────────────────────────────────{RESET}
"""

# ── shared state ─────────────────────────────────────────────────────────────
open_figures: list = []


# ── shared helpers ────────────────────────────────────────────────────────────

def show(fig) -> None:
    """Display a figure non-blocking and track it."""
    open_figures.append(fig)
    plt.show(block=False)
    plt.pause(0.1)


def close_all() -> None:
    plt.close('all')
    open_figures.clear()
    print(GREEN + "  All windows closed." + RESET)


def divider() -> None:
    print(GRAY + "  " + "─" * 55 + RESET)
