import streamlit as st
import pandas as pd
import numpy as np
import pickle
import plotly.express as px

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="Smart Waste Strategy Advisor", page_icon="♻️", layout="wide")

# Custom CSS for a professional "Card" look
st.markdown("""
    <style>
    .stApp { background-color: #f8f9fa; }
    div[data-testid="stMetric"] { background-color: white; padding: 15px; border-radius: 10px; box-shadow: 0px 2px 4px rgba(0,0,0,0.05); }
    </style>
""", unsafe_allow_html=True)

st.title("♻️ Smart Waste Management Strategy Advisor")
st.markdown("AI-powered decision support system for CO₂ reduction and waste strategy optimization.")

# Load Data/Model (Cached)
@st.cache_data
def load_data(): return pd.read_csv(r"data/cleaned_waste_management.csv")

df = load_data()
model = pickle.load(open(r"models/best_model.pkl", "rb"))
model_columns = pickle.load(open(r"models/model_columns.pkl", "rb"))

# Sidebar
st.sidebar.header("🌍 Control Panel")
country = st.sidebar.selectbox("Select Country", sorted(df["countries"].unique()))
country_df = df[df["countries"] == country]

# TABS NAVIGATION
tab1, tab2, tab3 = st.tabs(["📊 Overview", "⚡ Strategy Advisor", "🔮 ML Simulator"])

with tab1:
    st.subheader("Executive Summary")
    col1, col2, col3, col4 = st.columns(4)
    with col1: st.metric("Total Waste", f"{country_df['total_collected_msw_(t)'].iloc[0]:,.0f}")
    with col2: st.metric("Avg CO₂ Reduction", round(df["co₂_emissions_reduction_potential"].mean(), 3))
    with col3: st.metric("Best Global Strategy", df.groupby("scenario")["co₂_emissions_reduction_potential"].mean().idxmin())
    with col4: st.metric("Dominant Waste Type", country_df[["food","garden","paper","plastic","glass","metal","rubber_and_leather","textile","other"]].mean().idxmax())
    
    with st.container(border=True):
        st.subheader("🗑️ Waste Profile")
        composition = country_df[["food","garden","paper","plastic","glass","metal"]].mean()
        fig = px.pie(values=composition.values, names=composition.index, hole=0.3)
        st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.subheader("⚡ WTE Suitability Score")
    weights = {"plastic": 1.0, "rubber_and_leather": 0.9, "paper": 0.8, "textile": 0.7, "food": 0.3, "garden": 0.2, "glass": 0.0, "metal": 0.0, "other": 0.4}
    score = min(100, sum(country_df[k].mean() * w for k, w in weights.items()))
    st.progress(score / 100, text=f"Efficiency Potential: {score:.1f}%")
    
    # Logic from our previous chat
    if score > 75: 
        st.success("🟢 **HIGH POTENTIAL (75+)**")
        with st.container(border=True):
            st.markdown("**👉 Decision:** Prioritize WtE expansion. **👉 Why:** High energy recovery = higher revenue.")
    elif score > 50:
        st.warning("🟡 **MODERATE POTENTIAL (50–75)**")
        with st.container(border=True):
            st.markdown("**👉 Decision:** Build Hybrid System (Anaerobic Digestion + WtE). **👉 Priority:** Segregate organics.")
    else:
        st.error("🔴 **LOW POTENTIAL (<50)**")
        with st.container(border=True):
            st.markdown("**👉 Decision:** Focus on Composting/Biogas. **👉 Note:** Thermal WtE is financially inefficient here.")

    st.subheader("⚙️ Strategy Performance")
    scenario_df = country_df.groupby("scenario")["co₂_emissions_reduction_potential"].mean().reset_index()
    fig2 = px.bar(scenario_df, x="scenario", y="co₂_emissions_reduction_potential", color="co₂_emissions_reduction_potential")
    st.plotly_chart(fig2, use_container_width=True)

with tab3:
    st.subheader("🔮 CO₂ Prediction Model")
    scenario = st.selectbox("Select Scenario for Prediction", sorted(df["scenario"].unique()))
    if st.button("Predict CO₂ Reduction Potential"):
        input_data = country_df.iloc[0].copy()
        input_data["scenario"] = scenario
        input_df = pd.get_dummies(pd.DataFrame([input_data]).drop(columns=["co₂_emissions_reduction_potential"]))
        input_encoded = input_df.reindex(columns=model_columns, fill_value=0)
        prediction = model.predict(input_encoded)[0]
        st.metric("Predicted CO₂ Reduction", f"{round(prediction, 3)} units")
    
    st.subheader("📊 Strategy Ranking")
    st.dataframe(scenario_df.sort_values("co₂_emissions_reduction_potential"), use_container_width=True)