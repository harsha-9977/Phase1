# src/app.py

import streamlit as st
import pandas as pd
import plotly.express as px
import pydeck as pdk
from src.utils import load_crime_data
from src.predictive_model import load_model, make_prediction

# --- Setup
st.set_page_config(page_title="Crime Dashboard", layout="wide")

# --- Title
st.title("Crime Analysis & Prediction Dashboard")

# --- Load Data
@st.cache_data
def load_data():
    return load_crime_data()

crime_data = load_data()

# --- Sidebar Filters
st.sidebar.header("Filter the Data:")

districts = st.sidebar.multiselect(
    "Select District(s):", 
    sorted(crime_data['DISTRICT'].dropna().unique())
)

offense_types = st.sidebar.multiselect(
    "Select Crime Type(s):",
    sorted(crime_data['OFFENSE_CODE_GROUP'].dropna().unique())
)

years = st.sidebar.multiselect(
    "Select Year(s):",
    sorted(crime_data['YEAR'].dropna().unique())
)

months = st.sidebar.multiselect(
    "Select Month(s):",
    sorted(crime_data['MONTH'].dropna().unique())
)

# --- Filter Logic
filtered_data = crime_data.copy()

if districts:
    filtered_data = filtered_data[filtered_data['DISTRICT'].isin(districts)]

if offense_types:
    filtered_data = filtered_data[filtered_data['OFFENSE_CODE_GROUP'].isin(offense_types)]

if years:
    filtered_data = filtered_data[filtered_data['YEAR'].isin(years)]

if months:
    filtered_data = filtered_data[filtered_data['MONTH'].isin(months)]

# --- Main Metrics
st.subheader("📈 Key Statistics")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Crimes", len(filtered_data))

with col2:
    if not filtered_data.empty:
        most_common_crime = filtered_data['OFFENSE_CODE_GROUP'].mode()[0]
        st.metric("Most Common Crime", most_common_crime)
    else:
        st.metric("Most Common Crime", "No data")

with col3:
    if not filtered_data.empty:
        busiest_month = filtered_data['MONTH'].mode()[0]
        st.metric("Busiest Month", busiest_month)
    else:
        st.metric("Busiest Month", "No data")

st.markdown("---")

# --- Heatmap Visualization
st.subheader("🔥 Crime Risk Heatmap")

if not filtered_data.empty and 'Lat' in filtered_data.columns and 'Long' in filtered_data.columns:
    filtered_data = filtered_data.dropna(subset=['Lat', 'Long'])

    heatmap_layer = pdk.Layer(
        "HeatmapLayer",
        data=filtered_data,
        get_position='[Long, Lat]',
        opacity=0.9,
        threshold=0.3,
        get_weight=1
    )

    view_state = pdk.ViewState(
        latitude=filtered_data['Lat'].mean(),
        longitude=filtered_data['Long'].mean(),
        zoom=11,
        pitch=50,
    )

    heatmap = pdk.Deck(
        layers=[heatmap_layer],
        initial_view_state=view_state,
        tooltip={"text": "Crime Hotspot"}
    )

    st.pydeck_chart(heatmap)

else:
    st.warning("No location data available to plot heatmap.")

st.markdown("---")

# --- Monthly Crime Trends
st.subheader("📅 Monthly Crime Trends")
if not filtered_data.empty:
    fig = px.histogram(
        filtered_data,
        x="MONTH",
        color="OFFENSE_CODE_GROUP",
        barmode="group",
        title="Monthly Distribution of Crimes"
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("No data to display for monthly trends.")

# --- Top Offense Types
st.subheader("🔝 Top 10 Crime Types")
if not filtered_data.empty:
    top_offenses = filtered_data['OFFENSE_CODE_GROUP'].value_counts().head(10)
    st.bar_chart(top_offenses)
else:
    st.info("No data to display for top crimes.")

st.markdown("---")

# --- Predictive Model Section
st.subheader("🔮 Predict Crime Likelihood")

# Load the trained model
@st.cache_resource
def get_model():
    return load_model()

model = get_model()

# User input form
with st.form("prediction_form"):
    st.write("Enter details to predict potential crime occurrence:")

    selected_district = st.selectbox(
        "Select District:",
        sorted(crime_data['DISTRICT'].dropna().unique())
    )

    selected_day = st.selectbox(
        "Select Day of Week:",
        ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    )

    selected_hour = st.slider(
        "Select Hour of the Day:", 0, 23, 12
    )

    predict_button = st.form_submit_button("Predict")

if predict_button:
    input_data = {
        "DISTRICT": selected_district,
        "DAY_OF_WEEK": selected_day,
        "HOUR": selected_hour
    }

    prediction = make_prediction(model, input_data)

    st.success(f"🔮 Prediction: {prediction}")

# --- Footer
st.caption("Built with  Falcons For the Future with the Past.")
