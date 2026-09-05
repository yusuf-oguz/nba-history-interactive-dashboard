import os
import pandas as pd
import streamlit as st

BASE = os.path.dirname(__file__)
DATA = os.path.join(BASE, "data")
DATA_PLAYERS = os.path.join(BASE, "data_players")
DATA_BIRTHPLACES = os.path.join(BASE, "data_birthplaces")


# ── Raw loaders (cached) ──────────────────────────────────────────────────────

@st.cache_data
def load_player_per_game() -> pd.DataFrame:
    df = pd.read_csv(os.path.join(DATA, "Player Per Game.csv"))
    return df[df["lg"].isin(["NBA", "ABA", "BAA"])].copy()


@st.cache_data
def load_team_summaries() -> pd.DataFrame:
    df = pd.read_csv(os.path.join(DATA, "Team Summaries.csv"))
    return df[df["lg"].isin(["NBA", "ABA", "BAA"])].copy()


@st.cache_data
def load_team_stats_per_game() -> pd.DataFrame:
    df = pd.read_csv(os.path.join(DATA, "Team Stats Per Game.csv"))
    return df[df["lg"].isin(["NBA", "ABA", "BAA"])].copy()


@st.cache_data
def load_advanced() -> pd.DataFrame:
    df = pd.read_csv(os.path.join(DATA, "Advanced.csv"))
    return df[df["lg"].isin(["NBA", "ABA", "BAA"])].copy()


@st.cache_data
def load_all_seasons() -> pd.DataFrame:
    """justinas dataset — country, height, weight, 1996-2023."""
    return pd.read_csv(os.path.join(DATA_PLAYERS, "all_seasons.csv"))


@st.cache_data
def load_birthplaces() -> pd.DataFrame:
    """US state birthplace data — Player, City, State + career stats."""
    df = pd.read_csv(os.path.join(DATA_BIRTHPLACES, "nba_players_by_state.csv"))
    for col in ["PTS", "G", "Yrs", "TRB", "AST", "STL", "BLK"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    return df


# ── Derived datasets (cached) ─────────────────────────────────────────────────

@st.cache_data
def get_threept_trends() -> pd.DataFrame:
    """Annual league averages for 3P, scoring and pace (RQ1).

    Uses team-level stats (Team Stats Per Game) so 3PA/game reflects
    actual team attempts (~39 in 2024), not a per-player average.
    Pace comes from Team Summaries (available from 1951+).
    """
    # Team-level per-game averages aggregated to season
    tspg = load_team_stats_per_game()
    team_agg = (
        tspg[tspg["playoffs"] == False]
        .groupby("season")
        .agg(
            team_pts=("pts_per_game", "mean"),    # team scoring per game
            team_3pa=("x3pa_per_game", "mean"),   # team 3PA per game
            team_3p=("x3p_per_game", "mean"),     # team 3PM per game
            team_3p_pct=("x3p_percent", "mean"),  # team 3P%
            team_fga=("fga_per_game", "mean"),
        )
        .reset_index()
    )
    # 3P attempt share of all FGA
    team_agg["x3p_ar"] = team_agg["team_3pa"] / team_agg["team_fga"]

    # Pace from Team Summaries
    ts = load_team_summaries()
    pace_agg = (
        ts[ts["playoffs"] == False]
        .groupby("season")
        .agg(pace=("pace", "mean"))
        .reset_index()
    )

    return team_agg.merge(pace_agg, on="season", how="left").sort_values("season")


@st.cache_data
def get_physical_performance() -> pd.DataFrame:
    """Player height/weight vs pts, win shares (RQ2). Uses 1996-2023 window."""
    seasons = load_all_seasons().copy()
    adv = load_advanced().copy()

    # Normalise season: '1996-97' -> 1997 for join with Advanced (end-year int)
    seasons["season_end"] = seasons["season"].str.split("-").str[0].astype(int) + 1
    seasons["player_name_lower"] = seasons["player_name"].str.lower().str.strip()

    adv["season_end"] = adv["season"]
    adv["player_name_lower"] = adv["player"].str.lower().str.strip()

    # Aggregate advanced per player per season (handle mid-season trades)
    adv_agg = (
        adv.groupby(["player_name_lower", "season_end"])
        .agg(ws=("ws", "sum"), bpm=("bpm", "mean"), per=("per", "mean"))
        .reset_index()
    )

    merged = seasons.merge(adv_agg, on=["player_name_lower", "season_end"], how="left")
    cols = [
        "player_name", "season", "season_end", "age",
        "player_height", "player_weight", "country",
        "pts", "reb", "ast", "gp",
        "ws", "bpm", "per",
    ]
    return merged[cols].dropna(subset=["player_height", "player_weight", "pts"])


@st.cache_data
def get_career_arc() -> pd.DataFrame:
    """Average PPG by age across all players (RQ5)."""
    ppg = load_player_per_game()
    # Minimum games filter to exclude injury/cameo seasons
    ppg = ppg[ppg["g"] >= 20].copy()

    arc = (
        ppg.groupby("age")
        .agg(
            avg_pts=("pts_per_game", "mean"),
            avg_ast=("ast_per_game", "mean"),
            avg_trb=("trb_per_game", "mean"),
            n_player_seasons=("player_id", "count"),
        )
        .reset_index()
    )
    return arc[arc["age"].between(18, 40)]


@st.cache_data
def get_country_counts() -> pd.DataFrame:
    """Player counts and avg stats by country (RQ3 — world map)."""
    seasons = load_all_seasons()
    return (
        seasons.groupby("country")
        .agg(
            player_count=("player_name", "nunique"),
            avg_pts=("pts", "mean"),
            avg_reb=("reb", "mean"),
            avg_ast=("ast", "mean"),
        )
        .reset_index()
        .sort_values("player_count", ascending=False)
    )


@st.cache_data
def get_state_counts() -> pd.DataFrame:
    """Player counts by US state (RQ3 — choropleth)."""
    bp = load_birthplaces()
    return (
        bp.groupby("State")
        .agg(player_count=("Player", "count"), avg_pts=("PTS", "mean"))
        .reset_index()
    )


@st.cache_data
def get_position_profiles() -> pd.DataFrame:
    """Per-game stats + advanced by position (RQ4)."""
    ppg = load_player_per_game()
    adv = load_advanced()

    ppg = ppg[ppg["g"] >= 20].copy()

    # Keep primary position only (first listed)
    ppg["pos_primary"] = ppg["pos"].str.split("-").str[0]

    adv_agg = (
        adv.groupby(["player_id", "season"])
        .agg(ws=("ws", "sum"), per=("per", "mean"), bpm=("bpm", "mean"), vorp=("vorp", "sum"))
        .reset_index()
    )

    merged = ppg.merge(adv_agg, on=["player_id", "season"], how="left")

    stat_cols = [
        "pts_per_game", "ast_per_game", "trb_per_game",
        "stl_per_game", "blk_per_game", "fg_percent",
        "x3p_percent", "ft_percent",
        "per", "ws", "bpm",
    ]
    keep = ["player_id", "player", "season", "age", "pos_primary"] + stat_cols
    return merged[keep].dropna(subset=["pos_primary"])
