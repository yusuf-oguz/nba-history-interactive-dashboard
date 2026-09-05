import streamlit as st

st.set_page_config(
    page_title="NBA Data Visualization · DataVIZZ",
    page_icon="🏀",
    layout="wide",
)

from tabs import tab_threept, tab_physical, tab_career, tab_geo, tab_positions

st.title("🏀 NBA Statistics Dashboard (1947–2024)")
st.caption("DataVIZZ · YZV475E Data Visualization · ITU 2025–2026 Spring")

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📈 Three-Point Revolution",
    "💪 Physical vs Performance",
    "📊 Career Arc & Peak Age",
    "🌍 Geography",
    "🏃 Position Profiles",
])

with tab1:
    tab_threept.render()

with tab2:
    tab_physical.render()

with tab3:
    tab_career.render()

with tab4:
    tab_geo.render()

with tab5:
    tab_positions.render()
