import plotly.express as px

def time_series_plot(df, selected_crime, selected_neighbourhood, color):
    if selected_crime == "All":
        filtered_df = df
    else:
        filtered_df = df[(df["TYPE"] == selected_crime)]

    if selected_neighbourhood != "All":
        filtered_df = filtered_df[
            (filtered_df["NEIGHBOURHOOD"] == selected_neighbourhood)
        ]

    filtered_df = (
        filtered_df.groupby("HOUR").agg({"TYPE": "first", "COUNT": "sum"}).reset_index()
    )
    fig = px.line(
        filtered_df,
        x="HOUR",
        y="COUNT",
        title=f"Hourly Counts for {selected_crime} Crime in {selected_neighbourhood} Neighbourhood",
        labels={"HOUR": "Time [Hour]", "COUNT": "Crime Count"},
    )
    fig.update_traces(mode="lines+markers", line=dict(color=color))
    return fig