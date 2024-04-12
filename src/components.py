import dash_bootstrap_components as dbc
import dash_vega_components as dvc
import pandas as pd
from dash import Dash, dcc, html
from preprocessing import preprocessor

crime_df, hourly_df = preprocessor(
    pd.read_csv("data/processed/crimedata_processed.csv")
)

crime_type_options = [
    {"label": crime_type, "value": crime_type}
    for crime_type in crime_df["TYPE"].unique()
]

# crime_type_options.insert(0, {"label": "All", "value": "All"})

neighbourhood_options = [
    {"label": neighbourhood, "value": neighbourhood}
    for neighbourhood in crime_df["NEIGHBOURHOOD"].unique()
]

# neighbourhood_options.insert(0, {"label": "All", "value": "All"})


title = html.H1("VANCOUVER CRIME TRACKER 2023")

datacard = dbc.Card(
    [
        dbc.CardBody(
            [
                html.H3("Total Crime Count"),
                html.Br(),
                html.H2(crime_df.shape[0]),
            ]
        )
    ]
)

crime_type_dropdown = html.H5(
    [
        "Crime Type:",
        dcc.Dropdown(
            id="crime-type-dropdown",
            options=crime_type_options,
            value=["Theft Vehicle"],  # Default value
            clearable=False,
            multi=True,
        ),
    ]
)

neighbourhood_dropdown = html.H5(
    [
        "Neighbourhood:",
        dcc.Dropdown(
            id="neighbourhood-dropdown",
            options=neighbourhood_options,
            value=["Kitsilano"],  # Default value
            clearable=False,
            multi=True,
        ),
    ]
)

crime_type_bar_chart = html.H2([dcc.Graph(id="crime-type-bar-chat")])

neighbourhood_bar_chart = html.H2([dcc.Graph(id="crime-neighbourhood-bar-chat")])

crime_map_chart = html.H2([dcc.Graph(id="crime-map-chart")])

crime_line_chart = html.H2([dcc.Graph(id="crime-line-chart")])
