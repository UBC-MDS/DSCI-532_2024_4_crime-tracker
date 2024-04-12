import pandas as pd
from dash import callback, Output, Input
import plotly.express as px
from src.preprocessing import preprocessor, color_mapping

crime_df, hourly_df = preprocessor(
    pd.read_csv("data/processed/crimedata_processed.csv")
)


@callback(
    Output("crime-line-chart", "figure"),
    [Input("crime-type-dropdown", "value"), Input("neighbourhood-dropdown", "value")],
)
def update_line_chart(selected_crime, selected_neighbourhood):

    filtered_df = hourly_df[(hourly_df["TYPE"].isin(selected_crime))]

    filtered_df = filtered_df[
        (filtered_df["NEIGHBOURHOOD"].isin(selected_neighbourhood))
    ]
    if len(selected_crime) > 1:
        combined_color = "#636EFA"
    else:
        combined_color = color_mapping[selected_crime[0]]

    filtered_df = (
        filtered_df.groupby("HOUR").agg({"TYPE": "first", "COUNT": "sum"}).reset_index()
    )
    fig = px.line(
        filtered_df,
        x="HOUR",
        y="COUNT",
        title=f"Hourly Counts",
        labels={"HOUR": "Time [Hour]", "COUNT": "Crime Count"},
        color_discrete_sequence=[combined_color],
    )
    fig.update_traces(mode="lines+markers")
    return fig


@callback(
    Output("crime-map-chart", "figure"),
    [Input("crime-type-dropdown", "value"), Input("neighbourhood-dropdown", "value")],
)
def update_map_chart(selected_crime, selected_neighbourhood):

    filtered_df = crime_df[(crime_df["TYPE"].isin(selected_crime))]

    filtered_df = filtered_df[
        (filtered_df["NEIGHBOURHOOD"].isin(selected_neighbourhood))
    ]

    fig = px.scatter_mapbox(
        filtered_df.dropna(subset=["NEIGHBOURHOOD", "TYPE"]),
        lat="X",
        lon="Y",
        color="TYPE",
        title=f"Crime Location",
        color_discrete_map=color_mapping,
        center={"lat": 49.26914, "lon": -123.11226},
        zoom=11,
        mapbox_style="carto-positron",
    )  # , hover_data=["price", "number_of_reviews", "host_name"])
    fig.update_layout(margin=dict(l=0, r=0, t=30, b=10))
    fig.update_layout(legend=None)
    fig.update_traces(showlegend=False)
    return fig


@callback(
    Output("crime-type-bar-chat", "figure"),
    Input("crime-type-dropdown", "value"),
)
def update_type_bar_chart(selected_crime):
    print(selected_crime)

    filtered_df = crime_df[(crime_df["TYPE"].isin(selected_crime))]

    if len(selected_crime) > 1:
        combined_color = "#636EFA"
    else:
        combined_color = color_mapping[selected_crime[0]]

    aggregated_data = (
        filtered_df.groupby(["NEIGHBOURHOOD"]).size().reset_index(name="COUNT")
    )
    aggregated_data = aggregated_data.sort_values("COUNT", ascending=False)
    fig = px.bar(
        aggregated_data,
        x="NEIGHBOURHOOD",
        y="COUNT",
        text="COUNT",
        labels={"COUNT": "Crime Count", "NEIGHBOURHOOD": "Neighbourhood"},
        color_discrete_sequence=[combined_color],
    )
    fig.update_layout(margin=dict(l=0, r=0, t=30, b=10))
    fig.update_layout(legend=None)
    fig.update_traces(showlegend=False)
    fig.update_xaxes(tickangle=90)
    return fig


@callback(
    Output("crime-neighbourhood-bar-chat", "figure"),
    Input("neighbourhood-dropdown", "value"),
)
def update_neighbourhood_bar_chart(selected_neighbourhood):

    filtered_df = crime_df[(crime_df["NEIGHBOURHOOD"].isin(selected_neighbourhood))]

    aggregated_data = filtered_df.groupby(["TYPE"]).size().reset_index(name="COUNT")
    aggregated_data = aggregated_data.sort_values("COUNT", ascending=False)
    fig = px.bar(
        aggregated_data,
        x="TYPE",
        y="COUNT",
        text="COUNT",
        labels={"COUNT": "Crime Count", "TYPE": "Crime Type"},
        color="TYPE",  # Now 'TYPE' will be used for discrete color mapping
        color_discrete_map=color_mapping,
    )
    fig.update_layout(margin=dict(l=0, r=0, t=30, b=10))
    fig.update_layout(legend=None)
    fig.update_traces(showlegend=False)
    fig.update_xaxes(tickangle=90)
    return fig
