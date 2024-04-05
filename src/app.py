import dash_bootstrap_components as dbc
import dash_vega_components as dvc
import pandas as pd
from dash import Dash, dcc, callback, Output, Input, html
import plotly.express as px


# Initiatlize the app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

crime_data = pd.read_csv("data/processed/crimedata_processed.csv")

app.layout = dbc.Container([
    dbc.Row([
        html.H1('VANCOUVER CRIME TRACKER 2023'),
        html.Br(),
    ]),
    dbc.Row([
        dbc.Col([
            html.H1('Total Crime Count'),
        html.Br(),
        ], md=3),
        dbc.Col([
            html.H1('Top 1 Crime Type & Count'),
        html.Br(),
        ], md=3),
        dbc.Col([
            html.H1('Top 2 Crime Type & Count'),
        html.Br(),
        ], md=3),
        dbc.Col([
            html.H1('Top 3 Crime Type & Count'),
        html.Br(),
        ], md=3)
    ]),
    dbc.Row([
        dbc.Col([
            dbc.Row([
                dbc.Col([
                    html.H3(["Crime Type Filter"
                    ])
                ]),
                dbc.Col([
                    html.H3(["Neighborhood Filter"
                    ])
                ]),
            ]),
            dbc.Row([
                html.H2(["Map Chart"
                ])
            ]),
            dbc.Row([
                html.H2(["Time Series Chart"
                ])
            ])
        ], md=9
        ),
        dbc.Col([
            dbc.Row([
                html.H3('Crime Count per Crime Type in {Neighborhood}')
            ]),
            dbc.Row([
                html.H3('Bar Chart')
            ]),
            dbc.Row([
                html.H3('Crime Count per Neighborhood for {CrimeType}')
            ]),
            dbc.Row([
                html.H3('Bar Chart')
            ])
        ],md=3
        )
    ])
])

# Run the app/dashboard
if __name__ == '__main__':
    app.run(debug=False)

