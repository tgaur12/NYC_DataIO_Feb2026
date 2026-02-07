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
print(df.isnull().sum())
df["resarea"] = df["resarea"].fillna(0)
#change the data type of yearbuilt, numfloors, building_age
df["yearbuilt"] = pd.to_numeric(df["yearbuilt"].fillna(0).astype('int64'))
df["numfloors"] = pd.to_numeric(df["numfloors"].fillna(0).astype('int64'))
df["building_age"] = pd.to_numeric(df["building_age"].fillna(0).astype('int64'))
print(df.dtypes)




