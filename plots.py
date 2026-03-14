import matplotlib as mpl
import matplotlib.pyplot as plt
import fastf1
import fastf1.plotting
import numpy as np
import pandas as pd
import seaborn as sns
from fastf1.core import Laps
from timple.timedelta import strftimedelta
from matplotlib import colormaps
from matplotlib.collections import LineCollection

from config import (RED, CYAN, WHITE, BOLD, RESET, show, divider)


def speed_tracks(session) -> None:
    fastf1.plotting.setup_mpl(mpl_timedelta_support=True, color_scheme='fastf1')

    fastest_lap  = session.laps.pick_fastest()
    car_data     = fastest_lap.get_car_data().add_distance()
    circuit_info = session.get_circuit_info()
    team_color   = fastf1.plotting.get_team_color(fastest_lap['Team'], session=session)

    fig, ax = plt.subplots()
    ax.plot(car_data['Distance'], car_data['Speed'],
            color=team_color, label=fastest_lap['Driver'])

    v_min, v_max = car_data['Speed'].min(), car_data['Speed'].max()
    ax.vlines(circuit_info.corners['Distance'],
              ymin=v_min - 20, ymax=v_max + 20,
              linestyles='dotted', colors='grey')

    for _, corner in circuit_info.corners.iterrows():
        ax.text(corner['Distance'], v_min - 30,
                f"{corner['Number']}{corner['Letter']}",
                va='center_baseline', ha='center', size='small')

    ax.set_xlabel('Distance in m')
    ax.set_ylabel('Speed in km/h')
    ax.set_ylim([v_min - 40, v_max + 20])
    ax.legend()
    show(fig)


def position_changes(session) -> None:
    fastf1.plotting.setup_mpl(mpl_timedelta_support=False, color_scheme='fastf1')

    fig, ax = plt.subplots(figsize=(8.0, 4.9))
    for drv in session.drivers:
        drv_laps = session.laps.pick_drivers(drv)
        if drv_laps.empty:
            continue
        abb   = drv_laps['Driver'].iloc[0]
        style = fastf1.plotting.get_driver_style(
            identifier=abb, style=['color', 'linestyle'], session=session)
        ax.plot(drv_laps['LapNumber'], drv_laps['Position'], label=abb, **style)

    ax.set_ylim([20.5, 0.5])
    ax.set_yticks([1, 5, 10, 15, 20])
    ax.set_xlabel('Lap')
    ax.set_ylabel('Position')
    ax.legend(bbox_to_anchor=(1.0, 1.02))
    plt.tight_layout()
    show(fig)


def gear_shifts(session) -> None:
    lap = session.laps.pick_fastest()
    tel = lap.get_telemetry()

    points   = np.array([tel['X'].values, tel['Y'].values]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)
    gear     = tel['nGear'].to_numpy().astype(float)

    cmap = colormaps['Paired']
    lc   = LineCollection(segments, norm=plt.Normalize(1, cmap.N + 1), cmap=cmap)
    lc.set_array(gear)
    lc.set_linewidth(4)

    fig, ax = plt.subplots()
    ax.add_collection(lc)
    ax.axis('equal')
    ax.tick_params(labelleft=False, left=False, labelbottom=False, bottom=False)
    fig.suptitle(f"Fastest Lap Gear Shift\n"
                 f"{lap['Driver']} - {session.event['EventName']} {session.event.year}")

    cbar = fig.colorbar(lc, ax=ax, label="Gear", boundaries=np.arange(1, 10))
    cbar.set_ticks(np.arange(1.5, 9.5))
    cbar.set_ticklabels(np.arange(1, 9))
    show(fig)


def qualifying_result(session) -> None:
    fastf1.plotting.setup_mpl(mpl_timedelta_support=True, color_scheme=None)

    drivers = pd.unique(session.laps['Driver'])
    fastest_laps = (
        Laps([session.laps.pick_drivers(drv).pick_fastest() for drv in drivers])
        .sort_values(by='LapTime')
        .reset_index(drop=True)
    )

    pole_lap = fastest_laps.pick_fastest()
    fastest_laps['LapTimeDelta'] = fastest_laps['LapTime'] - pole_lap['LapTime']

    team_colors = [
        fastf1.plotting.get_team_color(lap['Team'], session=session)
        for _, lap in fastest_laps.iterlaps()
    ]

    fig, ax = plt.subplots()
    ax.barh(fastest_laps.index, fastest_laps['LapTimeDelta'],
            color=team_colors, edgecolor='grey')
    ax.set_yticks(fastest_laps.index)
    ax.set_yticklabels(fastest_laps['Driver'])
    ax.invert_yaxis()
    ax.set_axisbelow(True)
    ax.xaxis.grid(True, which='major', linestyle='--', color='black', zorder=-1000)

    lap_time_string = strftimedelta(pole_lap['LapTime'], '%m:%s.%ms')
    fig.suptitle(f"{session.event['EventName']} {session.event.year} Qualifying\n"
                 f"Fastest Lap: {lap_time_string} ({pole_lap['Driver']})")
    show(fig)


def speed_on_track(session) -> None:
    drivers = sorted(session.laps['Driver'].unique())
    print(f"\n{BOLD}{WHITE}  ── Select driver ──{RESET}")
    for i, drv in enumerate(drivers, 1):
        print(f"  {CYAN}{i:>2}{RESET}) {drv}")
    divider()

    while True:
        raw = input(f"  Driver (1-{len(drivers)}): ").strip()
        if raw.isdigit() and 1 <= int(raw) <= len(drivers):
            driver = drivers[int(raw) - 1]
            break
        print(RED + "  Invalid choice." + RESET)

    lap   = session.laps.pick_drivers(driver).pick_fastest()
    x     = lap.telemetry['X']
    y     = lap.telemetry['Y']
    color = lap.telemetry['Speed']

    points   = np.array([x, y]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)

    fig, ax = plt.subplots(figsize=(12, 6.75))
    fig.suptitle(f'{session.event.name} {session.event.year} - {driver} - Speed',
                 size=24, y=0.97)
    plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.12)
    ax.axis('off')
    ax.plot(x, y, color='black', linestyle='-', linewidth=16, zorder=0)

    norm = plt.Normalize(color.min(), color.max())
    lc   = LineCollection(segments, cmap=mpl.cm.plasma, norm=norm, linewidth=5)
    lc.set_array(color)
    ax.add_collection(lc)

    cbaxes = fig.add_axes([0.25, 0.05, 0.5, 0.05])
    mpl.colorbar.ColorbarBase(
        cbaxes,
        norm=mpl.colors.Normalize(vmin=color.min(), vmax=color.max()),
        cmap=mpl.cm.plasma, orientation="horizontal")
    show(fig)


def speed_traces(session) -> None:
    fastf1.plotting.setup_mpl(mpl_timedelta_support=True, color_scheme='fastf1')

    drivers = sorted(session.laps['Driver'].unique())
    print(f"\n{BOLD}{WHITE}  ── Select two drivers to compare ──{RESET}")
    for i, drv in enumerate(drivers, 1):
        print(f"  {CYAN}{i:>2}{RESET}) {drv}")
    divider()

    def pick_driver(label: str) -> str:
        while True:
            raw = input(f"  {label} (1-{len(drivers)}): ").strip()
            if raw.isdigit() and 1 <= int(raw) <= len(drivers):
                return drivers[int(raw) - 1]
            print(RED + "  Invalid choice." + RESET)

    drv1, drv2 = pick_driver("Driver 1"), pick_driver("Driver 2")

    lap1 = session.laps.pick_drivers(drv1).pick_fastest()
    lap2 = session.laps.pick_drivers(drv2).pick_fastest()
    tel1 = lap1.get_car_data().add_distance()
    tel2 = lap2.get_car_data().add_distance()

    c1 = fastf1.plotting.get_team_color(lap1['Team'], session=session)
    c2 = fastf1.plotting.get_team_color(lap2['Team'], session=session)

    fig, ax = plt.subplots()
    ax.plot(tel1['Distance'], tel1['Speed'], color=c1, label=drv1)
    ax.plot(tel2['Distance'], tel2['Speed'], color=c2, label=drv2)
    ax.set_xlabel('Distance in m')
    ax.set_ylabel('Speed in km/h')
    ax.legend()
    fig.suptitle(f"Fastest Lap Comparison — "
                 f"{session.event['EventName']} {session.event.year}")
    show(fig)


def plot_strategy(session) -> None:
    laps    = session.laps
    drivers = [session.get_driver(d)["Abbreviation"] for d in session.drivers]

    stints = (
        laps[["Driver", "Stint", "Compound", "LapNumber"]]
        .groupby(["Driver", "Stint", "Compound"])
        .count()
        .reset_index()
        .rename(columns={"LapNumber": "StintLength"})
    )

    fig, ax = plt.subplots(figsize=(5, 10))
    for driver in drivers:
        driver_stints      = stints.loc[stints["Driver"] == driver]
        previous_stint_end = 0
        for _, row in driver_stints.iterrows():
            ax.barh(y=driver,
                    width=row["StintLength"],
                    left=previous_stint_end,
                    color=fastf1.plotting.get_compound_color(row["Compound"], session=session),
                    edgecolor="black",
                    fill=True)
            previous_stint_end += row["StintLength"]

    ax.set_title(f"{session.event['EventName']} {session.event.year} — Tyre Strategy")
    ax.set_xlabel("Lap Number")
    ax.invert_yaxis()
    ax.grid(False)
    for spine in ('top', 'right', 'left'):
        ax.spines[spine].set_visible(False)
    plt.tight_layout()
    show(fig)


def team_pace_ranking(session) -> None:
    fastf1.plotting.setup_mpl(mpl_timedelta_support=False, color_scheme='fastf1')

    laps = session.laps.pick_quicklaps().copy()
    laps["LapTime (s)"] = laps["LapTime"].dt.total_seconds()

    team_order = (
        laps[["Team", "LapTime (s)"]]
        .groupby("Team")
        .median()["LapTime (s)"]
        .sort_values()
        .index
    )
    team_palette = {team: fastf1.plotting.get_team_color(team, session=session)
                    for team in team_order}

    fig, ax = plt.subplots(figsize=(15, 10))
    sns.boxplot(data=laps, x="Team", y="LapTime (s)", hue="Team",
                order=team_order, palette=team_palette,
                whiskerprops=dict(color="white"),
                boxprops=dict(edgecolor="white"),
                medianprops=dict(color="grey"),
                capprops=dict(color="white"),
                ax=ax)
    ax.set_title(f"{session.event['EventName']} {session.event.year} — Team Pace")
    ax.set(xlabel=None)
    ax.grid(visible=False)
    plt.tight_layout()
    show(fig)
