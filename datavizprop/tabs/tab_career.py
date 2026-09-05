import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from data_loader import get_career_arc, load_player_per_game
import pandas as pd


def render():
    st.header("Career Arc & Peak Age")
    st.markdown(
        "At what age do NBA players typically peak? "
        "How do different statistics evolve across a career? (1947–2024, min 20 games/season)"
    )

    arc = get_career_arc()

    # ── Chart 1: Multi-stat career arc ───────────────────────────────────────
    st.subheader("League-Wide Average Stats by Age")
    stats = st.multiselect(
        "Stats to display",
        options=["avg_pts", "avg_ast", "avg_trb"],
        default=["avg_pts", "avg_ast", "avg_trb"],
        format_func=lambda v: {"avg_pts": "Points", "avg_ast": "Assists", "avg_trb": "Rebounds"}[v],
        key="career_stats",
    )

    fig1 = go.Figure()
    colors = {"avg_pts": "#1D428A", "avg_ast": "#C8102E", "avg_trb": "#2E8B57"}
    labels = {"avg_pts": "PPG", "avg_ast": "APG", "avg_trb": "RPG"}
    for stat in stats:
        fig1.add_trace(go.Scatter(
            x=arc["age"], y=arc[stat],
            mode="lines+markers",
            name=labels.get(stat, stat),
            line=dict(color=colors.get(stat, "#888"), width=2.5),
            marker=dict(size=5),
        ))

    fig1.update_layout(
        height=420,
        xaxis_title="Age",
        yaxis_title="Average per game",
        legend=dict(orientation="h", y=1.08),
        margin=dict(t=20, b=20),
    )
    st.plotly_chart(fig1, use_container_width=True)

    # ── Peak age callout ──────────────────────────────────────────────────────
    peak_age = int(arc.loc[arc["avg_pts"].idxmax(), "age"])
    peak_pts = arc.loc[arc["avg_pts"].idxmax(), "avg_pts"]
    st.info(f"📌 League-wide scoring peak: **age {peak_age}** ({peak_pts:.1f} PPG average)")

    # ── Chart 2: Heatmap — stat × age ────────────────────────────────────────
    st.subheader("Stat Intensity by Age (Heatmap)")
    heat_df = arc[["age", "avg_pts", "avg_ast", "avg_trb"]].set_index("age").T
    heat_df.index = ["Points", "Assists", "Rebounds"]

    import plotly.figure_factory as ff
    import numpy as np

    fig2 = px.imshow(
        heat_df,
        color_continuous_scale="Blues",
        labels=dict(x="Age", y="Stat", color="Avg"),
        aspect="auto",
    )
    fig2.update_layout(height=260, margin=dict(t=20, b=20))
    st.plotly_chart(fig2, use_container_width=True)

    # ── Chart 3: Sample size per age ─────────────────────────────────────────
    st.subheader("Number of Player-Seasons per Age")
    fig3 = px.bar(
        arc, x="age", y="n_player_seasons",
        labels={"age": "Age", "n_player_seasons": "Player-seasons"},
        color="n_player_seasons",
        color_continuous_scale="Greens",
    )
    fig3.update_layout(height=300, margin=dict(t=20, b=20),
                       coloraxis_showscale=False)
    st.plotly_chart(fig3, use_container_width=True)
