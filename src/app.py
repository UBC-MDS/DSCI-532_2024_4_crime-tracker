from dash import Dash, html
import dash_bootstrap_components as dbc
import dash_vega_components as dvc
from dash import Dash

# the following is our files
import callbacks
from components import (
    title,
    datacard,
    crime_type_dropdown,
    neighbourhood_dropdown,
    crime_type_bar_chart,
    neighbourhood_bar_chart,
    crime_map_chart,
    crime_line_chart,
)

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server


app.layout = dbc.Container(
    [
        dbc.Row([title, html.Br()]),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Row([datacard]),
                        dbc.Row([crime_type_dropdown]),
                        dbc.Row([neighbourhood_dropdown]),
                        dbc.Row([crime_type_bar_chart]),
                        dbc.Row([neighbourhood_bar_chart]),
                    ],
                    md=3,
                ),
                dbc.Col(
                    [
                        dbc.Row([crime_map_chart]),
                        dbc.Row([crime_line_chart]),
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
