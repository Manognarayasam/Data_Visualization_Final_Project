import streamlit as st
import plotly.express as px
import pandas as pd

def bar_viz(df):
    
    if df.empty:
        st.warning("No data available for selected filters.")
        return

    # Ensure weekday order
    day_order = [
        "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"
    ]
    df["DayOfWeek"] = pd.Categorical(df["DayOfWeek"], categories=day_order, ordered=True)

    # Cast severity as string for discrete coloring
    df["Severity"] = df["Severity"].astype(str)

    # Grouped data
    grouped = df.groupby(["DayOfWeek", "Severity"]).size().reset_index(name="Count")

    # Flower palette colors for severity 1 to 4
    flower_palette = ["#7A1F1F", "#E25B5B", "#F29CAB", "#B38BA3"]

    fig = px.bar(
        grouped,
        x="DayOfWeek",
        y="Count",
        color="Severity",
        #title="Accident Counts by Day of the Week and Severity",
        category_orders={"DayOfWeek": day_order, "Severity": ["1", "2", "3", "4"]},
        color_discrete_sequence=flower_palette
    )

    fig.update_layout(
        font=dict(family="Segoe UI", size=14),
        plot_bgcolor="#FFF5F7",
        margin=dict(t=60, b=40, l=40, r=40)
    )

    st.plotly_chart(fig, use_container_width=True, key="fifth_viz_chart")
