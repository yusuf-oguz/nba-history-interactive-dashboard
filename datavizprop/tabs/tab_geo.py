import streamlit as st
import plotly.express as px
from data_loader import get_country_counts, get_state_counts

# Abbreviated US state codes mapping for choropleth
_STATE_ABBREV = {
    "Alabama": "AL", "Alaska": "AK", "Arizona": "AZ", "Arkansas": "AR",
    "California": "CA", "Colorado": "CO", "Connecticut": "CT", "DC": "DC",
    "Delaware": "DE", "Florida": "FL", "Georgia": "GA", "Hawaii": "HI",
    "Idaho": "ID", "Illinois": "IL", "Indiana": "IN", "Iowa": "IA",
    "Kansas": "KS", "Kentucky": "KY", "Louisiana": "LA", "Maine": "ME",
    "Maryland": "MD", "Massachusetts": "MA", "Michigan": "MI",
    "Minnesota": "MN", "Mississippi": "MS", "Missouri": "MO",
    "Montana": "MT", "Nebraska": "NE", "Nevada": "NV",
    "New Hampshire": "NH", "New Jersey": "NJ", "New Mexico": "NM",
    "New York": "NY", "North Carolina": "NC", "North Dakota": "ND",
    "Ohio": "OH", "Oklahoma": "OK", "Oregon": "OR", "Pennsylvania": "PA",
    "Rhode Island": "RI", "South Carolina": "SC", "South Dakota": "SD",
    "Tennessee": "TN", "Texas": "TX", "Utah": "UT", "Vermont": "VT",
    "Virginia": "VA", "Washingon": "WA", "Washington": "WA",
    "West Virginia": "WV", "Wisconsin": "WI", "Wyoming": "WY",
    "Delaware": "DE",
}


def render():
    st.header("Geography of NBA Players")
    st.markdown(
        "Which countries and U.S. states have produced the most NBA players? "
        "World map uses 1996–2023 data; U.S. choropleth covers the full historical dataset."
    )

    # ── World Map ─────────────────────────────────────────────────────────────
    st.subheader("NBA Players by Country (1996–2023)")
    country_df = get_country_counts()

    metric = st.radio(
        "Color by",
        ["player_count", "avg_pts", "avg_reb", "avg_ast"],
        format_func=lambda v: {
            "player_count": "# of Players",
            "avg_pts": "Avg Points",
            "avg_reb": "Avg Rebounds",
            "avg_ast": "Avg Assists",
        }[v],
        horizontal=True,
        key="geo_metric",
    )

    fig_world = px.choropleth(
        country_df,
        locations="country",
        locationmode="country names",
        color=metric,
        hover_name="country",
        hover_data={
            "player_count": True,
            "avg_pts": ":.1f",
            "avg_reb": ":.1f",
            "avg_ast": ":.1f",
        },
        color_continuous_scale="YlOrRd",
        labels={
            "player_count": "Players",
            "avg_pts": "Avg PPG",
            "avg_reb": "Avg RPG",
            "avg_ast": "Avg APG",
        },
    )
    fig_world.update_layout(
        height=480,
        margin=dict(t=10, b=10, l=0, r=0),
        geo=dict(showframe=False, showcoastlines=True),
    )
    st.plotly_chart(fig_world, use_container_width=True)

    # ── Top countries bar chart ───────────────────────────────────────────────
    top_n = st.slider("Show top N countries", 5, 30, 15, key="geo_topn")
    top_df = country_df.head(top_n)
    fig_bar = px.bar(
        top_df,
        x="country",
        y="player_count",
        color="avg_pts",
        color_continuous_scale="Blues",
        labels={"country": "Country", "player_count": "# Players", "avg_pts": "Avg PPG"},
        text="player_count",
    )
    fig_bar.update_traces(textposition="outside")
    fig_bar.update_layout(height=380, margin=dict(t=20, b=20),
                          coloraxis_showscale=True)
    st.plotly_chart(fig_bar, use_container_width=True)

    # ── US State Choropleth ───────────────────────────────────────────────────
    st.subheader("NBA Players by U.S. State (All-Time)")
    state_df = get_state_counts().copy()
    state_df["state_code"] = state_df["State"].map(_STATE_ABBREV)
    state_df = state_df.dropna(subset=["state_code"])

    fig_us = px.choropleth(
        state_df,
        locations="state_code",
        locationmode="USA-states",
        color="player_count",
        scope="usa",
        hover_name="State",
        hover_data={"player_count": True, "avg_pts": ":.0f"},
        color_continuous_scale="Blues",
        labels={"player_count": "# Players", "avg_pts": "Avg career PTS"},
    )
    fig_us.update_layout(height=440, margin=dict(t=10, b=10))
    st.plotly_chart(fig_us, use_container_width=True)
