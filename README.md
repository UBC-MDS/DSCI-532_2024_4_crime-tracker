# Vancouver Crime Tracker 2023 Dashboard 🇨🇦🍁

Welcome to the Vancouver Crime Tracker 2023 Dashboard!

[About](#about) | [Dashboard](#dashboard) | [Navigation](#navigating-the-dashboard) | [Feedback & Support](#feedback-and-support) | [Developer's Note](#developer-note) | [Contributing](#contributing-guidelines) | [License](#license)

## About

This "Crime Tracker" dashboard, designed specifically for law enforcement administrators and policymakers in the Vancouver Police Department, provides a comprehensive analytical view of crime data in Vancouver for the year 2023. Users can explore crime patterns based on location, time, and crime categories through interactive visualization and filtering options that empowers informed decision-making for resource allocation, tackling crime reduction. This dashboard features spatial heatmaps, temporal distribution, and summary statistic, offering users valuable insights into crime hotspots, temporal trends and spatial trends across neighborhoods. The dataset used comprised of eight specific crime types and eleven neighbourhoods. It can be found on [GeoDASH](https://geodash.vpd.ca/opendata/#).

## Dashboard

Our dashboard are hosted on the Render platform, accessible [here](https://dsci-532-2024-4-crime-tracker.onrender.com/).

### Navigating the Dashboard:

- Selected Crime Count Statistic: Located at the top of the left sidebar, this statistic reflects the total count of crimes in the selected neighborhood(s) and crime type(s).
- Neighborhood and Crime Type Filters: Utilize the multi-selection filters on the left sidebar to choose multiple neighborhoods and specific crime types of interest.
- Crime Count for Different Crimes: The bar chart at the top left of the dashboard displays the count of each crime type within the selected neighborhood(s), offering insights into the distribution of different types of crimes.
- Crime Count in Different Neighborhood: The bar chart at the bottom left illustrates the count of crimes across eleven different neighborhoods for the selected crime type(s), enabling comparison of crime frequency across neighborhoods.
- Geo-Location Map: Positioned on the top right, the map displays the exact geographic location of selected crimes. Tooltips provide additional information, including the neighborhood and specific crime type associated with each data point.
- Hourly Time Series: The line chart on the bottom right showcases the hourly time series, allowing examination of how crime incidents vary throughout the day.

### Interacting with Visualizations:

- Tooltip Information: Hover over elements in the charts to access detailed statistics via tooltips, providing additional insights into specific data points.
- Map Interaction: Explore different areas by clicking and dragging on the map to navigate and zoom in or out as needed.
- Download and Reset Options: Utilize the Plotly toolbar, available in every chart, to download the specific plot of interest in various formats for further analysis or sharing purposes.

![](https://github.com/UBC-MDS/DSCI-532_2024_4_crime-tracker/blob/main/img/demo.gif)

## Feedback and Support:

- All feedback is welcomed! If you encounter any issues during your experience, please do not hesitate to reach out via opening a new issue in this repository.
- Any comments and suggestions for improvement can also be logged through the same method.
- To log a new issue, navigate to the `Issues` tab and select `New` on the upper right. Fill in the title and a brief description and then click `Submit new issue`.

## Developer note:

In order to work on this dashboard locally, please run the instructions provided below.

1. Clone this GitHub repository using this command:
```bash
git clone https://github.com/UBC-MDS/DSCI-532_2024_4_crime-tracker.git
```

2. Run the following commands from the root directory of this project folder to create a virtual environment and activate it:
```bash
conda env create -f environment.yml
conda activate crimetracker
```

3. To run the dashboard locally, make two adjustments to the code in the `app.py` file located inside the `src` folder as follow:
- Comment out line 9 that says `server = app.server`
- Change the arguement for `app.run(debug=False)` to `app.run(debug=True)`
- Run the following command.
```bash
python src/app.py
```

## Contributing Guidelines
Please check out our contributing [guidelines](https://github.com/UBC-MDS/DSCI-532_2024_4_crime-tracker/blob/main/CONTRIBUTING.md) for more details. This project is released with a [Code of Conduct](https://github.com/UBC-MDS/DSCI-532_2024_4_crime-tracker/blob/main/CODE_OF_CONDUCT.md). By contirbuting to this project, you agree to abide by its terms.

## License
This project is licensed under the terms of the [MIT license](https://github.com/UBC-MDS/DSCI-532_2024_4_crime-tracker/blob/main/LICENSE).