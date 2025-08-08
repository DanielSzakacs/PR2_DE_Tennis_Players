import os 
import requests
import pandas as pd 

from dotenv import load_dotenv
load_dotenv()

ATP_MATCH_DATA_URL = os.getenv("ATP_TENNIS_MATCH_BY_YEAR")
ATP_MATCH_ODDS_URL = os.getenv("ATP_TENNIS_ODDS_BY_YEAR")

def _download_source_data_by_year(url: str, year: int, output_folder: str = "data/raw"):
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
        print(f"[INFO] Data from year {year} downloaded")
    else: 
        print(f"[ERROR] Exception: {response.status_code} - {response.reason}")
    return pd.read_csv(output_file)  

def _download_atp(year_from: int, year_to: int, output_folder: str):
    """
        Download and merge all the csv file into one csv and return it as a pd.Dataframe
        csv files will be saved in the output folder. If not exist, will be created

        Pramas: 
            year_from: int 
            year_to: int 
            output_folder: str

        Retrun: 
            pd.Datafolder
    """
    print(f"[INFO] Download ATP source data from {year_from} to {year_to}")
    dfs = [
        _download_source_data_by_year(
            ATP_MATCH_DATA_URL.format(year=year), 
            year, 
            output_folder
        )
        for year in range(year_from, year_to + 1)
    ]

    print(f"[INFO] Concat {len(dfs)} of dataframes")
    df_all = pd.concat(dfs, ignore_index=True)
    df_all = df_all.sort_values(by="tourney_date").reset_index(drop=True)
    print(f"[INFO] Save merged dataframe. Length of dataframe: {len(df_all)}")
    df_all.to_csv(output_folder + f"/all_from_{year_from}_to_{year_to}.csv")
    return df_all


def _download_atp_odds(year_from: int, year_to: int, output_folder: str): 
    """
        Download ATP men's odds data

        Params: 
            year_from: int 
            year_to: int 
            output_folder: str

        Return: 
            pd.DataFrame
    """

    dfs = [
        _download_source_data_by_year(
            ATP_MATCH_ODDS_URL.format(year=year),
            year,
            output_folder
        )
        for year in range(year_from, year_to + 1)
    ]

    df_all = pd.concat(dfs, ignore_index=True)
    df_all = df_all.sort_values(by="Date").reset_index(drop=True)
    df_all.to_csv(os.path.join(output_folder, f"all_from_{year_from}_to_{year_to}.csv"), index=False)
    return df_all


def download_all_atp_odds_raw_data():
    _download_atp(year_from=2000,year_to=2024, output_folder="data/raw/atp_men_2000_2024")
    _download_atp_odds(year_from=2001,year_to=2024, output_folder="data/raw/atp_odds_2001_2024")

def download_all_atp_raw_data():
    _download_atp(year_from=2000,year_to=2024, output_folder="data/raw/atp_men_2000_2024")