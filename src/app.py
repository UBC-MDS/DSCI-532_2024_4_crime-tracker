import dash_bootstrap_components as dbc
#import dash_vega_components as dvc
# from vega_datasets import data
import pandas as pd
from dash import Dash, dcc, callback, Output, Input, html
import altair as alt

# Initiatlize the app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

# crime_data = pd.read_csv("../data/crimedata_processed.csv")

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
            ]),
            dbc.Row([
            ]),
        ], md=3
        ),
        dbc.Col([
            # Map chart plot
        ], md=3
        ),
        dbc.Col([
            dbc.Row([
                # Line chart plot
            ]),
            dbc.Row([
                dbc.Col([
                    # Pie chart plot
                ]),
                dbc.Col([
                    # Stacked bar chart plot
                ]),
            ]),
        ], md=6
        )
    ])
])




app.run_server(host='127.0.0.1', port=8050, debug=True)
# Run the app/dashboard
if __name__ == '__main__':
    app.run(debug=False)

