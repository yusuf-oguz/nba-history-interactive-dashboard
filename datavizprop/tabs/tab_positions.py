import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from data_loader import get_position_profiles

_VALID_POS = ["PG", "SG", "SF", "PF", "C"]

_STAT_LABELS = {
    "pts_per_game": "Points",
    "ast_per_game": "Assists",
    "trb_per_game": "Rebounds",
    "stl_per_game": "Steals",
    "blk_per_game": "Blocks",
    "fg_percent": "FG%",
    "x3p_percent": "3P%",
    "ft_percent": "FT%",
    "per": "PER",
    "ws": "Win Shares",
    "bpm": "BPM",
}


def render():
    st.header("Position Profiles")
    st.markdown(
        "How do statistical profiles differ across NBA positions? "
        "Includes data from 1947 to 2024 (min 20 games/season)."
    )

    df = get_position_profiles()
    df = df[df["pos_primary"].isin(_VALID_POS)]

    # ── Filters ───────────────────────────────────────────────────────────────
    c1, c2 = st.columns([3, 2])
    with c1:
        positions = st.multiselect(
            "Positions",
            _VALID_POS,
            default=_VALID_POS,
            key="pos_filter",
        )
    with c2:
        era = st.selectbox(
            "Era",
            ["All", "Classic (1947–1979)", "Modern (1980–2002)", "Current (2003–2024)"],
            key="pos_era",
        )

    dff = df[df["pos_primary"].isin(positions)].copy()

    if era == "Classic (1947–1979)":
        dff = dff[dff["season"] <= 1979]
    elif era == "Modern (1980–2002)":
        dff = dff[dff["season"].between(1980, 2002)]
    elif era == "Current (2003–2024)":
        dff = dff[dff["season"] >= 2003]

    # ── Chart 1: Heatmap — position × stat ───────────────────────────────────
    st.subheader("Position × Statistics Heatmap (Average)")
    stat_cols = [c for c in _STAT_LABELS if c in dff.columns]
    heat = (
        dff.groupby("pos_primary")[stat_cols]
        .mean()
        .reindex(_VALID_POS)
        .dropna(how="all")
    )
    # Normalise each column 0-1 for visual comparability
    heat_norm = (heat - heat.min()) / (heat.max() - heat.min() + 1e-9)
    heat_norm.columns = [_STAT_LABELS[c] for c in heat_norm.columns]

    fig_heat = px.imshow(
        heat_norm,
        text_auto=False,
        color_continuous_scale="RdYlGn",
        labels=dict(x="Statistic", y="Position", color="Normalised"),
        aspect="auto",
    )
    fig_heat.update_layout(height=320, margin=dict(t=20, b=20))
    st.plotly_chart(fig_heat, use_container_width=True)

    # ── Chart 2: Box plots ────────────────────────────────────────────────────
    st.subheader("Distribution by Position")
    stat_box = st.selectbox(
        "Statistic",
        stat_cols,
        format_func=lambda v: _STAT_LABELS[v],
        key="pos_box_stat",
    )

    fig_box = px.box(
        dff.dropna(subset=[stat_box]),
        x="pos_primary",
        y=stat_box,
        color="pos_primary",
        category_orders={"pos_primary": _VALID_POS},
        labels={"pos_primary": "Position", stat_box: _STAT_LABELS[stat_box]},
        color_discrete_sequence=px.colors.qualitative.Bold,
    )
    fig_box.update_layout(height=400, showlegend=False, margin=dict(t=20, b=20))
    st.plotly_chart(fig_box, use_container_width=True)

    # ── Chart 3: Radar chart — average profile per position ───────────────────
    st.subheader("Radar Chart — Average Profile per Position")
    radar_stats = ["pts_per_game", "ast_per_game", "trb_per_game",
                   "stl_per_game", "blk_per_game", "per"]
    radar_stats = [s for s in radar_stats if s in dff.columns]
    radar_labels = [_STAT_LABELS[s] for s in radar_stats]

    pos_means = dff.groupby("pos_primary")[radar_stats].mean().reindex(positions)

    # Normalise for radar
    col_max = pos_means.max()
    pos_norm = pos_means.divide(col_max + 1e-9)

    colors_radar = px.colors.qualitative.Bold
    fig_radar = go.Figure()
    for i, pos in enumerate(pos_norm.index):
        vals = pos_norm.loc[pos].tolist()
        vals_closed = vals + [vals[0]]
        labels_closed = radar_labels + [radar_labels[0]]
        fig_radar.add_trace(go.Scatterpolar(
            r=vals_closed,
            theta=labels_closed,
            fill="toself",
            name=pos,
            line_color=colors_radar[i % len(colors_radar)],
            opacity=0.65,
        ))

    fig_radar.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
        height=460,
        legend=dict(orientation="h", y=-0.1),
        margin=dict(t=20, b=40),
    )
    st.plotly_chart(fig_radar, use_container_width=True)
