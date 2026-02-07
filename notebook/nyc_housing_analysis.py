import pandas as pd
import os
import matplotlib.pyplot as plt

#Accessing the dataset
workspace_folder = "data"
file_path = os.path.join(workspace_folder, "nyc_housing_base.csv")

## Check if file exists
if not os.path.exists(file_path):
    raise FileNotFoundError(
        f"Dataset not found at {file_path}. "
        "Make sure nyc_housing_base.csv is inside the 'data' folder."
    )

# Load CSV
df = pd.read_csv(file_path, encoding="latin1", engine="python")

print("Dataset loaded successfully!")
print("Shape:", df.shape)

df.head()
