import matplotlib.pyplot as plt
from config import (BANNER, BOLD, RED, CYAN, GREEN, YELLOW, RESET,open_figures, close_all)
from session import pick_session
from plots import (speed_tracks, position_changes, gear_shifts,qualifying_result, speed_on_track, speed_traces,plot_strategy, team_pace_ranking)
from wdc import wdc

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

while True:
    if ui_gui  == "1":
      app = QApplication(sys.argv)
      window = App()
      window.show()
      sys.exit(app.exec())
