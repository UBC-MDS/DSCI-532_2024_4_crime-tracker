import dash_bootstrap_components as dbc
import dash_vega_components as dvc
import pandas as pd
from dash import Dash, dcc, html
from src.preprocessing import preprocessor

crime_df, hourly_df = preprocessor(
    pd.read_csv("data/processed/crimedata_processed.csv")
)

crime_type_options = [
    {"label": crime_type, "value": crime_type}
    for crime_type in crime_df["TYPE"].unique()
]

neighbourhood_options = [
    {"label": neighbourhood, "value": neighbourhood}
    for neighbourhood in crime_df["NEIGHBOURHOOD"].unique()
]

title = html.H3("CRIME TRACKER 2023",
                className = "title")

datacard = dbc.Card(
    [
        dbc.CardBody(
            [
                html.H5("Selected Crime Count"),
                html.H5(id="crime-count"),
            ],
            style={
                'text-align' : 'center',
                'font-weight' : 'bold'
            }
        )
    ], className= "card-total-crime"
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
            style={'color':'#324e7b',
                   'padding':1},
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
            style={'color':'#324e7b',
                   'padding':1},
        ),
    ]
)

crime_type_bar_chart = html.H2([dcc.Graph(id="crime-type-bar-chat")])

neighbourhood_bar_chart = html.H2([dcc.Graph(id="crime-neighbourhood-bar-chat")])

crime_map_chart = html.H2([dcc.Graph(id="crime-map-chart")])

crime_line_chart = html.H2([dcc.Graph(id="crime-line-chart")])

sidebar = dbc.Col([
    title,
    html.Br(),
    datacard,
    html.Br(),
    neighbourhood_dropdown,
    html.Br() ,
    crime_type_dropdown,
    html.Br(),
    html.P(
        "This dashboard designed specifically for law enforcement administrators and policymakers in the Vancouver Police Department.",  # Description text
        className='text-muted',
        style={'margin-bottom': '0px', 'padding-bottom': '0px'}),
    html.Br(),
    html.Div([
        html.P("Contributors: @Thomas, @Mo, @Sharon, @Waleed"),
        html.P(html.A(href="https://github.com/UBC-MDS/DSCI-532_2024_4_crime-tracker",
                      target="_blank",
                      children=html.Img(src="https://upload.wikimedia.org/wikipedia/commons/9/91/Octicons-mark-github.svg",
                      style={'width': '40px', 'height': '40px', 'padding': '5px'}))
        )
    ])
    ],
    md=2, className="sidebar"
)
