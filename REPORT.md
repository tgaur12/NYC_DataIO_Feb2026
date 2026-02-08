## Introduction

This report provides a detailed explanation of the data preparation, feature selection, and analytical decisions used in the NYC Housing Price Analysis project. It expands on the methodology and reasoning behind the exploratory analysis and complements the high-level summary presented in the README.

## Data Loading and Access
The dataset is loaded using Pandas:
```python
df = pd.read_csv(file_path, encoding="latin1", engine="python")
```
- The dataset contains special characters that may cause Unicode errors. Using latin1 ensures the CSV loads correctly.
- The Python engine is more flexible and can handle irregular CSV formatting better than the default C engine.

## Feature Selection
The dataset contains many columns, but only the most relevant variables were selected for this analysis. These variables were chosen because they directly support the project objective of studying price trends, size effects, and location effects.
The analysis focused on the following columns:


| Category             | Columns Used |
|---------------------|--------------|
| Location            | borough_y, latitude, longitude |
| Price               | sale_price |
| Size                | bldgarea, lotarea, resarea, comarea |
| Property Structure  | unitsres, unitstotal, numfloors |
| Age / Year          | yearbuilt, building_age |
| Property Type       | bldgclass, landuse |

## Why Other Columns Were Not Used

Some columns such as block, lot, or internal IDs were excluded because:
- they act as identifiers rather than meaningful predictors
- they do not provide interpretable insight for price trends
- they do not contribute significantly to dashboard-level analysis

The goal was to retain only variables that are meaningful for understanding pricing patterns.

## Data Cleaning and Preprocessing

- Missing values were handled based on the meaning of the column:

    - `resarea` and `comarea` missing values were replaced with `0` because missing area often indicates no reported residential/commercial space.
    - `numfloors` missing values were replaced with the mode (most common value).
    - `latitude` and `longitude` missing values were replaced with the most common coordinates to avoid removing too many records.

 ```python
    df["resarea"] = df["resarea"].fillna(0)
    df["comarea"] = df["comarea"].fillna(0)
    df["numfloors"] = df["numfloors"].fillna(df["numfloors"].mode()[0])
  ```
- Outlier Removal

     - NYC housing datasets often contain extreme values that can distort visualizations and analysis. To maintain realistic results, the dataset was filtered to remove   unrealistic observations:
          - Sale price limited to under $10 million
          - Building area limited to under 500,000 sq ft
          - Building age limited to under 200 years
            
     - This ensures the plots are not dominated by extreme or incorrect values.
 ```python
   df = df[(df["sale_price"] > 0) & (df["sale_price"] < 10_000_000)]
   df = df[(df["bldgarea"] > 0) & (df["bldgarea"] < 500_000)]
   df = df[(df["building_age"] >= 0) & (df["building_age"] < 200)]

 ```
## Feature Engineering: Price Per Square Foot

A new feature called price per square foot was created:

 ```python
   df["price_per_sqft"] = df["sale_price"] / df["bldgarea"]
 ```
Sale price alone is not enough to measure housing value because larger buildings naturally sell for more.
Price per square foot provides a better comparison of relative property value across boroughs.

## Data Visualizations & Key Insights

### 1️. Average Housing Price by Borough  
**Graph:** `avg_price_by_borough.png`  

This bar chart shows the average sale price** for each borough.

Key Insight:
- Manhattan (MN) has the highest average sale price.
- Brooklyn (BK) is the second most expensive.
- Bronx (BX) has the lowest average sale price.

This confirms that location is a major driver of housing price.

---

### 2️.Price by Building Type (Building Class)  
**Graph:** `bldgclass_prices.png`  

This bar chart compares average sale prices by building class code.

Why it matters:
- Different property types have different market demand and value.

Key Insight:
- Certain building classes (such as **elevator apartments** and **luxury categories**) show significantly higher average prices.

---

### 3️. Sale Price vs Building Age  
**Graph:** `building_age_vs_price.png`  

This bar plot shows the average sale price grouped by building age ranges (20-year bins).

Why it matters:
- Age can influence property price because newer buildings may have modern features.
- Older buildings may still sell high if they are located in premium boroughs.
- Binning age values makes trends easier to see compared to a scatter plot.

Key Insight:
- Building age alone does not strongly determine sale price.
- Some older buildings still show high average sale prices, likely due to high-demand locations such as Manhattan.
- Location and building class appear to have a stronger impact than building age.

---

### 4️. Correlation Heatmap (What Drives Sale Price?)  
**Graph:** `correlation_heatmap.png`  

This heatmap shows correlations between numerical features such as:
- building area  
- lot area  
- residential area  
- total units  
- residential units  
- number of floors  
- building age  

Key Insight:
- Sale price has weak correlation with most numerical variables.
- Many size-related features are strongly correlated with each other.

This suggests NYC pricing is influenced by multiple factors, not just size.

---

### 5️. NYC Housing Map (Price per Sq Ft by Location)  
**Graph:** `nyc_housing_map.png`  
**Interactive File:** `nyc_housing_map_interactive.html`  

This visualization maps properties using latitude and longitude:
- Color = price per square foot
- Darker points indicate higher price per sq ft

Key Insight:
- Manhattan has dense high-price clusters.
- Brooklyn also shows expensive clusters.
- Outer boroughs show more affordable pricing patterns.

---

### 6️. Best Value Boroughs ($/sq ft)  
**Graph:** `price_per_sqft.png`  

This bar chart compares boroughs based on average price per square foot.

Why price per sq ft is useful:
- Total sale price depends heavily on building size.
- Price per sq ft normalizes comparisons.

Key Insight:
- Staten Island and Queens tend to provide better value per square foot.
- Manhattan is the most expensive even after normalization.

---

### 7️.Price per Sq Ft Distribution by Borough (Boxplot)  
**Graph:** `price_per_sqft_boxplot.png`  

This boxplot shows distribution of price per square foot in each borough.

Why it matters:
Averages can be misleading. Boxplots show:
- median price  
- variability  
- outliers  

Key Insight:
- Manhattan has extreme outliers due to luxury properties.
- Brooklyn and Queens show wide distributions.
- Bronx has a lower median price per sq ft.

---

### 8️. Sale Price vs Building Area  
**Graph:** `price_vs_bldgarea.png`  

This bar plot shows the **average sale price** grouped by building area ranges (5,000 sq ft bins).

Why it matters:
- Building area is one of the strongest indicators of property value.
- Grouping into bins reduces noise and makes the overall trend easier to interpret.
- Helps identify whether larger properties consistently sell for higher prices.

Key Insight:
- Properties with larger building area generally have a higher average sale price.
- Smaller building sizes show high variation, meaning location and building type can still heavily impact price.
- The relationship is positive overall, but not perfectly linear due to neighborhood and property-type differences.


## Correlation Analysis

A correlation analysis was conducted to quantify the relationship between sale_price and numerical variables such as building area, lot area, and building age.
The results were saved in:

sale_price_correlation.csv

Correlation provides numeric evidence of which variables are most strongly related to housing prices.

## Limitations & Assumptions

- The analysis does not account for time-based effects such as inflation or market cycles.
- Neighborhood-level factors (zoning, school districts, transit access) were not included.
- Correlation analysis captures only linear relationships and does not imply causation.
- Outlier removal may exclude valid ultra-luxury properties, particularly in Manhattan.
- Price per square foot assumes uniform value across building area, which may not hold for mixed-use or luxury properties.

## Conclusion & Future Work

This analysis demonstrates that NYC housing prices are driven by a combination of location, property type, and size rather than any single numerical factor. The cleaned dataset and engineered features provide a strong foundation for interactive visualization and further modeling.

Potential next steps include:
- Neighborhood-level analysis and clustering
- Regression or machine learning models for price prediction
- Time-series analysis to study market trends
- Enhanced geospatial analysis using zoning or transit data
