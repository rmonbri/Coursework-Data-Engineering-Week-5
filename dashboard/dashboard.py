from os import environ as ENV
import csv
from dotenv import load_dotenv
import pandas as pd
import streamlit as st
import pyodbc
from datetime import datetime, timedelta
import altair as alt


# @st.cache_data
# def get_UN_data():
#     AWS_BUCKET_URL = "https://streamlit-demo-data.s3-us-west-2.amazonaws.com"
#     df = pd.read_csv(AWS_BUCKET_URL + "/agri.csv.gz")
#     return df.set_index("Region")


# try:
#     df = get_UN_data()
#     countries = st.multiselect(
#         "Choose countries", list(df.index), [
#             "China", "United States of America"]
#     )
#     if not countries:
#         st.error("Please select at least one country.")
#     else:
#         data = df.loc[countries]
#         data /= 1000000.0
#         st.subheader("Gross agricultural production ($B)")
#         st.dataframe(data.sort_index())

#         data = data.T.reset_index()
#         data = pd.melt(data, id_vars=["index"]).rename(
#             columns={"index": "year",
#                      "value": "Gross Agricultural Product ($B)"}
#         )
#         chart = (
#             alt.Chart(data)
#             .mark_area(opacity=0.3)
#             .encode(
#                 x="year:T",
#                 y=alt.Y("Gross Agricultural Product ($B):Q", stack=None),
#                 color="Region:N",
#             )
#         )
#         st.altair_chart(chart, use_container_width=True)
# except URLError as e:
#     st.error(
#         f"This demo requires internet access. Connection error: {e.reason}")

def get_conn():
    conn_str = (f"DRIVER={{{ENV['DB_DRIVER']}}};SERVER={ENV['DB_HOST']};"
                f"PORT={ENV['DB_PORT']};DATABASE={ENV['DB_NAME']};"
                f"UID={ENV['DB_USERNAME']};PWD={ENV['DB_PASSWORD']};Encrypt=no;")

    conn = pyodbc.connect(conn_str)

    return conn


def execute_query(conn, q: str):
    cur = conn.cursor()
    cur.execute(q)
    data = cur.fetchall()
    return data


# def get_df_from_csv(filename: csv):
#     return pd.read_csv(filename)


# def get_df_from_sql(query, conn):
#     return pd.read_sql(query, conn)

def get_plant_information(conn) -> pd.DataFrame:
    '''Queries the database, returns and merges tables'''
    plant_type_df = pd.read_sql('SELECT * FROM plant_type', conn)
    botanist_df = pd.read_sql('SELECT * FROM botanist', conn)
    origin_df = pd.read_sql('SELECT * FROM origin', conn)
    plant_df = pd.read_sql('SELECT * FROM plant', conn)
    merged_plant_with_type = pd.merge(plant_df, plant_type_df,
                                      on='plant_type_id', how='outer')
    merged_plant_with_type_with_botanist = pd.merge(
        merged_plant_with_type, botanist_df, on='botanist_id', how='outer')
    plant_information = pd.merge(
        merged_plant_with_type_with_botanist, origin_df, on='location_id', how='outer').sort_values("plant_id")
    return plant_information


def get_measurements(conn) -> pd.DataFrame:
    '''Returns all measurements from the measurement table taken within 24 hours'''
    query = "SELECT * FROM measurement;"
    measurement = pd.read_sql(query, conn)
    measurement = measurement[measurement['measurement_time']
                              > datetime.now() - timedelta(hours=24)]
    return measurement


def create_botanist_pie_chart(df):
    g_df = df.groupby("botanist_name").agg(
        {"plant_id": "count"}).reset_index()

    g_df.rename(columns={"botanist_name": "Botanist",
                "plant_id": "Number of plants"}, inplace=True)

    pie = alt.Chart(g_df).mark_arc(innerRadius=75).encode(
        theta=alt.Theta(field="Number of plants", type="quantitative", stack=True, scale=alt.Scale(
            type="linear", rangeMax=1.5708, rangeMin=-1.5708)),
        color=alt.Color(field="Botanist", type="nominal",
                        scale=alt.Scale(scheme="greens"))
    )
    text = pie.mark_text(radius=110, fontSize=25, fill="black", baseline="middle", align="center").encode(
        text=alt.Text("Number of plants:Q")
    )
    chart = (pie + text).properties(
        title="Plant Distribution by Botanist"
    )

    return chart


def create_single_plant_chart(merged_df, plant_id):
    single_plant_measurement = merged_df[merged_df['plant_id'] == plant_id].sort_values(
        "measurement_time").reset_index()

    plant_name = single_plant_measurement['plant_name'].iloc[0]

    base = alt.Chart(single_plant_measurement).encode(
        alt.X('measurement_time:T').title(None),
    ).properties(width=20)

    temperature_line = base.mark_line(stroke='#e83d17', interpolate='monotone').encode(
        alt.Y('temperature').axis(
            title='Avg. Temperature (°C)', titleColor='#e83d17')
    )

    moisture_line = base.mark_line(stroke='#5276A7', interpolate='monotone').encode(
        alt.Y('moisture').axis(
            title='Moisture Content (%)', titleColor='#5276A7')
    )

    chart = alt.layer(temperature_line, moisture_line).resolve_scale(
        y='independent'
    ).properties(title=f"Temperature and moisture content of the {plant_name} over the last 24 hours")

    return chart, plant_name


def streamlit(pie_chart, merged_df):
    '''Execute the streamlit code'''
    st.set_page_config(
        page_title="Botanist Dashboard", layout="wide")

    st.markdown(
        """
    <style>
        body {
            background-color: #e8daba;
            color: #000000;
        }
        .stApp {
            background-color: #e8daba;
        }
        .stSidebar {
            background-color: #94ce81;
        }
    </style>
    """,
        unsafe_allow_html=True
    )

    st.title(
        ":seedling: :green[Botanist Dashboard] :seedling:")
    st.header(
        "_Liverpool Museum of Natural History_")
    st.subheader("Summary Statistics")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.altair_chart(pie_chart)

    with col2:
        yesterday_temperature_mean, yesterday_moisture_mean = display_reading_change(
            merged_df)
        temperature_mean = merged_df['temperature'].mean()
        moisture_mean = merged_df['moisture'].mean()
        temperature_difference_string = f"{(temperature_mean - yesterday_temperature_mean).round(2)}°C since yesterday"
        moisture_difference_string = f"{(moisture_mean - yesterday_moisture_mean).round(2)}% since yesterday"
        # st.subheader(
        #     f"Avg. Temperature: {temperature_mean.round(2)}°C")
        st.metric(label="Avg. Temperature", value=f"{temperature_mean.round(2)}°C",
                  delta=temperature_difference_string)
        # st.subheader(
        #     f"# Avg. Moisture: {moisture_mean.round(2)}%")
        st.metric(label="# Avg. Moisture:", value=f"{moisture_mean.round(2)}%",
                  delta=moisture_difference_string)

    with col3:
        st.write("### Title")

    st.subheader("Short-Term Database Insights")
    chosen_plant_id = int(st.selectbox(
        "Which plant would you like to analyse? Choose a plant ID:",
        (merged_df['plant_id'].unique()))
    )
    plant_chart, plant_name = create_single_plant_chart(
        merged_df, chosen_plant_id)

    st.write(f"You have selected the {plant_name}: ID {chosen_plant_id}")

    st.altair_chart(plant_chart)


def display_reading_change(merged_df):
    """Display the difference between readings from today and all time"""
    not_today_df = merged_df[merged_df['measurement_time'].dt.day !=
                             datetime.now().day]
    temperature_mean = not_today_df['temperature'].mean()
    moisture_mean = not_today_df['moisture'].mean()
    return temperature_mean, moisture_mean


if __name__ == "__main__":
    load_dotenv()

    conn = get_conn()
    plant_df = get_plant_information(conn)
    print(plant_df.head())
    measurement_df = get_measurements(conn)
    merged_df = pd.merge(plant_df, measurement_df, on='plant_id', how='outer')
    botanist_pie_chart = create_botanist_pie_chart(plant_df)
    streamlit(botanist_pie_chart, merged_df)
