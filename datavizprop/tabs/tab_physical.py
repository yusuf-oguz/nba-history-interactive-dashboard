import pandas as pd
import streamlit as st
import plotly.express as px
from data_loader import get_physical_performance

_POSITIONS = ["All", "PG", "SG", "SF", "PF", "C"]


def render():
    st.header("Physical Attributes vs Performance")
    st.markdown(
        "Is there a meaningful relationship between a player's height/weight "
        "and their on-court production? Data covers the 1996–2023 seasons."
    )

    df = get_physical_performance()

    # ── Filters ───────────────────────────────────────────────────────────────
    c1, c2, c3 = st.columns(3)
    with c1:
        x_axis = st.selectbox(
            "X axis (physical)",
            ["player_height", "player_weight"],
            format_func=lambda v: "Height (cm)" if "height" in v else "Weight (kg)",
            key="phys_x",
        )
    with c2:
        y_axis = st.selectbox(
            "Y axis (performance)",
            ["pts", "ws", "per", "bpm"],
            format_func=lambda v: {
                "pts": "Points per game",
                "ws": "Win Shares",
                "per": "Player Efficiency Rating",
                "bpm": "Box Plus/Minus",
            }[v],
            key="phys_y",
        )
    with c3:
        country_filter = st.selectbox(
            "Country",
            ["All"] + sorted(df["country"].dropna().unique().tolist()),
            key="phys_country",
        )

    dff = df.copy()
    if country_filter != "All":
        dff = dff[dff["country"] == country_filter]
    dff = dff.dropna(subset=[x_axis, y_axis])

    axis_labels = {
        "player_height": "Height (cm)",
        "player_weight": "Weight (kg)",
        "pts": "Points per game",
        "ws": "Win Shares",
        "per": "PER",
        "bpm": "Box Plus/Minus",
    }

    # ── Chart 1: Scatter with OLS trendline ───────────────────────────────────
    st.subheader(f"{axis_labels[x_axis]} vs {axis_labels[y_axis]}")
    sample = dff.sample(min(len(dff), 3000), random_state=42)
    fig1 = px.scatter(
        sample,
        x=x_axis,
        y=y_axis,
        color="country",
        hover_name="player_name",
        hover_data={"season": True, "age": True, x_axis: True, y_axis: True, "country": False},
        labels=axis_labels,
        opacity=0.5,
        trendline="ols",
        trendline_scope="overall",
        trendline_color_override="#FF4B4B",
        color_discrete_sequence=px.colors.qualitative.Safe,
    )
    fig1.update_layout(height=480, showlegend=False, margin=dict(t=20, b=20))
    st.plotly_chart(fig1, use_container_width=True)

    # ── Chart 2: Height/Weight distribution by scoring tier ───────────────────
    st.subheader(f"{axis_labels[x_axis]} Distribution by Scoring Tier")
    dff2 = dff.dropna(subset=[x_axis, "pts"]).copy()
    dff2["scoring_tier"] = pd.qcut(
        dff2["pts"], q=4,
        labels=["Bottom 25%", "25–50%", "50–75%", "Top 25%"],
    )
    fig2 = px.box(
        dff2,
        x="scoring_tier",
        y=x_axis,
        color="scoring_tier",
        labels={"scoring_tier": "Scoring Tier", x_axis: axis_labels[x_axis]},
        color_discrete_sequence=px.colors.sequential.Blues[2:],
        category_orders={"scoring_tier": ["Bottom 25%", "25–50%", "50–75%", "Top 25%"]},
    )
    fig2.update_layout(height=380, showlegend=False, margin=dict(t=20, b=20))
    st.plotly_chart(fig2, use_container_width=True)
