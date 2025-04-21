import streamlit as st
import plotly.express as px

def render_fifth_viz(df):
    st.markdown("This chart shows how accident severity has changed year by year from 2016 to 2023.")

    # === Custom Flower-Inspired Colors ===
    colors = ["#7A1F1F", "#E25B5B", "#F29CAB", "#B38BA3", "#4B1F2D"]

    # === Group Data by Year & Severity ===
    severity_counts = df.groupby(["Year", "Severity"]).size().reset_index(name="Count")

    # === Area Chart ===
    fig_area = px.area(
        severity_counts,
        x="Year",
        y="Count",
        color="Severity",
        title="Severity Level Trends Per Year",
        category_orders={"Severity": [1, 2, 3, 4]},
        color_discrete_sequence=colors
    )

    fig_area.update_layout(
        font=dict(family="Segoe UI", size=14),
        plot_bgcolor="#F9F9F9",
        margin=dict(t=60, b=40, l=40, r=40)
    )

    #st.plotly_chart(fig_area, use_container_width=True)
    st.plotly_chart(fig_area, use_container_width=True, key="fifth_viz_chart")



