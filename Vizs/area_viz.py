#D:\Data_Visuvalization\Data_Visualization_Final_Project\Vizs\area_viz.py
import streamlit as st
import plotly.express as px
import pandas as pd

def render_area_viz(df):
    #st.markdown("This chart shows how accident severity has changed year by year from 2016 to 2023.")

    # Ensureing proper year format
    df["Year"] = df["Year"].astype(int)

    # Defineing the full year and severity range
    all_years = list(range(2016, 2024))
    #all_severities = [1, 2, 3, 4] 
    all_severities = df["Severity"].unique()


    # Createing a complete index for (year, severity)
    idx = pd.MultiIndex.from_product([all_years, all_severities], names=["Year", "Severity"])
    severity_counts = df.groupby(["Year", "Severity"]).size().reindex(idx, fill_value=0).reset_index(name="Count")

    # Flower-inspired severity colors
    colors = ["#7A1F1F", "#E25B5B", "#F29CAB", "#B38BA3"]

    fig = px.area(
        severity_counts,
        x="Year",
        y="Count",
        color="Severity",
        #title="Severity Level Trends Per Year",
        category_orders={"Severity": all_severities},   
        color_discrete_sequence=colors
    )

    fig.update_layout(
        font=dict(family="Segoe UI", size=14),
        plot_bgcolor="#F9F9F9",
        margin=dict(t=60, b=40, l=40, r=40)
    )

    st.plotly_chart(fig, use_container_width=True, key="first_viz_chart")
