import plotly.express as px

def map_plot(crime_df, selected_crime, selected_neighbourhood, color="RdYlGn_r"):
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
        color_continuous_scale=color,
        center={"lat": 49.26914, "lon": -123.11226},
        zoom=11,
        mapbox_style="carto-positron",
    )  # , hover_data=["price", "number_of_reviews", "host_name"])
    fig.update_layout(margin=dict(l=0, r=0, t=30, b=10))
    fig.update_layout(legend=None)
    fig.update_traces(showlegend=False)
    return fig