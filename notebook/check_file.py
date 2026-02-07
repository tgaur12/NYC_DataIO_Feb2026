import os

file_path = "../data/nyc_housing_base.csv"

print("File exists:", os.path.exists(file_path))
print("File size (bytes):", os.path.getsize(file_path))
