#D:\Data_Visuvalization\Data_Visualization_Final_Project\Dashboard_final.py
import streamlit as st
import pandas as pd
from Vizs.area_viz import render_area_viz
from Vizs.line_viz import render_line_viz
from Vizs.dotplot_viz import dot_plot_render
from Vizs.choroplethmap_viz import render_choroplethmap_viz
from Vizs.bar_viz import bar_viz
from Vizs.donut_viz import render_donut_chart

st.set_page_config(layout="wide")
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
st.markdown("""
<style>
body {
    background-color: #FFF5F7; /* light blush base */
}

[data-testid="stAppViewContainer"] {
    background-color: #FFF5F7;
}

.block-container {
    padding: 1rem 3rem;
    background-color: #FFF5F7;
}

h1, h2, h3, h4, h5, h6 {
    color: #4B1F2D;  /* deep plum for headers */
}

.stMarkdown, .stText, .stDataFrame {
    color: #7A1F1F;  /* soft dark red for text */
}

.stSidebar {
    background-color: #F29CAB; /* soft pink sidebar */
    color: #4B1F2D;
}

.stButton>button {
    background-color: #E25B5B;
    color: white;
    border: none;
}

.stButton>button:hover {
    background-color: #B38BA3;
    color: white;
}
</style>
""", unsafe_allow_html=True)


@st.cache_data
def load_data():
    df = pd.read_csv("US_Accidents_March23.csv", usecols=["Severity", "Start_Time", "State", "Traffic_Signal", "Stop", "Crossing"])
    df["Start_Time"] = pd.to_datetime(df["Start_Time"], errors="coerce")
    df.dropna(subset=["Start_Time"], inplace=True)
    df["Year"] = df["Start_Time"].dt.year
    df["Hour"] = df["Start_Time"].dt.hour
    df["DayOfWeek"] = df["Start_Time"].dt.day_name()
    df['Start_Time'] = pd.to_datetime(df['Start_Time'])
    df['Year'] = df['Start_Time'].dt.year
    df['Month'] = df['Start_Time'].dt.month
    df['Day_of_Week'] = df['Start_Time'].dt.day_name()
    return df


df = load_data()

# === 🚦Filter Controls ===
st.sidebar.header(" Filters")
year = st.sidebar.selectbox("Select Year", sorted(df["Year"].unique()), index=0)
#state = st.sidebar.selectbox("Select State", sorted(df["State"].unique()))
severity_levels = st.sidebar.multiselect("Select Severity Levels", [1, 2, 3, 4], default=[1, 2, 3, 4])

# === 🔁 Filtered Data ===
filtered_df = df[
    (df["Year"] == year) &
    (df["Severity"].isin(severity_levels))
]

# Example of grouping accident causes - assuming column exists
if 'Accident_Cause' in df.columns:
    df['Cause_Grouped'] = df['Accident_Cause'].replace({
        'Vehicle Lost Control': 'Driver Error',
        'Drunk Driving': 'Impaired Driving',
        'Speeding': 'Driver Error',
        'Distracted Driving': 'Driver Error',
        'Poor Weather': 'Environmental',
        'Mechanical Failure': 'Vehicle Failure'
    })
else:
    df['Cause_Grouped'] = 'Unknown'

# Normalize Severity (as proxy for injury severity)
df['Severity_Norm'] = (df['Severity'] - df['Severity'].min()) / (df['Severity'].max() - df['Severity'].min())
st.header("Analysis of US Road Accidents from 2016-2023")
# === 🔍 Filter Summary ===
st.markdown(f"### 📅 Year: `{year}`  | ⚠️ Severity: `{', '.join(map(str, severity_levels))}`")


# === Summary Metrics ===
#st.markdown("### 📈 Dashboard Summary")
metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)

# Total accidents
total_accidents = len(filtered_df)
metric_col1.metric("Total Accidents", f"{total_accidents:,}")

# Most common severity
most_common_severity = filtered_df['Severity'].mode()[0]
metric_col2.metric("Most Common Severity", f"Level {most_common_severity}")

# Hour with most accidents
peak_hour = filtered_df['Hour'].mode()[0]
metric_col3.metric("Peak Hour", f"{peak_hour}:00")

# Most common day
common_day = filtered_df['DayOfWeek'].mode()[0]
metric_col4.metric("Busiest Day", common_day)

# === 🧩 Linked Visuals ===


col1, col2 = st.columns(2)
with col1:
    st.markdown("#### Severity Level Trends Over Years")
    render_area_viz(filtered_df)
    st.caption("Accident severity steadily increased from 2016 to 2021.")

    st.markdown("#### Weekly Accident Severity Distribution")
    bar_viz(filtered_df)
    st.caption("Weekdays see more severe accidents, especially mid-week.")
    

with col2:
    st.markdown("#### Hourly Accidents by Day")
    render_line_viz(filtered_df)
    st.caption("Hourly accident patterns vary significantly across weekdays." )
    
    st.markdown("#### Severity Proportion Distribution")
    render_donut_chart(filtered_df)
    st.caption("Donut chart shows proportion of each severity level in the filtered data.")
   
    
st.markdown("--------------")
st.subheader("Severity Distribution of Accidents by Traffic Control Features (like Traffic signals, Crossings and Stop Sign) over the years")
dot_plot_render(df)
st.caption("This dot plot illustrates how the presence or absence of traffic control elements like traffic signals, stop signs, and pedestrian crossings, impacts the severity distribution of traffic accidents across different years in the U.S.")


st.markdown("--------------")
st.subheader("Yearly Severity 4 Accidents per 100,000 People (Normalized by 2016 Population)")
render_choroplethmap_viz(df)
st.caption("This animated map shows the evolution of Severity 4 traffic accidents, those with the most critical outcomes, across U.S. states from 2016 to 2023. Normalized by 2016 population figures, it highlights how the rate of severe accidents per 100,000 residents has shifted over time, with darker shades revealing areas experiencing high accident severity.")


st.markdown("--------------")
st.subheader("Additional Insights")
st.image("assets/Chrisviz.jpg", use_container_width=True)