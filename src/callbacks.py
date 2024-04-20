import pandas as pd
from dash import callback, Output, Input
import plotly.express as px
from src.preprocessing import load_data, color_mapping
import joblib

crime_df, hourly_df = load_data()

memory = joblib.Memory("tmp", verbose=0)


@callback(
    Output("crime-line-chart", "figure"),
    [Input("crime-type-dropdown", "value"), Input("neighbourhood-dropdown", "value")],
)
@memory.cache()
def update_line_chart(selected_crime, selected_neighbourhood):

    filtered_df = hourly_df[(hourly_df["TYPE_SHORT"].isin(selected_crime))]

    filtered_df = filtered_df[
        (filtered_df["NEIGHBOURHOOD"].isin(selected_neighbourhood))
    ]
    if len(selected_crime) > 1:
        combined_color = "#636EFA"
    else:
        combined_color = color_mapping[selected_crime[0]]

    filtered_df = (
        filtered_df.groupby("HOUR")
        .agg({"TYPE_SHORT": "first", "COUNT": "sum"})
        .reset_index()
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
    fig.update_layout(title=dict(font=dict(color="#cb212c", size=16)))
    fig.update_layout(margin=dict(l=0, r=0, t=30, b=10))
    return fig


@callback(
    Output("crime-map-chart", "figure"),
    [Input("crime-type-dropdown", "value"), Input("neighbourhood-dropdown", "value")],
)
@memory.cache()
def update_map_chart(selected_crime, selected_neighbourhood):

    filtered_df = crime_df[(crime_df["TYPE_SHORT"].isin(selected_crime))]

    filtered_df = filtered_df[
        (filtered_df["NEIGHBOURHOOD"].isin(selected_neighbourhood))
    ]

    fig = px.scatter_mapbox(
        filtered_df.dropna(subset=["NEIGHBOURHOOD", "TYPE_SHORT"]),
        lat="X",
        lon="Y",
        color="TYPE_SHORT",
        title=f"Crime Location",
        color_discrete_map=color_mapping,
        center={"lat": 49.244936, "lon": -123.170190},
        zoom=11,
        mapbox_style="carto-positron",
    )  # , hover_data=["price", "number_of_reviews", "host_name"])
    fig.update_layout(title=dict(font=dict(color="#cb212c", size=16)))
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

    filtered_df = crime_df[(crime_df["TYPE_SHORT"].isin(selected_crime))]

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
        title=f"Crime Count in Different Neighbourhood",
        color_discrete_sequence=[combined_color],
    )
    fig.update_layout(margin=dict(l=0, r=0, t=30, b=10))
    fig.update_layout(title=dict(font=dict(color="#cb212c", size=16)))
    fig.update_layout(legend=None)
    fig.update_traces(showlegend=False)
    fig.update_xaxes(tickangle=45)
    return fig


@callback(
    Output("crime-neighbourhood-bar-chat", "figure"),
    Input("neighbourhood-dropdown", "value"),
)
def update_neighbourhood_bar_chart(selected_neighbourhood):

    filtered_df = crime_df[(crime_df["NEIGHBOURHOOD"].isin(selected_neighbourhood))]

    aggregated_data = (
        filtered_df.groupby(["TYPE_SHORT"]).size().reset_index(name="COUNT")
    )
    aggregated_data = aggregated_data.sort_values("COUNT", ascending=False)
    fig = px.bar(
        aggregated_data,
        x="TYPE_SHORT",
        y="COUNT",
        text="COUNT",
        labels={"COUNT": "Crime Count", "TYPE_SHORT": "Crime Type"},
        color="TYPE_SHORT",  # Now 'TYPE' will be used for discrete color mapping
        title=f"Crime Count for Different Crimes",
        color_discrete_map=color_mapping,
    )
    fig.update_layout(margin=dict(l=0, r=0, t=30, b=10))
    fig.update_layout(title=dict(font=dict(color="#cb212c", size=16)))
    fig.update_layout(legend=None)
    fig.update_traces(showlegend=False)
    fig.update_xaxes(tickangle=45)
    return fig


@callback(
    Output("crime-count", "children"),
    [Input("crime-type-dropdown", "value"), Input("neighbourhood-dropdown", "value")],
)
def update_crime_count_card(selected_crime, selected_neighbourhood):
    total_count = len(crime_df)
    filtered_df = crime_df[
        (crime_df["TYPE_SHORT"].isin(selected_crime))
        & (crime_df["NEIGHBOURHOOD"].isin(selected_neighbourhood))
    ]
    count = len(filtered_df)

    return f"{count} out of {total_count}"
