import streamlit as st
import plotly.graph_objects as go
#divya
def render_third_viz(df, selected_year, feature, value):
    #st.markdown("This chart shows the severity distribution using dot representation (1 dot ≈ 5%) for selected traffic features.")

    severity_colors = {
        1: '#611621',
        2: '#d65961',
        3: '#f7a8b4',
        4: '#b884a7'
    }

    year_df = df[df["Year"] == selected_year]
    filtered = year_df[year_df[feature] == value]
    severity_counts = filtered['Severity'].value_counts()
    total_year_count = len(year_df)

    dots_x, dots_y, colors, hover = [], [], [], []
    for severity in range(1, 5):
        count = severity_counts.get(severity, 0)
        pct = count / total_year_count if total_year_count > 0 else 0
        #dot_count = int(round(pct * 100 / 5))  # 1 dot = 5%
        dot_count = int(round(pct * 100))  # Instead of pct * 100 / 5


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

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=dots_x, y=dots_y, mode='markers',
        marker=dict(size=12, color=colors),
        hovertext=hover, hoverinfo="text"
    ))

    fig.update_layout(
        title=f"Severity Distribution (1 dot ≈ 5%) - {selected_year} | {feature.replace('_', ' ')} = {value}",
        xaxis=dict(title="Severity Level", tickvals=[1, 2, 3, 4], range=[0.5, 4.5]),
        yaxis_title="Dots (1% each)",
        plot_bgcolor="#F9F9F9",
        template="simple_white",
        height=450
    )

    st.plotly_chart(fig, use_container_width=True, key="third_viz_chart")
