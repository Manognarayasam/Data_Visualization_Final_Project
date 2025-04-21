import streamlit as st
import pandas as pd

from Vizs.firstviz import render_first_viz
from Vizs.secondviz import render_second_viz
from Vizs.thirdviz import render_third_viz
from Vizs.fourthviz import render_fourth_viz
from Vizs.fifthviz import render_fifth_viz

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
    padding: 2rem 3rem;
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
    return df

df = load_data()

# === 🚦Filter Controls ===
st.sidebar.header("🔧 Filters")
year = st.sidebar.selectbox("Select Year", sorted(df["Year"].unique()), index=0)
state = st.sidebar.selectbox("Select State", sorted(df["State"].unique()))
severity_levels = st.sidebar.multiselect("Select Severity Levels", [1, 2, 3, 4], default=[1, 2, 3, 4])

# === 🔁 Filtered Data ===
filtered_df = df[
    (df["Year"] == year) &
    (df["State"] == state) &
    (df["Severity"].isin(severity_levels))
]

st.header("US-accidents Dashboard")
# === 🔍 Filter Summary ===
st.markdown(f"### 📅 Year: `{year}` | 📍 State: `{state}` | ⚠️ Severity: `{', '.join(map(str, severity_levels))}`")

# === 🧩 Linked Visuals ===


col1, col2 = st.columns(2)
with col1:
    render_first_viz(filtered_df)
    render_second_viz(filtered_df)

with col2:
    render_third_viz(df, selected_year=year, feature='Traffic_Signal', value=True)
    render_fourth_viz(filtered_df)

st.subheader("🧪 Additional Insights")
render_fifth_viz(filtered_df)
