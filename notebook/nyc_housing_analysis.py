import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

#Accessing the dataset
file_path = "../nyc_housing_base.csv"

## Check if file exists
if not os.path.exists(file_path):
    raise FileNotFoundError(
        f"Dataset not found at {file_path}. "
        "Make sure nyc_housing_base.csv is in the project root directory."
    )

# Load CSV
df = pd.read_csv(file_path, encoding="latin1", engine="python")

print("Dataset loaded successfully!")
print("Shape:", df.shape)

df.head()

print("\nColumns: \n", df.columns)
print("\nDataset Info:")
print(df.info())

# data cleaning
useful_col = ["borough_y", "sale_price", "yearbuilt", "lotarea", "bldgarea", "resarea", "comarea",
              "unitsres", "unitstotal", "numfloors", "latitude", "longitude", "landuse", "bldgclass",
              "building_age"]
df = df[useful_col]

# fill in empty cols
print(df.isnull().sum())
df["building_age"] = df["building_age"].fillna(df.groupby("bldgclass")["building_age"].transform('median').fillna(0))
df["yearbuilt"] = df["yearbuilt"].fillna((2023 - df["building_age"]).fillna(1900).astype(int))
df["bldgarea"] = df["bldgarea"].fillna(df.groupby("bldgclass")["bldgarea"].transform('median').fillna(1000))
df["resarea"] = df["resarea"].fillna(0)
df["comarea"] = df["comarea"].fillna(0)
df["numfloors"] = df["numfloors"].fillna(df.groupby("bldgclass")["numfloors"].transform('median').fillna(1))
df["latitude"] = df["latitude"].fillna(df.groupby("borough_y")["latitude"].transform('median'))
df["longitude"] = df["longitude"].fillna(df.groupby("borough_y")["longitude"].transform('median'))

print("After cleaning:\n", df.isnull().sum())
print("Sample ages:", df["building_age"].describe())  # Check: realistic 0-150?

# Remove crazy outliers (top 1% prices, negative areas, impossible ages)
df = df[(df["sale_price"] > 0) & (df["sale_price"] < 10_000_000)]
df = df[(df["bldgarea"] > 0) & (df["bldgarea"] < 500_000)]
df = df[(df["building_age"] >= 0) & (df["building_age"] < 200)]
df = df.dropna(subset=["latitude", "longitude"])  # Musthave location for map

print(f"After outlier removal: {len(df):,} rows (from {len(df)*1.5:+,} originally)")
# average price by borough
avg_price_borough = df.groupby("borough_y")["sale_price"].mean().sort_values()

print("Average price by borough:", avg_price_borough)

# Price ber sq foot
df["price_per_sqft"] = df["sale_price"] / df["bldgarea"].replace(0, 1)  # Avoid divide-by-zero
df["price_per_sqft"] = df["price_per_sqft"].clip(0, 5000)  # Cap insane $5000/sqft

pxsqft_borough = df.groupby("borough_y")["price_per_sqft"].mean().sort_values(ascending=False)
print("Price per Sq Ft by Borough:\n", pxsqft_borough.round(0))

plt.figure(figsize=(8,5))
sns.barplot(x=pxsqft_borough.index, y=pxsqft_borough.values, palette="coolwarm")
plt.title("Best Value Boroughs ($/sq ft)")
plt.ylabel("$ per Square Foot")
plt.savefig("../images/price_per_sqft.png", dpi=300, bbox_inches='tight')
plt.show()

# plts by borough -> helps figure out highest average price and lowest average price
# based on location
plt.figure(figsize=(8,5))
sns.barplot(
    x=avg_price_borough.index,
    y=avg_price_borough.values / 1_000_000,  # in millions for readability
    hue=avg_price_borough.index,
    palette='viridis',
    legend=False
)
plt.title("Average Housing Price by Borough (Million $)")
plt.xlabel("Borough")
plt.ylabel("Average Housing Price ($)")
plt.xticks(rotation=45)
plt.tight_layout()
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
