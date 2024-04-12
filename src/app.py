import dash_bootstrap_components as dbc
import dash_vega_components as dvc
import pandas as pd
from dash import Dash, dcc, html
import callbacks
from preprocessing import preprocessor

crime_df, hourly_df = preprocessor(
    pd.read_csv("data/processed/crimedata_processed.csv")
)

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server


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
        dbc.Row([html.H1("VANCOUVER CRIME TRACKER 2023"), html.Br()]),
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
                                                html.H3("Total Crime Count"),
                                                html.Br(),
                                                html.H2(crime_df.shape[0]),
                                            ]
                                        )
                                    ]
                                )
                            ]
                        ),
                        dbc.Row(
                            [
                                html.H2(
                                    [
                                        "Crime Type:",
                                        dcc.Dropdown(
                                            id="crime-type-dropdown",
                                            options=crime_type_options,
                                            value="All",  # Default value
                                            clearable=False,
                                            # multi=True,
                                        ),
                                    ]
                                )
                            ]
                        ),
                        dbc.Row(
                            [
                                html.H2(
                                    [
                                        "Neighbourhood:",
                                        dcc.Dropdown(
                                            id="neighbourhood-dropdown",
                                            options=neighbourhood_options,
                                            value="All",  # Default value
                                            clearable=False,
                                            # multi=True,
                                        ),
                                    ]
                                )
                            ]
                        ),
                        dbc.Row([html.H2([dcc.Graph(id="crime-type-bar-chat")])]),
                        dbc.Row(
                            [html.H2([dcc.Graph(id="crime-neighbourhood-bar-chat")])]
                        ),
                    ],
                    md=3,
                ),
                dbc.Col(
                    [
                        dbc.Row([html.H2([dcc.Graph(id="crime-map-chart")])]),
                        dbc.Row([html.H2([dcc.Graph(id="crime-line-chart")])]),
                    ],
                    md=9,
                ),
            ]
        ),
    ]
)


# Run the app/dashboard
if __name__ == "__main__":
    app.run(debug=False)
