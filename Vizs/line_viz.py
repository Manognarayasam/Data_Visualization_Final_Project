import streamlit as st
import pandas as pd
import plotly.express as px

def render_line_viz(df):
    #4st.markdown("This animated line chart shows the number of accidents for each hour across different weekdays.")

    # Defineing color palette
    colors = ["#7A1F1F", "#E25B5B", "#F29CAB", "#B38BA3", "#4B1F2D"]

    # Prepareing data: Hour vs DayOfWeek
    hour_day = df.groupby(["DayOfWeek", "Hour"]).size().reset_index(name="Accidents")
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    hour_day["DayOfWeek"] = pd.Categorical(hour_day["DayOfWeek"], categories=day_order, ordered=True)

    # Plot animated line chart
    fig_line = px.line(
        hour_day,
        x="Hour",
        y="Accidents",
        animation_frame="DayOfWeek",
        #title="Hourly Accidents Across Weekdays",
        markers=True,
        line_shape="spline",
        color_discrete_sequence=[colors[2]]
    )

    fig_line.update_traces(line=dict(width=3), hovertemplate="Hour: %{x}h<br>Accidents: %{y:,}")
    fig_line.update_layout(
        xaxis=dict(title="Hour of Day", dtick=1),
        yaxis_title="Accident Count",
        plot_bgcolor="#F9F9F9",
        font=dict(family="Segoe UI", size=14),
        margin=dict(t=80, b=60, l=60, r=60)
    )

    #st.plotly_chart(fig_line, use_container_width=True)
    st.plotly_chart(fig_line, use_container_width=True, key="second_viz_chart")

