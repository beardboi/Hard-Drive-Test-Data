import numpy as np
import pandas as pd

# Read the csv file.
df = pd.read_csv("harddrive.csv")

# Original dataframe info.
df.info()

# Put the headers in a list.
headers = df.columns.values.tolist()

# See the min & max values for each column.
# for header in headers:
#     print(f"{header} -> Min: {df[header].min()} to Max: {df[header].min()}")

# Columns that will be loaded
sh_columns = []

# Do not load the raw columns.
for header in headers:
    if "raw" not in header or "capacity_bytes" not in header:
        sh_columns.append(header)

# Read the file having filtered the raw value columns.
df = pd.read_csv("harddrive.csv", 
                  usecols = sh_columns,
                  converters= {
                      "date": str,
                      "model": str,
                      "serial_number": str
                  })

# Fill the NA values with 0.
df2 = df.fillna(0)

# Function to resize the datatypes
def compress_dataframe(dataframe):
    for column in sh_columns:
        if dataframe[column].dtype == np.float64 or dataframe[column].dtype == np.int64:
            dataframe[column] = dataframe[column].astype(np.uint8)

# Compress the dataframe clean from NA values.
compress_dataframe(df2)

# New dataframe info
df2.info()
