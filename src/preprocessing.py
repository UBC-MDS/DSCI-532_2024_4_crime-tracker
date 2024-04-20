import os
import pandas as pd
from pyproj import Proj, transform, Transformer

crime_type_mapping = {
    "Break and Enter Commercial": "B&E Comm",
    "Break and Enter Residential/Other": "B&E Res/Other",
    "Mischief": "Mischief",
    # "Offence Against a Person": "Offence Person",
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
    # "Offence Person": "#AB63FA",  # purple
    "Other Theft": "#FFA15A",  # orange
    "Theft Vehicle": "#19D3F3",  # light blue
    "Theft Bicycle": "#FF6692",  # pink
    "Theft of Vehicle": "#B6E880",  # light green
    "Collision Fatal": "#FF97FF",  # magenta
    "Collision Injury": "#FECB52",  # yellow
}

east_van_areas = [
    "Kitsilano",
    "Marpole",
    "Oakridge",
    "Fairview",
    "South Cambie",
    "Kerrisdale",
    "Shaughnessy",
    "Musqueam",
    "Dunbar-Southlands",
    "Arbutus Ridge",
    "West Point Grey",
]


def convert_to_decimal_degrees(x_list, y_list):

    utm_zone = 10
    utm_crs = Proj(proj="utm", zone=utm_zone, ellps="WGS84")
    latlon_crs = Proj(proj="latlong", datum="WGS84")
    lon, lat = transform(utm_crs, latlon_crs, x_list, y_list)

    return lat, lon


def preprocessor(data_path, save_path="./data/processed"):

    crime_df = pd.read_csv(data_path)
    crime_df = crime_df[crime_df.NEIGHBOURHOOD.isin(east_van_areas)]
    crime_df = crime_df[crime_df.TYPE.isin(crime_type_mapping.keys())]
    X_list, Y_list = convert_to_decimal_degrees(crime_df["X"], crime_df["Y"])
    crime_df["X"] = X_list
    crime_df["Y"] = Y_list
    crime_df["TYPE_SHORT"] = crime_df["TYPE"].replace(crime_type_mapping)
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
    hourly_df["TYPE_SHORT"] = hourly_df["TYPE"].replace(crime_type_mapping)
    hourly_df["HOUR"] = hourly_df["DATE"].dt.strftime("%H")
    crime_df.to_parquet(os.path.join(save_path, "crimedata.parquet"))
    hourly_df.to_parquet(os.path.join(save_path, "crimedata_hourly.parquet"))


def load_data(data_path="./data/processed"):
    crime_df = pd.read_parquet(os.path.join(data_path, "crimedata.parquet"))
    hourly_df = pd.read_parquet(os.path.join(data_path, "crimedata_hourly.parquet"))
    return crime_df, hourly_df


if __name__ == "__main__":
    data_path = os.path.join("../data/raw", "crimedata_csv_2023.csv")
    preprocessor(data_path, save_path="../data/processed/")
