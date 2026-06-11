
import streamlit as st
import pandas as pd
import numpy as np
import pickle
import plotly.express as px

# =========================
# CONFIG
# =========================
st.set_page_config(
    page_title="Smart Waste Strategy Advisor",
    page_icon="♻️",
    layout="wide"
)

st.title("♻️ Smart Waste Management Strategy Advisor")
st.markdown("AI-powered decision support system for CO₂ reduction and waste strategy optimization.")

# =========================
# LOAD DATA + MODEL
# =========================
@st.cache_data
def load_data():
    return pd.read_csv(
        r"data/cleaned_waste_management.csv"
    )

df = load_data()

model = pickle.load(open(
    r"models/best_model.pkl",
    "rb"
))

model_columns = pickle.load(open(
    r"models/model_columns.pkl",
    "rb"
))

# =========================
# SIDEBAR
# =========================
st.sidebar.header("🌍 Control Panel")

country = st.sidebar.selectbox(
    "Select Country",
    sorted(df["countries"].unique())
)



country_df = df[df["countries"] == country]

# =========================
# KPI SECTION
# =========================
st.subheader("📊 Executive Summary")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Waste", f"{country_df['total_collected_msw_(t)'].iloc[0]:,.0f}")

with col2:
    st.metric("Avg CO₂ Reduction", round(df["co₂_emissions_reduction_potential"].mean(), 3))

best_strategy_global = df.groupby("scenario")["co₂_emissions_reduction_potential"].mean().idxmin()

with col3:
    st.metric("Best Global Strategy", best_strategy_global)

dominant_waste = country_df[
    ["food","garden","paper","plastic","glass","metal","rubber_and_leather","textile","other"]
].mean().idxmax()

with col4:
    st.metric("Dominant Waste Type", dominant_waste)

# =========================
# WASTE COMPOSITION
# =========================
st.subheader("🗑️ Waste Profile")

composition = country_df[
    ["food","garden","paper","plastic","glass","metal"]
].mean()

fig = px.pie(values=composition.values, names=composition.index)
st.plotly_chart(fig, use_container_width=True)

# =========================
# WTE SUITABILITY SCORE (OPTION B)
# =========================
st.subheader("⚡ WTE Suitability Score")

weights = {
    "plastic": 1.0,
    "rubber_and_leather": 0.9,
    "paper": 0.8,
    "textile": 0.7,
    "food": 0.3,
    "garden": 0.2,
    "glass": 0.0,
    "metal": 0.0,
    "other": 0.4
}

score = 0
for k, w in weights.items():
    score += country_df[k].mean() * w

score = min(100, score)

st.metric("WTE Suitability Score", f"{score:.1f} / 100")

if score > 75:
    st.success("🟢 **High Potential:** This waste composition is rich in high-calorific materials (Plastic/Paper). Thermal WtE plants will operate with high efficiency here.")
elif score > 50:
    st.warning("🟡 **Moderate Potential:** This waste stream has a mix of organic and high-calorific materials. Consider a Hybrid approach: Anaerobic Digestion for the organics and WtE for the residuals.")
else:
    st.error("🔴 **Low Potential:** This waste stream is primarily organic or high-moisture (Food/Garden). Traditional incineration is inefficient here. Focus on Composting or Biogas production instead.")

# =========================
# STRATEGY COMPARISON
# =========================
st.subheader("⚙️ Strategy Performance Comparison")

scenario_df = country_df.groupby("scenario")["co₂_emissions_reduction_potential"].mean().reset_index()

fig = px.bar(
    scenario_df,
    x="scenario",
    y="co₂_emissions_reduction_potential",
    color="co₂_emissions_reduction_potential"
)

st.plotly_chart(fig, use_container_width=True)

# =========================
# RECOMMENDATION ENGINE
# =========================
st.subheader("🏆 Strategy Recommendation Engine")

best_row = scenario_df.sort_values("co₂_emissions_reduction_potential").iloc[0]

st.success(f"""
Recommended Strategy: {best_row['scenario']}

Expected CO₂ Reduction: {best_row['co₂_emissions_reduction_potential']:.3f}
""")

st.markdown("### Why this strategy?")
st.write("""
- Based on waste composition distribution  
- Optimized for CO₂ reduction potential  
- Aligns with environmental efficiency patterns  
""")

# =========================
# STRATEGY RANKING
# =========================
st.subheader("📊 Strategy Ranking")

ranking = scenario_df.sort_values("co₂_emissions_reduction_potential")

st.dataframe(ranking, use_container_width=True)

# =========================
# ML PREDICTION
# =========================
st.subheader("🔮 CO₂ Prediction Model")

scenario = st.selectbox(
    "Select Scenario for Prediction",
    sorted(df["scenario"].unique())
)

input_data = country_df.iloc[0].copy()
input_data["scenario"] = scenario

input_df = pd.DataFrame([input_data])

input_df = input_df.drop(columns=["co₂_emissions_reduction_potential"])

input_encoded = pd.get_dummies(input_df)

input_encoded = input_encoded.reindex(columns=model_columns, fill_value=0)

if st.button("Predict CO₂ Reduction"):
    prediction = model.predict(input_encoded)[0]
    st.metric("Predicted CO₂ Reduction", round(prediction, 3))
