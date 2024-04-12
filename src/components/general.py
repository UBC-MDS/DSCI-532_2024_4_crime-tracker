import plotly.express as px
import pandas as pd

crime_df = pd.read_csv("data/processed/crimedata_processed.csv")
crime_df["DATE"] = pd.to_datetime(crime_df[["YEAR", "MONTH", "DAY", "HOUR", "MINUTE"]])
crime_df.set_index("DATE", inplace=True)
hourly_df = (
    crime_df.groupby(["TYPE", "NEIGHBOURHOOD"])
    .resample("h")
    .size()
    .reset_index(name="COUNT")
)
hourly_df["HOUR"] = hourly_df["DATE"].dt.strftime("%H")

def update_line_chart(selected_crime, selected_neighbourhood):
    if selected_crime == "All":
        filtered_df = hourly_df
    else:
        filtered_df = hourly_df[(hourly_df["TYPE"] == selected_crime)]

    if selected_neighbourhood != "All":
        filtered_df = filtered_df[
            (filtered_df["NEIGHBOURHOOD"] == selected_neighbourhood)
        ]

    filtered_df = (
        filtered_df.groupby("HOUR").agg({"TYPE": "first", "COUNT": "sum"}).reset_index()
    )
    fig = px.line(
        filtered_df,
        x="HOUR",
        y="COUNT",
        title=f"Hourly Counts for {selected_crime} Crime in {selected_neighbourhood} Neighbourhood",
        labels={"HOUR": "Time [Hour]", "COUNT": "Crime Count"},
    )
    fig.update_traces(mode="lines+markers", line=dict(color="blue"))
    return fig


def update_map_chart(selected_crime, selected_neighbourhood):

    if selected_neighbourhood == "All":
        if selected_crime == "All":
            filtered_df = crime_df
        else:
            filtered_df = crime_df[(crime_df["TYPE"] == selected_crime)]
    else:
        if selected_crime == "All":
            filtered_df = crime_df
            filtered_df = filtered_df[
                (filtered_df["NEIGHBOURHOOD"] == selected_neighbourhood)
            ]
        else:
            filtered_df = crime_df[(crime_df["TYPE"] == selected_crime)]
            filtered_df = filtered_df[
                (filtered_df["NEIGHBOURHOOD"] == selected_neighbourhood)
            ]

    fig = px.scatter_mapbox(
        filtered_df.dropna(subset=["NEIGHBOURHOOD", "TYPE"]),
        lat="X",
        lon="Y",
        color="TYPE",
        title=f"Crime Location for {selected_crime} Crime in {selected_neighbourhood} Neighbourhood",
        color_continuous_scale="RdYlGn_r",
        center={"lat": 49.26914, "lon": -123.11226},
        zoom=11,
        mapbox_style="carto-positron",
    )  # , hover_data=["price", "number_of_reviews", "host_name"])
    fig.update_layout(margin=dict(l=0, r=0, t=30, b=10))
    fig.update_layout(legend=None)
    fig.update_traces(showlegend=False)
    return fig

def update_type_bar_chart(crime_type):
    if crime_type == "All":
        filtered_df = crime_df
    else:
        filtered_df = crime_df[(crime_df["TYPE"] == crime_type)]

    aggregated_data = (
        filtered_df.groupby(["NEIGHBOURHOOD"]).size().reset_index(name="COUNT")
    )
    fig = px.bar(
        aggregated_data,
        x="NEIGHBOURHOOD",
        y="COUNT",
        text="COUNT",
        labels={"COUNT": "Crime Count", "NEIGHBOURHOOD": "Neighbourhood"},
    )
    fig.update_layout(margin=dict(l=0, r=0, t=30, b=10))
    fig.update_layout(legend=None)
    fig.update_traces(showlegend=False)
    fig.update_xaxes(tickangle=90)
    return fig

def update_neighbourhood_bar_chart(crime_neighbourhood):
    if crime_neighbourhood == "All":
        filtered_df = crime_df
    else:
        filtered_df = crime_df[(crime_df["NEIGHBOURHOOD"] == crime_neighbourhood)]

    aggregated_data = filtered_df.groupby(["TYPE"]).size().reset_index(name="COUNT")
    fig = px.bar(
        aggregated_data,
        x="TYPE",
        y="COUNT",
        text="COUNT",
        labels={"COUNT": "Crime Count", "TYPE": "Crime Type"},
    )
    fig.update_layout(margin=dict(l=0, r=0, t=30, b=10))
    fig.update_layout(legend=None)
    fig.update_traces(showlegend=False)
    fig.update_xaxes(tickangle=90)
    return fig
