import streamlit as st
import plotly.express as px
#Bhavitha
def render_fourth_viz(df):
    df["Year"] = df["Year"].astype(int)
    df_severe = df[df['Severity'] == 4].copy()

    if df_severe.empty:
        st.warning("No Severity 4 data available for the selected filters.")
        return

    state_year = df_severe.groupby(['State', 'Year']).size().reset_index(name='Severe_Accident_Count')

    # Population mapping (must be inside the function)
    pop_2016 = {
        'CA': 39144818, 'TX': 27862596, 'FL': 20612439, 'NY': 19745289, 'PA': 12802503,
        'IL': 12801539, 'OH': 11614373, 'GA': 10414841, 'NC': 10146788, 'MI': 9922576,
        'NJ': 8935871, 'VA': 8411808, 'WA': 7288000, 'AZ': 6931071, 'MA': 6811779,
        'TN': 6651194, 'IN': 6633053, 'MO': 6109796, 'MD': 6016447, 'WI': 5771337,
        'CO': 5540545, 'MN': 5519952, 'SC': 4961119, 'AL': 4863300, 'LA': 4681666,
        'KY': 4436974, 'OR': 4093465, 'OK': 3923561, 'CT': 3588184, 'UT': 3051217,
        'IA': 3134693, 'NV': 2940058, 'AR': 2988726, 'MS': 2988727, 'KS': 2907289,
        'NM': 2081015, 'NE': 1907116, 'WV': 1831102, 'ID': 1680710, 'HI': 1428557,
        'NH': 1331479, 'ME': 1330650, 'RI': 1052917, 'MT': 1052917, 'DE': 952065,
        'SD': 865454, 'ND': 757952, 'AK': 741204, 'VT': 624594, 'WY': 585501, 'DC': 681170
    }

    state_year['Population'] = state_year['State'].map(pop_2016)
    state_year.dropna(subset=["Population"], inplace=True)

    state_year['Severe_Accidents_per_100k'] = (
        state_year['Severe_Accident_Count'] / state_year['Population']
    ) * 100000

    if state_year.empty:
        st.warning("No mapped states have population or severity 4 accidents.")
        return

    fig = px.choropleth(
        state_year,
        locations='State',
        locationmode='USA-states',
        color='Severe_Accidents_per_100k',
        animation_frame='Year',
        scope='usa',
        color_continuous_scale='Reds',
        range_color=[0, state_year['Severe_Accidents_per_100k'].max()],
        labels={
            'Severe_Accidents_per_100k': 'Accidents per 100k',
            'State': 'State',
            'Year': 'Year'
        },
        title='Yearly Severity 4 Accidents per 100,000 People (Normalized by 2016 Population)'
    )
    #viz
    fig.update_layout(
        coloraxis_colorbar=dict(
            title='Per 100k People',
            tickvals=[0, 5, 10, 15, 20, 25, 30, 40],
            ticktext=['0', '5', '10', '15', '20', '25', '30', '40+']
        ),
        geo=dict(showlakes=True, lakecolor='rgb(255, 255, 255)')
    )

    st.plotly_chart(fig, use_container_width=True, key="fourth_viz_chart")
