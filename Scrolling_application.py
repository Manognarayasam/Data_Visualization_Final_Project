import streamlit as st
import pandas as pd

# ✅ FIRST Streamlit command
st.set_page_config(layout="wide", page_title="US Accidents Scrollytelling")

from Vizs.area_viz import render_first_viz
from Vizs.line_viz import render_second_viz
from Vizs.dotplot_viz import render_third_viz
from Vizs.choroplethmap_viz import render_fourth_viz
from Vizs.bar_viz import render_fifth_viz

# Remove top padding
st.markdown(
    """
    <style>
        .block-container {
            padding-top: 1rem;
        }
    </style>
    """,
    unsafe_allow_html=True
)
 
@st.cache_data
def load_data():
    cols_needed = [
        "Severity", "Start_Time", "Traffic_Signal", "Stop", "Crossing", "State"
    ]

    df = pd.read_csv("US_Accidents_March23.csv", usecols=cols_needed)

    # Explicitly convert Start_Time to datetime
    df["Start_Time"] = pd.to_datetime(df["Start_Time"], errors='coerce')

    # Drop rows where Start_Time couldn't be parsed
    df = df.dropna(subset=["Start_Time"])

    # Extract Year
    df["Year"] = df["Start_Time"].dt.year.astype(int)
    df["Hour"] = df["Start_Time"].dt.hour
    df["DayOfWeek"] = df["Start_Time"].dt.day_name()

    return df

df = load_data()  # This loads and defines 'df'

st.title("🚦 US Traffic Accidents (2016–2023)")
st.markdown("This dashboard aggregates and visualizes traffic data from 2016 to 2023.")

tabs = st.tabs([
    "📊 Severity Over Time",
    "🕒 Hourly Trends",
    "🔥 c representation",
    "🌦️ Weather Impact",
    "🧪 Custom Insights"
])

with tabs[0]:
    render_first_viz(df)

with tabs[1]:
    render_second_viz(df)

with tabs[2]:
    render_third_viz(df)
    

with tabs[3]:
    render_fourth_viz(df)
    

with tabs[4]:
    render_fifth_viz(df)
  

