import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns


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
df["yearbuilt"] = df["yearbuilt"].fillna(0).astype('int64')
df["numfloors"] = df["numfloors"].fillna(0).astype('int64')
df["building_age"] = df["building_age"].fillna(0).astype('int64')
df["resarea"] = df["resarea"].fillna(0)
df["comarea"] = df["comarea"].fillna(0)
df["numfloors"] = df["numfloors"].fillna(df["numfloors"].mode()[0])
df["latitude"] = df["latitude"].fillna(df["latitude"].mode()[0])
df["longitude"] = df["longitude"].fillna(df["longitude"].mode()[0])

# average price by borough
avg_price_borough = df.groupby("borough_y")["sale_price"].mean().sort_values()

print("Average price by borough:", avg_price_borough)

# plts by borough -> helps figure out highest average price and lowest average price
# based on location
plt.figure(figsize=(8,5))
sns.barplot(x=avg_price_borough.index, y=avg_price_borough.values)
plt.title("Average Housing Price by Borough")
plt.xlabel("Borough")
plt.ylabel("Average Housing Price ($)")
plt.xticks(rotation=45)
plt.tight_layout()
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
plt.show()


# saves images
plt.savefig("../images/avg_price_by_borough.png")
plt.savefig("../images/price_vs_bldgarea.png")
plt.savefig("../images/building_age_vs_price.png")

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
