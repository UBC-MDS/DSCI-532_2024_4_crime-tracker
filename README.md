# Vancouver Crime Tracker 2023 Dashboard 🇨🇦🍁

Welcome to the Vancouver Crime Tracker 2023 Dashboard!

# About
This "Crime Tracker" dashboard, designed specifically for law enforcement administrators and policymakers in the Vancouver Police Department, provides a comprehensive analytical view of crime data in Vancouver for the year 2023. Users can explore crime patterns based on location, time, and crime categories through interactive visualization and filtering options that empowers informed decision-making for resource allocation, tackling crime reduction. This dashboard features spatial heatmaps, temporal distribution, and summary statistics, offering users valuable insights into crime hotspots, temporal trends and spatial trends across neighborhoods.

## Usage

Our dashboard are hosted on the Render platform, accessible [here](https://dsci-532-2024-4-crime-tracker.onrender.com/).

### Navigating the Dashboard:

- The top row displays four static summaries showing the total crime count and the top three crime types alongside their respective crime counts.
- Use the dropdown filters on the left side of the dashboard to select specific crime types and neighbourhoods of interest. These filters will update the interactive map and time series chart below it.
- Use the drop down filter on the upper right side of the dashboard to select specific crime type to view crime counts per neighbourhood in the bar chart underneath.
- Similarly, use the dropdown filter on the bottom right side of the dashboard to select a specific neighbourhood of interest to view crime counts per crime type in the bar chart below.

### Interacting with Visualizations:

- Hover over elements in the charts to view detailed statistics via tooltips.
- Drag the map to explore different areas by clicking and dragging.

### Feedback and Support:

- All feedback is welcomed! If you encounter any issues during your experience, please do not hesitate to reach out via opening a new issue in this repository.
- Any comments and suggestions for improvement can also be logged through the same method.
- To log a new issue, navigate to the `Issues` tab and select `New` on the upper right. Fill in the title and a brief description and then click `Submit new issue`.

## LINK TO GIF 
https://github.com/UBC-MDS/DSCI-532_2024_4_crime-tracker/blob/main/img/demo.gif

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

