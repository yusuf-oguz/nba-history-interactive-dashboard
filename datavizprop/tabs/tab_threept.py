import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from data_loader import get_threept_trends


def render():
    st.header("Three-Point Revolution")
    st.markdown(
        "How did the three-point shot transform NBA gameplay? "
        "All metrics below are **team averages per game** (regular season only), "
        "making them directly comparable across eras."
    )

    df = get_threept_trends().sort_values("season")

    col_filter, _ = st.columns([2, 5])
    with col_filter:
        year_range = st.slider(
            "Season range",
            min_value=int(df["season"].min()),
            max_value=int(df["season"].max()),
            value=(1979, int(df["season"].max())),
            key="threept_range",
        )

    dff = df[df["season"].between(year_range[0], year_range[1])]

    # ── Chart 1: Team 3PA per game ────────────────────────────────────────────
    st.subheader("3-Point Attempts per Game (Team Average)")
    st.caption("How many 3-pointers did an average NBA team attempt each game?")

    fig1 = px.area(
        dff,
        x="season",
        y="team_3pa",
        labels={"season": "Season", "team_3pa": "3PA per game (team)"},
        color_discrete_sequence=["#E35B44"],
    )
    fig1.add_vline(x=1979, line_dash="dash", line_color="gray",
                   annotation_text="3P rule introduced (1979–80)",
                   annotation_position="top right")
    fig1.add_vline(x=2015, line_dash="dot", line_color="#aaa",
                   annotation_text="Warriors era begins",
                   annotation_position="top left")
    fig1.update_layout(height=360, margin=dict(t=20, b=20))
    st.plotly_chart(fig1, use_container_width=True)

    # ── Chart 2: Team scoring + Pace dual-axis ────────────────────────────────
    st.subheader("Team Scoring Average & Pace Over Time")
    st.caption(
        "Left axis: average points scored per game by a team. "
        "Right axis: pace (possessions per 48 min). Pace data available from 1974."
    )

    df_pts = dff.dropna(subset=["team_pts"])
    df_pace = dff.dropna(subset=["pace"])

    fig2 = make_subplots(specs=[[{"secondary_y": True}]])
    fig2.add_trace(
        go.Scatter(x=df_pts["season"], y=df_pts["team_pts"],
                   name="Team PPG", line=dict(color="#1D428A", width=2.5)),
        secondary_y=False,
    )
    fig2.add_trace(
        go.Scatter(x=df_pace["season"], y=df_pace["pace"],
                   name="Pace", line=dict(color="#C8102E", width=2, dash="dot")),
        secondary_y=True,
    )
    fig2.update_yaxes(title_text="Team points per game", secondary_y=False)
    fig2.update_yaxes(title_text="Pace (possessions / 48 min)", secondary_y=True)
    fig2.update_xaxes(range=[year_range[0], year_range[1]])
    fig2.update_layout(height=380, margin=dict(t=20, b=20),
                       legend=dict(orientation="h", y=1.1))
    st.plotly_chart(fig2, use_container_width=True)

    # ── Chart 3: 3P attempt share of all FGA ─────────────────────────────────
    st.subheader("3-Point Attempts as % of All Field Goal Attempts")
    st.caption("Share of a team's shot attempts that were 3-pointers.")

    fig3 = px.bar(
        dff.dropna(subset=["x3p_ar"]),
        x="season",
        y="x3p_ar",
        labels={"season": "Season", "x3p_ar": "3PA / FGA"},
        color="x3p_ar",
        color_continuous_scale="Reds",
    )
    fig3.update_layout(height=340, margin=dict(t=20, b=20),
                       coloraxis_showscale=False)
    st.plotly_chart(fig3, use_container_width=True)

    # ── Key stat callout ──────────────────────────────────────────────────────
    latest = dff[dff["season"] == dff["season"].max()].iloc[0]
    first_3p = dff[dff["season"] == 1980]
    c1, c2, c3 = st.columns(3)
    c1.metric("Team 3PA/game (latest)", f"{latest['team_3pa']:.1f}")
    c2.metric("3P share of FGA (latest)", f"{latest['x3p_ar']*100:.1f}%")
    if not first_3p.empty:
        growth = latest["team_3pa"] / (first_3p.iloc[0]["team_3pa"] + 0.01)
        c3.metric("Growth since 1980", f"{growth:.0f}×")
