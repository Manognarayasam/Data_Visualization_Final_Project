import streamlit as st
import pandas as pd
import plotly.express as px

def render_donut_chart(df):
    
    # severity_counts = df["Severity"].value_counts().sort_index()
    severity_counts = df["Severity"].value_counts()
    severity_labels = {
        1: "1 - Low",
        2: "2 - Moderate",
        3: "3 - Serious",
        4: "4 - Critical"
    }

    labeled_names = [severity_labels.get(s, str(s)) for s in severity_counts.index]
    fig = px.pie(
        names=labeled_names,
        values=severity_counts.values,
        #title="Severity Distribution",
        hole=0.5,  # for donut style
        color=severity_counts.index,
        color_discrete_sequence=['#611621', '#d65961', '#f7a8b4', '#b884a7']
    )
    fig.update_traces(textinfo='percent+label')
    st.plotly_chart(fig, use_container_width=True)
