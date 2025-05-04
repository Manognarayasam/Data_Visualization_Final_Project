import pandas as pd
import plotly.graph_objects as go
import streamlit as st


def dot_plot_render(df):
    #  Load and preprocess the dataset
    #df = pd.read_csv("../US_Accidents_March23.csv", usecols=["Start_Time", "Traffic_Signal", "Stop", "Crossing", "Severity"])
    # Extracting only the year from the Start_Time
    # df["Start_Time"] = df["Start_Time"].str.replace(r"\.\d+", "", regex=True)
    # df["Year"] = pd.to_datetime(df["Start_Time"]).dt.year

    df["Start_Time"] = pd.to_datetime(df["Start_Time"], errors='coerce')
    df["Year"] = df["Start_Time"].dt.year

    df = df[df["Year"].between(2016, 2023)]
    df.dropna(subset=["Traffic_Signal", "Stop", "Crossing", "Severity"], inplace=True)

    # Selecting the Color palette for each severity level
    severity_colors = {
        1: '#611621',
        2: '#d65961',
        3: '#f7a8b4',
        4: '#b884a7'
    }

    # Dot generator function based on selected year & feature the
    def compute_dots_by_year(feature, value, year):
        year_df = df[df["Year"] == year]
        filtered = year_df[year_df[feature] == value]
        severity_counts = filtered['Severity'].value_counts()
        total_year_count = len(year_df)

        dots_x, dots_y, colors, hover = [], [], [], []
        for severity in range(1, 5):
            count = severity_counts.get(severity, 0)
            pct = count / total_year_count if total_year_count > 0 else 0
            dot_count = int(round(pct * 100 / 5))  # 1 dot = 5%

            for i in range(1, dot_count + 1):
                dots_x.append(severity)
                dots_y.append(i)
                colors.append(severity_colors[severity])
                hover.append(f"{pct*100:.1f}%")

            if dot_count == 0:
                dots_x.append(severity)
                dots_y.append(0)
                colors.append('rgba(0,0,0,0)')
                hover.append("0.0%")

        return dots_x, dots_y, colors, hover

    # STEP 6: Setup all possible years and filters
    years = list(range(2016, 2024))
    feature_conditions = [
        ("Traffic_Signal", True),
        ("Traffic_Signal", False),
        ("Crossing", True),
        ("Crossing", False),
        ("Stop", True),
        ("Stop", False)
    ]

    # STEP 7: Create traces for all combinations
    traces = []
    trace_labels = []

    for year in years:
        for feature, val in feature_conditions:
            label = f"{year}_{feature}_{val}"
            x, y, color, hover = compute_dots_by_year(feature, val, year)
            traces.append(go.Scatter(
                x=x, y=y, mode='markers',
                marker=dict(size=12, color=color),
                name=label,
                visible=(label == "2023_Traffic_Signal_True"),
                hovertext=hover,
                hoverinfo="text"
            ))
            trace_labels.append(label)

    # STEP 8: Create dropdowns separately for year and filter
    year_buttons = []
    for year in years:
        vis = [label.startswith(f"{year}_") and label.endswith("Traffic_Signal_True") for label in trace_labels]
        year_buttons.append(dict(
            label=str(year),
            method="update",
            args=[{"visible": vis}, {"title": f"Severity Distribution (Percentage:1 dot = 5%) - {year} | Traffic_Signal = True"}]
        ))

    filter_buttons = []
    for feature, val in feature_conditions:
        vis = [label.endswith(f"{feature}_{val}") and label.startswith("2023_") for label in trace_labels]
        label_text = f"{feature.replace('_', ' ')} = {val}"
        filter_buttons.append(dict(
            label=label_text,
            method="update",
            args=[{"visible": vis}, {"title": f"Severity Distribution (percentage:1 dot = 5%) - 2023 | {label_text}"}]
        ))

    # STEP 9: Layout the figure with both dropdowns
    fig = go.Figure(data=traces)
    fig.update_layout(
        updatemenus=[
            dict(
                buttons=year_buttons,
                direction="down",
                showactive=True,
                x=0.1,
                xanchor="left",
                y=1.15,
                yanchor="top"
            ),
            dict(
                buttons=filter_buttons,
                direction="down",
                showactive=True,
                x=0.45,
                xanchor="left",
                y=1.15,
                yanchor="top"
            )
        ],
        title="Severity Distribution (Percentage:1 dot = 5%) - 2023 | Traffic_Signal = True",
        xaxis=dict(
            title="Severity Level (1 = Least Severe, 4 = Most Severe)",
            tickmode="array",
            tickvals=[1, 2, 3, 4],
            range=[0.5, 4.5]
        ),
        yaxis_title="Dots (~5% each of accidents in selected year)",
        template="plotly_white",
        height=450
    )

    #fig.show()
    st.plotly_chart(fig, use_container_width=True)

