import pandas as pd
import plotly.graph_objects as go
import streamlit as st


def dot_plot_render(df):
    #STEP 1: Load the dataset
    #df = pd.read_csv("US_Accidents_March23.csv", usecols=["Start_Time", "Traffic_Signal", "Stop", "Crossing", "Severity"])
    # df["Start_Time"] = df["Start_Time"].str.replace(r"\.\d+", "", regex=True)
    # df["Year"] = pd.to_datetime(df["Start_Time"]).dt.year

    df["Start_Time"] = pd.to_datetime(df["Start_Time"], errors='coerce')
    df["Year"] = df["Start_Time"].dt.year

    df = df[df["Year"].between(2016, 2023)]
    df.dropna(subset=["Traffic_Signal", "Stop", "Crossing", "Severity"], inplace=True)

    # STEP 2: Set the colors accordingly
    severity_colors = {
        1: '#611621',
        2: '#d65961',
        3: '#f7a8b4',
        4: '#b884a7'
    }

    # STEP 3: Dot calculation function ( with normalization)
    def compute_dots(feature, value, year):
        year_df = df[df["Year"] == year]
        total = len(year_df)
        filtered = year_df[year_df[feature] == value]
        severity_counts = filtered['Severity'].value_counts()

        dots_x, dots_y, colors, hover = [], [], [], []
        for sev in range(1, 5):
            pct = severity_counts.get(sev, 0) / total if total > 0 else 0
            dot_count = int(round(pct * 100 / 5))
            for i in range(1, dot_count + 1):
                dots_x.append(sev)
                dots_y.append(i)
                colors.append(severity_colors[sev])
                hover.append(f"{feature}={value}<br>Severity {sev}<br>{pct*100:.1f}%")
            if dot_count == 0:
                dots_x.append(sev)
                dots_y.append(0)
                colors.append("rgba(0,0,0,0)")
                hover.append(f"{feature}={value}<br>Severity {sev}<br>0.0%")
        return dots_x, dots_y, colors, hover

    # STEP 4: Seting up the year & traffic feature options
    years = list(range(2016, 2024))
    features = [("Traffic_Signal", True), ("Traffic_Signal", False),
                ("Crossing", True), ("Crossing", False),
                ("Stop", True), ("Stop", False)]

    traces, trace_labels = [], []

    for year in years:
        for feature, val in features:
            label = f"{year}_{feature}_{val}"
            x, y, color, hover = compute_dots(feature, val, year)
            traces.append(go.Scatter(
                x=x, y=y, mode='markers',
                marker=dict(size=12, color=color),
                name=label,
                visible=False,
                hovertext=hover, hoverinfo="text"
            ))
            trace_labels.append(label)

    # STEP 5: Set default visible trace
    default_year = 2016
    default_feature = "Traffic_Signal"
    default_value = True
    default_label = f"{default_year}_{default_feature}_{default_value}"
    for i, lbl in enumerate(trace_labels):
        if lbl == default_label:
            traces[i].visible = True

    # STEP 6: Interactive buttons (year + feature combo)
    buttons = []
    for year in years:
        for feature, val in features:
            label = f"{year}_{feature}_{val}"
            vis = [lbl == label for lbl in trace_labels]
            title = f"Severity Distribution during the year - {year} and when {feature.replace('_',' ')} = {val}"
            buttons.append(dict(
                label=f"{year} | {feature.replace('_',' ')} = {val}",
                method="update",
                args=[{"visible": vis}, {"title": title}]
            ))

    # STEP 7: Layout and plot
    fig = go.Figure(data=traces)
    fig.update_layout(
        updatemenus=[dict(buttons=buttons, direction="down", x=0.4, y=1.15)],
        title=f"Severity Distribution (where each dot is 5% approximately) - {default_year} | {default_feature.replace('_',' ')} = {default_value}",
        xaxis=dict(title="Severity Levels (1 is least severe ~ 4 is most severe)", tickvals=[1, 2, 3, 4], range=[0.5, 4.5]),
        yaxis_title="No. of Dots(where 1dot= 5% of accidents in that year)",
        template="plotly_white",
        height=450
    )



    st.plotly_chart(fig, use_container_width=True)

