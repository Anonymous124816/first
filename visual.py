
import pandas as pd
import streamlit as st
import plotly.express as px
import os
import numpy as np
import streamlit_card
# from streamlit_extras import *
#import streamlit_vertical_slider as sv
import gdown as gd
from millify import millify
import plotly.graph_objects as go



# from streamlit_card import streamlit_card

# import millify


st.set_page_config(
    page_icon="🕊️",
    page_title="Global Death Analysis",
    initial_sidebar_state="auto",
    layout="wide"
)

st.title(
    "🌍 World Death Analysis 💔",
)
st.write(
    "Death is a cup from which every living being drinks eventually.",
    unsafe_allow_html=True,
)

st.divider()
# st.write('---',)
# os.chdir(path="F:\anonymous\ml\deaths")
url =  'https://drive.google.com/file/d/1m9KFCbeiO_8ZBpmPBAquCSyzFTTo1_Sm/view?usp=sharing'
file_id = url.split('/')[-2]

download_url = 'https://drive.google.com/uc?id={}'.format(file_id)

data = gd.download(download_url, 'deaths_final_location.csv', quiet=False)

df = pd.read_csv(data)

filtered_df = df.copy()


key_main_slider = "main_slider_key"
key_sidebar_slider = "sidebar_slider_key"


# with st.columns()
year_range_slider = st.select_slider(
    label="Year",
    options=[i for i in range(1990, 2020)],
    value=(1990, 2019),
    label_visibility="hidden",
    key=key_main_slider,
)

df_new = filtered_df[
    filtered_df["year"].between(year_range_slider[0], year_range_slider[1])
]

with st.sidebar:
    st.header("Filters")
    st.divider()
    # sidebar_year_range_slider = st.select_slider(
    #     label="Year",
    #     options=[i for i in range(1990, 2020)],
    #     value=year_range_slider,
    #     label_visibility="collapsed",
    #     key=key_sidebar_slider,
    # )
    st.write("Select Your option")
    st.divider()
    tab1, tab2, tab3 = st.tabs(
        ["Area", "Cause", "Financial"],
    )

    with tab1:
        with st.expander("Continent-Wise"):
            continent_sb = st.multiselect(
                ("Continent"),
                df_new["continent"].unique(),
                placeholder="Multiselect",
                default=df_new["continent"].unique(),
            )

            if not continent_sb:
                df2 = df_new.copy()
            else:
                df2 = df_new[df_new["continent"].isin(continent_sb)].copy()
        with st.expander("Region-Wise"):
            region_sb = st.multiselect(
                "Region",
                df2["region"].unique(),
                placeholder="Multiselect",
                default=df2["region"].unique(),
            )
            if not region_sb:
                df3 = df2.copy()
            else:
                df3 = df2[df2["region"].isin(region_sb)].copy()

    with tab2:
        with st.expander("Causes-Category"):
            cause_cat_sb = st.multiselect(
                "Causes Category",
                df3["cause_cat"].unique(),
                placeholder="Multiselect",
                default=df3["cause_cat"].unique(),
            )
            if not cause_cat_sb:
                df4 = df3.copy()
            else:
                df4 = df3[df3["cause_cat"].isin(cause_cat_sb)].copy()
        with st.expander("Specific Causes"):
            causes_sb = st.multiselect(
                "Causes (33 causes)",
                df4["causes"].unique(),
                placeholder="Multiselect",
                default=df4["causes"].unique(),
            )
            if not causes_sb:
                df5 = df4.copy()
            else:
                df5 = df4[df4["causes"].isin(causes_sb)].copy()

    with tab3:
        with st.expander("Income-Group"):
            income_group_sb = st.multiselect(
                "Income Group",
                df5["income_group"].unique(),
                placeholder="Multiselect",
                default=df5["income_group"].unique(),
            )
            if not income_group_sb:
                df6 = df5.copy()
            else:
                df6 = df5[df5["income_group"].isin(income_group_sb)].copy()
        with st.expander("Country Status"):
            country_status_sb = st.multiselect(
                "Country Status",
                df6["country_status"].unique(),
                placeholder="Multiselect",
                default=df6["country_status"].unique(),
            )
            if not country_status_sb:
                df7 = df6.copy()
            else:
                df7 = df6[df6["country_status"].isin(country_status_sb)].copy()


df = df7.copy()

sum_deaths = df.groupby("continent")["deaths"].sum().reset_index()

max_death_value = sum_deaths["deaths"].max()
continent_with_max_deaths = sum_deaths.loc[
    sum_deaths["deaths"] == max_death_value, "continent"
].values[0]

min_death_value = sum_deaths["deaths"].min()
continent_with_min_deaths = sum_deaths.loc[
    sum_deaths["deaths"] == min_death_value, "continent"
].values[0]

st.divider()
met1, met2, met3, met4, met5 = st.columns(5)

met1.metric("Total Deaths", millify(sum_deaths["deaths"].sum()))

met2.metric(f"{continent_with_max_deaths} (max deaths)", millify(max_death_value))


start_year = year_range_slider[0]
end_year = year_range_slider[1]

total_years = end_year - start_year

st.write(total_years)

total_deaths = sum_deaths["deaths"].sum()  # Total number of deaths
max_percentage_burden = (
    max_death_value / total_deaths
) * 100  # Calculate the percentage

min_percentage_burden = (min_death_value / total_deaths) * 100
met3.metric(
    label=f"{continent_with_max_deaths} percentage",
    value=f"{max_percentage_burden:.2f}%",  # Format the percentage with 2 decimal places
)

met4.metric(f"{continent_with_min_deaths} (min deaths)", millify(max_death_value))

met5.metric(
    label=f"{continent_with_min_deaths} percentage",
    value=f"{min_percentage_burden:.2f}%",
)


col1, col2 = st.columns(2,gap="small")
with col1:
    fig = px.pie(
        sum_deaths,
        names="continent",
        values="deaths",
        color="continent",
        hole=0.5,
        title="Continent Wise",
    )
    fig.update_traces(
        textinfo="percent",
    )
    st.plotly_chart(
        fig, use_container_width=True, aspect_ratio=1.0, use_container_height=True
    )

with col2:
    fig_hist_country_status = px.histogram(
    df,
    x="country_status",
    color="country_status",
    title="Distribution of Deaths by Country Status",
    labels={"deaths": "Total Deaths", "country_status": "Country Status"},
    )
    st.plotly_chart(fig_hist_country_status, use_container_width=True)


df_new = df[df["year"].between(year_range_slider[0], year_range_slider[1])]

# Calculate the total deaths for each continent for the selected range
# Calculate the total deaths for each continent for the selected range
total_deaths_by_continent = df_new.groupby(["continent", "year"])["deaths"].sum().reset_index()


# Calculate the change in deaths relative to the previous 5 years
total_deaths_by_continent["deaths_change"] = total_deaths_by_continent.groupby("continent")["deaths"].diff(5)

# Line chart showing the change in deaths relative to the previous 5 years by continent
fig_line_change = px.line(
    total_deaths_by_continent,
    x="year",
    y="deaths_change",
    color="continent",
    title="Change in Deaths Relative to Previous 5 Years by Continent",
    labels={"deaths_change": "Change in Deaths", "year": "Year", "continent": "Continent"},
)

# Display the line chart with legend and colors
fig_line_change.update_layout(legend=dict(title="Continent"), showlegend=True)

# Display the line chart
st.plotly_chart(fig_line_change, use_container_width=True)

# fig = go.Figure()

# # Add a scattergeo layer for each continent
# for continent, data in df.groupby('continent'):
#     fig.add_trace(go.Scattergeo(
#         lon=data['long'],
#         lat=data['lat'],
#         text=data['deaths'],
#         mode='markers',
#         marker=dict(size=data['deaths'], color=data['deaths'], colorscale='Viridis', opacity=0.7),
#         name=continent
#     ))

# # Customize the layout of the map
# fig.update_geos(projection_type="natural earth")
# fig.update_layout(
#     title='Deaths by Continent on World Map',
#     geo=dict(showland=True, landcolor="rgb(240, 240, 240)"),
# )

# # Display the map
# st.plotly_chart(fig, use_container_width=True)
    
# fig_line = px.line(
#     df,
#     x="year",
#     y="deaths",
#     color="continent",
#     title="Deaths Over Time by Continent",
#     labels={"deaths": "Total Deaths", "year": "Year", "continent": "Continent"},
# )

# # Display the line chart
# st.plotly_chart(fig_line, use_container_width=True)

# fig_hist_country_status = px.histogram(
#     df,
#     x="country_status",
#     color="country_status",
#     title="Distribution of Deaths by Country Status",
#     labels={"deaths": "Total Deaths", "country_status": "Country Status"},
# )
# st.plotly_chart(fig_hist_country_status, use_container_width=True)


# col1, col2 = st.columns(2)

# # Display the charts side by side
# with col1:
#     st.plotly_chart(fig_line, use_container_width=True)

# with col2:
#     st.plotly_chart(fig_hist_country_status, use_container_width=True)

