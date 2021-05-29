import pandas as pd
import sqlite3
import time

# First method using pandas
def get_avg_pandas(model):
    df = pd.read_csv("harddrive.csv")
    df = df[df["model"] == model]
    daily_count = df.groupby(["date","model"])["date"].count()
    average = daily_count.mean()
    print(f"Average of daily readings performed: {average}")

# Best approach using sqlite and indexes.
def index_data():
    db = sqlite3.connect("harddrive.sqlite")
    for df in pd.read_csv("harddrive.csv",
                          usecols=["date", "model"],
                          chunksize=1000000):
        df.to_sql("harddrive", db, if_exists="append")
    
    # Create index for the model column.
    # Take the execution time.
    start_time = time.time()
    db.execute("CREATE INDEX model ON harddrive(model)")
    db.close()

# Define a simple function to get the daily avg given certain hardrive model
def get_daily_avg(model):
    connection = sqlite3.connect("harddrive.sqlite")
    # another_query = "SELECT COUNT(`date`) FROM harddrive WHERE model = ? GROUP BY `date`"
    sub_query = "SELECT COUNT(*) as daily_count FROM harddrive WHERE model = ? GROUP BY `date`"
    query = f"SELECT AVG(daily_count) FROM ({sub_query}) AS daily_count_table"
    values = (model,)
    data = pd.read_sql_query(query, connection, params=values)
    connection.close()
    print(f"Average of daily readings performed: {data}")
    return data

print("Calculating...")

# First approach
start_time = time.time()
get_avg_pandas("Hitachi HDS5C3030ALA630")
print(f"Execution time using only pandas: {time.time() - start_time} seconds \n")

# Second approach
index_data()
start_time = time.time()
get_daily_avg("Hitachi HDS5C3030ALA630")
print(f"Execution time using pandas + sqlite: {time.time() - start_time} seconds")
