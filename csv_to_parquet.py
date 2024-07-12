import pandas as pd
import os

curr_path = os.path.dirname(os.path.abspath(__file__))

csv_fnm = 'name_and_address.csv'
parquet_fnm = 'name_and_address.parquet'

csv_file = '{}\{}'.format(curr_path, csv_fnm)
parquet_file = '{}\{}'.format(curr_path, parquet_fnm)

df = pd.read_csv(csv_file)
df.to_parquet(parquet_file)
