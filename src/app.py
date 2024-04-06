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
                    html.H5(["Crime Type:",
                                 dcc.Dropdown(
                                    id='crime-type-dropdown',
                                    options=crime_type_options,
                                    value='All',  # Default value
                                    clearable=False,
                                )]),
                ]),
                dbc.Col([
                    html.H5(["Neighbourhood:",
                            dcc.Dropdown(
                                id='neighbourhood-dropdown',
                                options=neighbourhood_options,
                                value='All',  # Default value
                                clearable=False,
                        )]),
                ]),
            ]),
            dbc.Row([
                html.H2(["Map Chart"
                ])
            ]),
            dbc.Row([
                html.Div([
                        dcc.Graph(id='crime-line-chart')
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

# Define callback to update line chart based on dropdown selection
@app.callback(
    Output('crime-line-chart', 'figure'),
    [Input('crime-type-dropdown', 'value'),
     Input('neighbourhood-dropdown','value')]
)
def update_line_chart(selected_crime,selected_neighbourhood):

    # Hourly data by Crime Type
    hourly_df = crime_df.groupby(['TYPE','NEIGHBOURHOOD']).resample('h').size().reset_index(name='COUNT')
    hourly_df['HOUR']=hourly_df['DATE'].dt.strftime('%H')

    if selected_crime == 'All':
        filtered_df = hourly_df
    else:
        filtered_df = hourly_df[(hourly_df['TYPE'] == selected_crime)]

    if selected_neighbourhood != 'All':
        filtered_df = filtered_df[(filtered_df['NEIGHBOURHOOD'] == selected_neighbourhood)]

    filtered_df = filtered_df.groupby('HOUR').agg({'TYPE': 'first','COUNT': 'sum'}).reset_index()
    fig = px.line(filtered_df, x='HOUR', y='COUNT', title=f'Hourly Counts for {selected_crime} Crime in {selected_neighbourhood} Neighbourhood',
                    labels={'HOUR': 'Time [Hour]', 'COUNT': 'Crime Count'})
    fig.update_traces(mode='lines+markers', line=dict(color='blue'))
    return fig

# Run the app/dashboard
if __name__ == '__main__':
    app.run(debug=False)

