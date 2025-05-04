import streamlit as st
import pandas as pd
from Vizs.area_viz import render_first_viz
from Vizs.line_viz import render_second_viz
from Vizs.dotplot_viz import render_third_viz
from Vizs.choroplethmap_viz import render_fourth_viz
from Vizs.bar_viz import render_fifth_viz

st.set_page_config(layout="wide", page_title="US Accidents Scrollytelling")

# Add slight layout improvements
st.markdown("""
    <style>
        .scroll-text {
            padding-top: 3rem;
        }
        .section-container {
            margin-top: 6rem;
            margin-bottom: 6rem;
        }
        .reportview-container {
            overflow-x: hidden;
        }
    </style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    cols = ["Severity", "Start_Time", "Traffic_Signal", "Stop", "Crossing", "State"]
    df = pd.read_csv("US_Accidents_March23.csv", usecols=cols)
    df["Start_Time"] = pd.to_datetime(df["Start_Time"], errors="coerce")
    df.dropna(subset=["Start_Time"], inplace=True)
    df["Year"] = df["Start_Time"].dt.year.astype(int)
    df["Hour"] = df["Start_Time"].dt.hour
    df["DayOfWeek"] = df["Start_Time"].dt.day_name()
    return df

df = load_data()

# Scroll-like layout: full-width block per section
def scrollytell_section(title, desc, viz_func):
    with st.container():
        st.markdown(f"<div class='section-container'>", unsafe_allow_html=True)
        col1, col2 = st.columns([1.2, 0.8])

        with col1:
            viz_func(df)

        with col2:
            st.markdown(f"<div class='scroll-text'><h2>{title}</h2><p>{desc}</p></div>", unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

# === All Sections ===
scrollytell_section(" Severity Over Time", "Explore how accident severity evolved from 2016 to 2023.", render_first_viz)
scrollytell_section(" Hourly Trends", "See how accident frequency changes by hour of day.", render_second_viz)
scrollytell_section(" City Representation", "Dot representation of accident severity by feature presence.", render_third_viz)
scrollytell_section(" Weather Impact", "Severity 4 accidents per 100,000 people normalized by year and state.", render_fourth_viz)
scrollytell_section(" Custom Insights", "Deep dive into custom filters and patterns in the accident data.", render_fifth_viz)
