## NYC Housing Price Analysis (Data I/O Challenge)

**Interactive Dashboard — explore NYC housing prices by borough, size, and value:**
https://ny-property-pulse.lovable.app/

## Project Overview

This project analyzes New York City housing sales data to identify major trends and factors affecting housing prices across boroughs. Using exploratory data analysis (EDA), correlation analysis, and feature engineering, this project highlights how location, property size, building age, and building type influence sale prices.
The project was developed as part of the Data I/O Challenge, where participants were expected to clean the dataset, generate meaningful insights, and prepare the data for an interactive dashboard.

## Objectives

The main objectives of this project are:
- Analyze trends in housing prices across NYC boroughs.
- Identify key factors influencing housing sale prices (building area, lot area, building type, age, and borough).
- Visualize findings using charts and summary tables.
- Create a beginner-friendly foundation for an interactive dashboard.

## Dataset Information

The dataset used in this project is stored locally in the repository as: nyc_housing_base.csv

This file contains NYC property sales records and includes important features such as:

- sale price
- borough location
- property size and area
- building type classification
- coordinates (latitude and longitude)
- building age and construction year

## Repository Structure

The repository is organized as follows:

```text
NYC_DataIO_Feb2026/
│── nyc_housing_base.csv
│── README.md
│── nyc_housing_important_columns.csv
│── sale_price_correlation.csv
│
├── notebook/
│   └── nyc_housing_analysis.py
│
└── images/
    ├── avg_price_by_borough.png
    ├── price_vs_bldgarea.png
    ├── building_age_vs_price.png
    ├── price_per_sqft.png
    └── bldgclass_prices.png
```
## Technologies and Libraries Used

This project was implemented using Python and the following libraries:

- Pandas – data cleaning, transformation, and aggregation
- Matplotlib – visualization and plotting
- Seaborn – statistical plots and chart styling
- OS module – file handling and path validation

## How to Run the project

Step 1: Install Required Libraries
Make sure you have Python installed, then install the dependencies:

```bash
pip install pandas numpy matplotlib seaborn plotly
pip install --upgrade kaleido
```

Step 2: Clone the git repository
```bash
git clone https://github.com/tgaur12/NYC_DataIO_Feb2026.git
```

Step 3: Run the Analysis Script

Navigate to the notebook folder and run:

```bash
python nyc_housing_analysis.py

```
The script will:
- load nyc_housing_base.csv
- clean and filter the dataset
- remove extreme outliers
- generate visualizations and save them in the images/ folder
- generate cleaned output CSV files for dashboard use

## Output Files Generated

This project produces the following output files and visualizations:

**Static Graphs**
- `avg_price_by_borough.png`  
- `bldgclass_prices.png`  
- `building_age_vs_price.png`  
- `correlation_heatmap.png`  
- `price_per_sqft.png`  
- `price_per_sqft_boxplot.png`  
- `price_vs_bldgarea.png`  
- `nyc_housing_map.png`  

**Interactive Dashboard / Map**
- `nyc_housing_map_interactive.html`  

## Key Visual Insights
- Manhattan has the highest average sale price and price per square foot
- Brooklyn follows with strong high-price clusters
- Staten Island and Queens provide better value per square foot
- Building size increases sale price, but location and building class have stronger influence
- Numerical correlations with sale price are generally weak, reinforcing that NYC housing prices are driven by multiple interacting factors.

## Conclusion

This project explored NYC housing sales data to understand what factors influence property prices across boroughs. Through cleaning, feature selection, and exploratory analysis, clear differences in pricing patterns were observed between boroughs, with Manhattan consistently showing the highest sale prices and price-per-square-foot values.
The analysis also showed that while building size impacts sale price, location and building class play an even stronger role in determining value. Additionally, the price-per-square-foot metric provided a more meaningful comparison across boroughs than raw sale price alone.
Overall, this project provides a structured dataset, useful insights, and visual outputs that can support further dashboard development and more advanced modeling in future work.

## Explore the Interactive Dashboard

All charts, maps, and visual insights are available here:  
https://ny-property-pulse.lovable.app/
