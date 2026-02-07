import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px


#Accessing the dataset
file_path = "../nyc_housing_base.csv"

# Check if file exists
if not os.path.exists(file_path):
    raise FileNotFoundError(
        f"Dataset not found at {file_path}. "
        "Make sure nyc_housing_base.csv is in the project root directory."
    )

# read the CSV file into a pandas DataFrame
# encoding="latin1" -> handles unusual characters
# engine="python" -> parser able to handle messy file
df = pd.read_csv(file_path, encoding="latin1", engine="python")

# confirmation that loading worked
print("Dataset loaded successfully!")
print("Shape:", df.shape)       # (rows, columns)

# looks at first 5 rows -> shows in Jupyter
df.head()

# show column names and a quick summary of data types
print("\nColumns: \n", df.columns)
print("\nDataset Info:")
print(df.info())

# keep only the columns that are going to be used
useful_col = ["borough_y", "sale_price", "yearbuilt", "lotarea", "bldgarea", "resarea", "comarea",
              "unitsres", "unitstotal", "numfloors", "latitude", "longitude", "landuse", "bldgclass",
              "building_age"]

# drops everything but the useful columns
df = df[useful_col]

# check how many values are missing in each column
print(df.isnull().sum())

# handles missing data

# yearbuilt: missing -> unkown -> use 0 as placeholder
df["yearbuilt"] = df["yearbuilt"].fillna(0).astype('int64')

# same as yearbuilt for building_age
df["building_age"] = df["building_age"].fillna(0).astype('int64')

# area columns that have no info are assumed to be 0 feet
df["resarea"] = df["resarea"].fillna(0)
df["comarea"] = df["comarea"].fillna(0)

# numfloors: sets value to mode if missing
df["numfloors"] = df["numfloors"].fillna(df["numfloors"].mode()[0])

# coordinates: fills the missing values with the most common ones
df["latitude"] = df["latitude"].fillna(df["latitude"].mode()[0])
df["longitude"] = df["longitude"].fillna(df["longitude"].mode()[0])

# Remove crazy outliers (top 1% prices, negative areas, impossible ages)
df = df[(df["sale_price"] > 0) & (df["sale_price"] < 10_000_000)]
df = df[(df["bldgarea"] > 0) & (df["bldgarea"] < 500_000)]
df = df[(df["building_age"] >= 0) & (df["building_age"] < 200)]
df = df.dropna(subset=["latitude", "longitude"])  # Musthave location for map

print(f"After outlier removal: {len(df):,} rows (from {len(df)*1.5:+,} originally)")
# average price by borough

# group by borough and calculate mean sale price, sorted from lowest to highest
avg_price_borough = df.groupby("borough_y")["sale_price"].mean().sort_values()

print("Average price by borough:", avg_price_borough)


# Average price by borough

# create new figure window
plt.figure(figsize=(8,5))
sns.barplot(
    x=avg_price_borough.index,                  # borough names go on x-axis
    y=avg_price_borough.values / 1_000_000,     # in millions for readability
    hue=avg_price_borough.index,                # different color for each borough
    palette='coolwarm',                          # color scale
    legend=False                                # don't need legend
)
plt.title("Average Housing Price by Borough (Million $)")
plt.xlabel("Borough")
plt.ylabel("Average Housing Price ($)")
plt.xticks(rotation=45)                         # rotate names so they don't overlap
plt.tight_layout()                              # fix spacing automatically
plt.savefig("../images/avg_price_by_borough.png")
plt.show()


# plots price vs property size
# we use resarea and bldgarea to see if bigger buildings cost more
plt.figure(figsize=(8,5))
sns.scatterplot(x="bldgarea", y="sale_price", data=df, alpha=0.3)
plt.title("Sale Price vs Building Area")
plt.xlabel("Building Area (sq ft)")
plt.ylabel("Sale Price ($)")
# gets rid of extreme outliers
plt.ylim(0, 5_000_000)
plt.tight_layout()
plt.savefig("../images/price_vs_bldgarea.png")
plt.show()

# building age vs sale price
# newer buildings likely to be more expensive but location would impact this?
plt.figure(figsize=(8,5))
sns.scatterplot(x="building_age", y="sale_price", data=df, alpha=0.3)
plt.title("Sale Price vs Building Age")
plt.xlabel("Building Age (Years)")
plt.ylabel("Sale Price ($)")
plt.ylim(0, 5_000_000)
plt.tight_layout()
plt.savefig("../images/building_age_vs_price.png")
plt.show()

# top building classes
top_classes = df.groupby("bldgclass").agg({
    "sale_price": ["mean", "count"],
    "bldgarea": "mean"
}).round(0).sort_values(("sale_price", "mean"), ascending=False)

top_classes = top_classes[top_classes[("sale_price", "count")] >= 50]  # Reliable
print("Top 10 Building Classes by Avg Price:\n", top_classes.head(10))

top_classes.plot(kind="bar", y=("sale_price", "mean"), figsize=(12,6))
plt.title("Price by Building Type (A9=Co-ops, C0=Elevators)")
plt.ylabel("Avg Sale Price")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("../images/bldgclass_prices.png", dpi=300, bbox_inches='tight')
plt.show()

#creating a table
df_table = df[useful_col]
df_table.to_csv("../nyc_housing_important_columns.csv", index=False)
print("New CSV file created: nyc_housing_important_columns.csv")

corr_cols = ["sale_price", "bldgarea", "lotarea", "resarea", "comarea",
             "unitstotal", "unitsres", "numfloors", "building_age"]

#Correlation analysis
correlation_result = df[corr_cols].corr()["sale_price"].sort_values(ascending=False)
# Convert to dataframe
corr_df = correlation_result.reset_index()
corr_df.columns = ["feature", "correlation_with_sale_price"]

# Save as CSV
corr_df.to_csv("../sale_price_correlation.csv", index=False)

print("Correlation results saved as sale_price_correlation.csv")


# Create a new feature: price per square foot to better compare property values across different building sizes
df["price_per_sqft"] = df["sale_price"] / df["bldgarea"]

# Remove extreme outliers in price_per_sqft (top 1%) to avoid skewing analysis and plots
df = df[df["price_per_sqft"] < df["price_per_sqft"].quantile(0.99)]

# Price per sq foot
df["price_per_sqft"] = df["sale_price"] / df["bldgarea"].replace(0, 1)  # Avoid divide-by-zero
df["price_per_sqft"] = df["price_per_sqft"].clip(0, 5000)  # Cap insane $5000/sqft

pxsqft_borough = df.groupby("borough_y")["price_per_sqft"].mean().sort_values(ascending=False)
print("Price per Sq Ft by Borough:\n", pxsqft_borough.round(0))

plt.figure(figsize=(8,5))
sns.barplot(x=pxsqft_borough.index, y=pxsqft_borough.values, hue=pxsqft_borough.index, palette="coolwarm")
plt.title("Best Value Boroughs ($/sq ft)")
plt.ylabel("$ per Square Foot")
plt.savefig("../images/price_per_sqft.png", dpi=300, bbox_inches='tight')
plt.show()

plt.figure(figsize=(10, 6))
sns.boxplot(
    x="borough_y",
    y="price_per_sqft",
    data=df,
    hue="borough_y",
    palette="coolwarm",
    order=pxsqft_borough.index  # sort by highest to lowest
)
plt.title("Price per Square Foot Distribution by Borough\n(Spread shows variability within each borough)")
plt.ylabel("$ per Sq Ft")
plt.xlabel("Borough")
plt.ylim(0, df["price_per_sqft"].quantile(0.98))  # zoom to remove extreme tails
plt.tight_layout()
plt.savefig("../images/price_per_sqft_boxplot.png", dpi=300, bbox_inches='tight')
plt.show()

# Geographic View: Where in NYC is housing most/least affordable?

# drop any remaining invalid lat/lon
df_map = df.dropna(subset=['latitude', 'longitude'])

fig = px.scatter_map(
    df_map,
    lat="latitude",
    lon="longitude",
    color="price_per_sqft",               # color by affordability
    size="sale_price",                    # bigger = more expensive total sale
    hover_data=["borough_y", "bldgclass", "building_age"],
    color_continuous_scale="RdYlBu_r",
    zoom=9.5,                             # good starting zoom for NYC
    title="NYC Housing Sales: Price per Sq Ft by Location<br>(Darker = more expensive per sq ft)",
    height=900
)

fig.update_layout(
    margin={"r":0, "t":50, "l":0, "b":0},
    title_font_size=20
)

# Save interactive HTML (always works, great for viewing/submission)
fig.write_html("../images/nyc_housing_map_interactive.html")

# Save static high-res PNG — this will work once kaleido is fixed below
fig.write_image("../images/nyc_housing_map.png", scale=2)

fig.show()

plt.figure(figsize=(10,8))
sns.heatmap(
    df[corr_cols].corr(),
    annot=True,
    cmap="coolwarm",
    fmt=".2f",
    vmin=-1, vmax=1
)
plt.title("What Drives Sale Price? Correlations")
plt.tight_layout()
plt.savefig("../images/correlation_heatmap.png", dpi=300)
plt.show()


