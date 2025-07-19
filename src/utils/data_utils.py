# Adattisztító függvények
import requests
import os
import pandas as pd 

def download_source_data_by_year(url: str, year: int, output_folder: str = "data/raw"):
    """
        Download a single csv file and return it as a pd.Dataframe from github
        
        Params: 
            year: int 
            output_folder: str
        
        Return:
            pd.Dataframe
    """

    output_file = os.path.join(output_folder, f"atp_matches_{year}.csv")
    os.makedirs(output_folder, exist_ok=True)
    response = requests.get(url)
    if response.status_code == 200: 
        with open(output_file, "wb") as f :
            f.write(response.content)
        print(f"{output_file} downloaded")
    else: 
        print(f"Exception: {response.status_code} - {response.reason}")
    return pd.read_csv(output_file)  