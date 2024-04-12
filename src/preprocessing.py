import pandas as pd

crime_type_mapping = {
    "Break and Enter Commercial": "B&E Comm",
    "Break and Enter Residential/Other": "B&E Res/Other",
    "Mischief": "Mischief",
    "Offence Against a Person": "Offence Person",
    "Other Theft": "Other Theft",
    "Theft from Vehicle": "Theft Vehicle",
    "Theft of Bicycle": "Theft Bicycle",
    "Theft of Vehicle": "Theft Vehicle",
    "Vehicle Collision or Pedestrian Struck (with Fatality)": "Collision Fatal",
    "Vehicle Collision or Pedestrian Struck (with Injury)": "Collision Injury",
}

color_mapping = {
    "B&E Comm": "#6C6EBA",  # dark purple
    "B&E Res/Other": "#EF553B",  # red-orange
    "Mischief": "#00CC96",  # teal
    "Offence Person": "#AB63FA",  # purple
    "Other Theft": "#FFA15A",  # orange
    "Theft Vehicle": "#19D3F3",  # light blue
    "Theft Bicycle": "#FF6692",  # pink
    "Theft of Vehicle": "#B6E880",  # light green
    "Collision Fatal": "#FF97FF",  # magenta
    "Collision Injury": "#FECB52",  # yellow
}


def preprocessor(crime_df):

    crime_df = pd.read_csv("data/processed/crimedata_processed.csv")
    crime_df["TYPE"] = crime_df["TYPE"].replace(crime_type_mapping)
    crime_df["DATE"] = pd.to_datetime(
        crime_df[["YEAR", "MONTH", "DAY", "HOUR", "MINUTE"]]
    )
    crime_df.set_index("DATE", inplace=True)
    hourly_df = (
        crime_df.groupby(["TYPE", "NEIGHBOURHOOD"])
        .resample("h")
        .size()
        .reset_index(name="COUNT")
    )
    hourly_df["HOUR"] = hourly_df["DATE"].dt.strftime("%H")
    return crime_df, hourly_df
