import dash_bootstrap_components as dbc
import dash_vega_components as dvc
import pandas as pd
from dash import Dash, dcc, callback, Output, Input, html
import plotly.express as px

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server
crime_type_mapping = {
    "Break and Enter Commercial": "B&E Comm",
    "Break and Enter Residential/Other": "B&E Res/Other",
    "Mischief": "Mischief",
    "Offence Against a Person": "Offence Person",
    "Other Theft": "Other Theft",
    "Theft from Vehicle": "Theft Vehicle",
    "Theft of Bicycle": "Theft Bicycle",
    "Theft of Vehicle": "Theft Vehicle",
    "Vehicle Collision or Pedestrian Struck (with Fatality)": "Collision Fatal",
    "Vehicle Collision or Pedestrian Struck (with Injury)": "Collision Injury",
}


crime_df = pd.read_csv("data/processed/crimedata_processed.csv")
crime_df["TYPE"] = crime_df["TYPE"].replace(crime_type_mapping)
crime_df["DATE"] = pd.to_datetime(crime_df[["YEAR", "MONTH", "DAY", "HOUR", "MINUTE"]])
crime_df.set_index("DATE", inplace=True)
hourly_df = (
    crime_df.groupby(["TYPE", "NEIGHBOURHOOD"])
    .resample("h")
    .size()
    .reset_index(name="COUNT")
)
hourly_df["HOUR"] = hourly_df["DATE"].dt.strftime("%H")

crime_type_options = [
    {"label": crime_type, "value": crime_type}
    for crime_type in crime_df["TYPE"].unique()
]
crime_type_options.insert(0, {"label": "All", "value": "All"})
neighbourhood_options = [
    {"label": neighbourhood, "value": neighbourhood}
    for neighbourhood in crime_df["NEIGHBOURHOOD"].unique()
]
neighbourhood_options.insert(0, {"label": "All", "value": "All"})

app.layout = dbc.Container(
    [
        dbc.Row(
            [
                html.H1("VANCOUVER CRIME TRACKER 2023"),
                html.Br()
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Row(
                            [
                                dbc.Card(
                                    [
                                        dbc.CardBody(
                                            [
                                                html.H3(
                                                    "Total Crime Count"
                                                ),
                                                html.Br(),
                                                html.H2(
                                                    crime_df.shape[0]
                                                )
                                            ]
                                        )
                                    ]
                                )
                            ]
                        ),
                        dbc.Row(
                            [
                                html.H5(
                                    [
                                        "Crime Type:",
                                        dcc.Dropdown(
                                            id="crime-type-dropdown",
                                            options=crime_type_options,
                                            value="All",  # Default value
                                            clearable=False,
                                        ),
                                    ]
                                )
                            ]

                        ),
                        dbc.Row(
                            [
                                html.H5(
                                    [
                                        "Neighbourhood:",
                                        dcc.Dropdown(
                                            id="neighbourhood-dropdown",
                                            options=neighbourhood_options,
                                            value="All",  # Default value
                                            clearable=False,
                                        ),
                                    ]
                                )
                            ]
                        ),
                        dbc.Row(
                            [
                                html.H2(
                                    [
                                        dcc.Graph(id="crime-type-bar-chat"
                                        )
                                    ]
                                )
                            ]
                        ),
                        dbc.Row(
                            [
                                html.H2(
                                    [
                                        dcc.Graph(id="crime-neighbourhood-bar-chat"
                                        )
                                    ]
                                )
                            ]
                        )
                    ],
                    md=3
                ),
                dbc.Col(
                    [
                        dbc.Row(
                            [
                                html.H2(
                                    [
                                        dcc.Graph(id="crime-map-chart"
                                        )
                                    ]
                                )
                            ]
                        ),
                        dbc.Row(
                            [
                                html.H2(
                                    [
                                        dcc.Graph(id="crime-line-chart"
                                        )
                                    ]
                                )
                            ]
                        )

                    ],
                    md=9
                )

            ]
        )
    ]
)

@app.callback(
    Output("crime-line-chart", "figure"),
    [Input("crime-type-dropdown", "value"), Input("neighbourhood-dropdown", "value")],
)
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


@app.callback(
    Output("crime-map-chart", "figure"),
    [Input("crime-type-dropdown", "value"), Input("neighbourhood-dropdown", "value")],
)
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


@app.callback(
    Output("crime-type-bar-chat", "figure"),
    Input("crime-type-dropdown", "value"),
)
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


@app.callback(
    Output("crime-neighbourhood-bar-chat", "figure"),
    Input("neighbourhood-dropdown", "value"),
)
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


# Run the app/dashboard
if __name__ == "__main__":
    app.run(debug=False)
