import dash_bootstrap_components as dbc
import dash_vega_components as dvc
import pandas as pd
from dash import Dash, dcc, callback, Output, Input, html
import plotly.express as px

# Initiatlize the app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

crime_df = pd.read_csv("data/processed/crimedata_processed.csv")
crime_df['DATE'] = pd.to_datetime(crime_df[['YEAR','MONTH','DAY','HOUR','MINUTE']])
crime_df.set_index('DATE',inplace=True)

# Create dropdown options
crime_type_options = [{'label': crime_type, 'value': crime_type} for crime_type in crime_df['TYPE'].unique()]
crime_type_options.insert(0, {'label': 'All', 'value': 'All'})
neighbourhood_options = [{'label': neighbourhood, 'value': neighbourhood} for neighbourhood in crime_df['NEIGHBOURHOOD'].unique()]
neighbourhood_options.insert(0, {'label': 'All', 'value': 'All'})

app.layout = dbc.Container([
    dbc.Row([
        html.H1('VANCOUVER CRIME TRACKER 2023', style={'color': 'purple'}),
        html.Br(),
    ]),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H3('Total Crime Count', style={'color': 'blue'}),
                    html.Br(),
                    html.H2(crime_df.shape[0], style={'color': 'red'})
                ], style={'background-color': 'lightgrey'})
            ])
        ], md=3),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H3(crime_df['TYPE'].value_counts().index.tolist()[0], style={'color': 'blue'}),
                    html.Br(),
                    html.H2(crime_df['TYPE'].value_counts().nlargest(1)[0],style={'color': 'red'})
                ], style={'background-color': 'lightgrey'})    
            ])
        ], md=3),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H3(crime_df['TYPE'].value_counts().index.tolist()[1], style={'color': 'blue'}),
                    html.Br(),
                    html.H2(crime_df['TYPE'].value_counts().nlargest(2)[1],style={'color': 'red'})
                ], style={'background-color': 'lightgrey'})
            ])    
        ], md=3),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H3(crime_df['TYPE'].value_counts().index.tolist()[2], style={'color': 'blue'}),
                    html.Br(),
                    html.H2(crime_df['TYPE'].value_counts().nlargest(3)[2],style={'color': 'red'})
                ], style={'background-color': 'lightgrey'}),
            ])
        ], md=3)
    ]),
    dbc.Row([
        dbc.Col([
            dbc.Row([
                dbc.Col([
                    html.H5(["Crime Type:",
                                dcc.Dropdown(
                                id='crime-type-dropdown',
                                options=crime_type_options,
                                value='All',  # Default value
                                clearable=False,
                            )
                        ]),
                    ]),
                dbc.Col([
                    html.H5(["Neighbourhood:",
                                dcc.Dropdown(
                                    id='neighbourhood-dropdown',
                                    options=neighbourhood_options,
                                    value='All',  # Default value
                                    clearable=False,
                                )
                            ]),
                    ]),
                ]),
            dbc.Row([
                html.H2([dcc.Graph(id='crime-map-chart')
                ])
            ]),
            dbc.Row([
                html.Div([
                         dcc.Graph(id='crime-line-chart')
                    ])
                ]),
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
        ),
    ])
])

@app.callback(
    Output('crime-map-chart', 'figure'),
    [Input('crime-type-dropdown', 'value'),
     Input('neighbourhood-dropdown','value')]
)

def update_map_chart(selected_crime,selected_neighbourhood):

    if selected_neighbourhood == 'All':
        if selected_crime == 'All':
            filtered_df = crime_df
        else:
            filtered_df = crime_df[(crime_df['TYPE'] == selected_crime)]
    else:    
        if selected_crime == 'All':
            filtered_df = crime_df
            filtered_df = filtered_df[(filtered_df['NEIGHBOURHOOD'] == selected_neighbourhood)]
        else:
            filtered_df = crime_df[(crime_df['TYPE'] == selected_crime)]
            filtered_df = filtered_df[(filtered_df['NEIGHBOURHOOD'] == selected_neighbourhood)]

    fig = px.scatter_mapbox(filtered_df.dropna(subset=["NEIGHBOURHOOD", "TYPE"]), lat="X", lon="Y", color="TYPE",
                            title=f'Crime Location for {selected_crime} Crime in {selected_neighbourhood} Neighbourhood',
                            color_continuous_scale="RdYlGn_r",
                            center={"lat": 49.26914, "lon": -123.11226}, zoom=11,
                            mapbox_style="carto-positron")#, hover_data=["price", "number_of_reviews", "host_name"])
    fig.update_layout(margin=dict(l=0, r=0, t=30, b=10))
    fig.update_layout(legend=None)
    fig.update_traces(showlegend=False)
    return fig

# Run the app/dashboard
if __name__ == '__main__':
    app.run(debug=False)