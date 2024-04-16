from dash import Dash, html
import dash_bootstrap_components as dbc
import dash_vega_components as dvc
from dash import Dash

# the following is our files
import src.callbacks
from src.components import (
    crime_type_bar_chart,
    neighbourhood_bar_chart,
    crime_map_chart,
    crime_line_chart,
    sidebar
)

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server


app.layout = dbc.Container([
    dbc.Row([
        sidebar,
        dbc.Col([
            dbc.Row([neighbourhood_bar_chart]),
            dbc.Row([crime_type_bar_chart]),
        ],
        md=4,
        ),
        dbc.Col([
            dbc.Row([crime_map_chart]),
            dbc.Row([crime_line_chart]),
        ],
        md=5,
        ),
    ])
],fluid = True)

app.run_server(host='127.0.0.1', port=8054, debug=True)
# Run the app/dashboard
if __name__ == "__main__":
    app.run(debug=False)
