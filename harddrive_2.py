import pandas as pd

# Function to filter the date
def filter_pd_date(date_pattern):
    return pd.concat(
        # If the row value contains the pattern date, ignore NA values.
        df[df["date"].str.contains(date_pattern, na = False)] for df in
        pd.read_csv("harddrive.csv", 
                    usecols = ["date", "model", ], 
                    chunksize=780000
                    )
    )

# Get the dataframe filtered by the date.
df = filter_pd_date("2016-04")

print(df)
print(type(df))
