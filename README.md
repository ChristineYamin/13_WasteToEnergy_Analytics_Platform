# ♻️ Smart Waste Management Strategy Advisor

An AI-powered decision support system that helps waste management authorities and Waste-to-Energy (WtE) managers evaluate waste composition, estimate energy recovery potential, and select the most effective environmental strategy to reduce CO₂ emissions.

---

## 🎯 Project Objective

This project transforms raw municipal solid waste data into an **interactive decision intelligence platform**.

It answers three key questions:

- What is the current waste composition of a country?
- How suitable is the waste for Waste-to-Energy (WtE) conversion?
- Which waste management strategy delivers the best CO₂ reduction?

---

## 🧠 Key Features

### ⚡ 1. Executive Dashboard
- Total waste collected per country
- Dominant waste type identification
- Average CO₂ reduction potential
- Best-performing global strategy

---

### 🗑️ 2. Waste Composition Analysis
- Visual breakdown of waste types:
  - Food waste
  - Plastic
  - Paper
  - Glass
  - Metal
- Helps identify energy-rich vs non-recyclable fractions

---

### ⚡ 3. WTE Suitability Score (Core Innovation)
A custom-built **engineering metric** that evaluates how suitable a waste stream is for energy recovery.

#### Weighted Formula:

- Plastic → 1.0  
- Rubber & Leather → 0.9  
- Paper → 0.8  
- Textile → 0.7  
- Food → 0.3  
- Garden → 0.2  
- Glass → 0.0  
- Metal → 0.0  

#### Output:
- Score (0–100)
- Classification:
  - 🟢 High Potential
  - 🟡 Moderate Potential
  - 🔴 Low Potential

---

### 🏆 4. Strategy Recommendation Engine
Automatically recommends the optimal waste management strategy based on CO₂ reduction potential.

Supported strategies:
- Composting
- Anaerobic Digestion
- Waste-to-Energy (WtE)
- Hybrid systems (WtE + Composting)

Each recommendation includes:
- Expected CO₂ reduction
- Explanation of decision logic
- Operational guidance

---

### 📊 5. Strategy Ranking System
- Ranks all available strategies per country
- Compares CO₂ reduction performance
- Supports decision prioritization

---

### 🔮 6. Machine Learning Prediction Model
A supervised regression model trained to predict CO₂ emission reduction potential.

#### Models evaluated:
- Linear Regression
- Random Forest Regressor
- XGBoost Regressor

#### Final model:
I used linear regression, Random Forest and XGBoost and 
the best model is the linear regression according to performance (R², RMSE, MAE)
---

### ⚠️ 7. Strategic Decision Alerts
Provides managerial insights:

- 🟢 High potential → prioritize WtE expansion
- 🟡 Moderate → adopt hybrid systems
- 🔴 Low → focus on composting and biogas infrastructure

---

## 🏗️ Tech Stack

- Python 🐍
- Pandas & NumPy
- Scikit-learn
- XGBoost
- Streamlit
- Plotly
- Matplotlib / Seaborn

---

## Key Insights 
- Waste composition directly impacts energy recovery potential
- Countries with high plastic/paper waste show higher WtE efficiency
- Hybrid systems outperform single-strategy approaches in most cases
- CO₂ reduction potential varies significantly across waste scenarios

## Business Value
This system acts as a decision intelligence tool for:
- Waste-to-Energy plant managers
- Environmental policymakers
- Municipal waste authorities

It enables:
- Faster decision-making (within minutes)
- Strategy optimization
- Environmental impact forecasting
- Data-driven infrastructure planning

## Machine Learning Work Flow
1. Data preprocessing & cleaning
2. Feature encoding (countries + scenarios)
3. Model training (regression models)
4. Model evaluation (MAE, RMSE, R²)
5. Final model selection
6. Deployment via Streamlit

## Author
Shwe Yamin
Data Science Graduate | AI & Analytics Enthusiast