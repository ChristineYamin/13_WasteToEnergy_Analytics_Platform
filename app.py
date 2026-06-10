import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------
# PAGE CONFIG
# -----------------------------

st.set_page_config(
    page_title="Waste-to-Energy Analytics Platform",
    page_icon="♻️",
    layout="wide"
)

# -----------------------------
# LOAD DATA
# -----------------------------

@st.cache_data
def load_data():
    return pd.read_csv(
        r"data/cleaned_waste_management.csv"
    )

df = load_data()

# -----------------------------
# TITLE
# -----------------------------

st.title("♻️ Waste-to-Energy Analytics Platform")

st.markdown("""
This dashboard explores waste composition,
management strategies and CO₂ reduction potential.
""")

# ===================================================
# KPI SECTION
# ===================================================

st.subheader("📊 Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Countries",
        df['countries'].nunique()
    )

with col2:
    st.metric(
        "Records",
        len(df)
    )

with col3:
    st.metric(
        "Avg CO₂ Reduction",
        round(
            df['co₂_emissions_reduction_potential'].mean(),
            3
        )
    )

best_scenario = (
    df.groupby('scenario')
      ['co₂_emissions_reduction_potential']
      .mean()
      .idxmin()
)

with col4:
    st.metric(
        "Best Scenario",
        best_scenario
    )

# ===================================================
# PIE CHART
# ===================================================

st.subheader("🗑️ Average Waste Composition")

composition = df[
    [
        'food',
        'garden',
        'paper',
        'plastic',
        'glass',
        'metal'
    ]
].mean()

fig = px.pie(
    values=composition.values,
    names=composition.index,
    title="Average Waste Composition"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ===================================================
# COUNTRY ANALYSIS
# ===================================================

st.subheader("🌍 Country Analysis")

selected_country = st.selectbox(
    "Select Country",
    sorted(df['countries'].unique())
)

country_df = df[
    df['countries'] == selected_country
]

st.dataframe(country_df.head())

# ===================================================
# SCENARIO ANALYSIS
# ===================================================

st.subheader("⚡ Scenario Comparison")

scenario_df = (
    country_df.groupby('scenario')
              ['co₂_emissions_reduction_potential']
              .mean()
              .reset_index()
)

fig = px.bar(
    scenario_df,
    x='scenario',
    y='co₂_emissions_reduction_potential',
    title=f"CO₂ Reduction Potential - {selected_country}"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ===================================================
# MAP
# ===================================================

st.subheader("🗺️ Global Waste Generation")

country_totals = (
    df.groupby('countries')
      ['total_collected_msw_(t)']
      .sum()
      .reset_index()
)

fig = px.choropleth(
    country_totals,
    locations="countries",
    locationmode="country names",
    color="total_collected_msw_(t)",
    title="Global Waste Generation"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ===================================================
# INSIGHTS
# ===================================================

st.subheader("💡 Smart Insight")

best_country_scenario = (
    country_df.groupby('scenario')
              ['co₂_emissions_reduction_potential']
              .mean()
              .idxmin()
)

st.success(
    f"For {selected_country}, "
    f"the most environmentally beneficial strategy is "
    f"'{best_country_scenario}'."
)