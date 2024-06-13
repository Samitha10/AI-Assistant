import sys,os
import pandas as pd
data_path = os.path.join(os.path.dirname(__file__), '..', 'DataFiles', 'data.csv')

def data_file_importer():
    df = pd.read_csv(data_path)
    return df
