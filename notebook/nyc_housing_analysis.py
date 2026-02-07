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
useful_col = ["borough_y", "sale_price", "zip_code", "yearbuilt", "lotarea", "bldgarea", "resarea", "comarea",
              "unitsres", "unitstotal", "numfloors", "latitude", "longitude", "landuse", "bldgclass",
              "building_age"]
df = df[useful_col]
print(df.isnull().sum())
df["resarea"] = df["resarea"].fillna(0)

#Creating table
df_table = df[useful_col]

df_table.to_csv("../nyc_housing_important_columns.csv", index=False)

print("New CSV file created: nyc_housing_important_columns.csv")
