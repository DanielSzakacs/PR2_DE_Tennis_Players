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


def drop_hight_na_columns(df: pd.DataFrame, threshold: int = 0.6):
    """
        Removes columns where missing values are evaluated by the appropriate threshold.

        Parameters:
        df (pd.DataFrame): The input data frame
        threshold (float): The proportion of missing values above which to delete (e.g. 0.7 = 70%)

        Returns:
        pd.DataFrame: The new data frame, without the problematic columns
    """
    na_ratio = df.isna().mean()
    columns_to_drop = na_ratio[na_ratio > threshold].index
    print(f"[INFO] Droping features {columns_to_drop}")
    return df.drop(columns=columns_to_drop)


def fill_na_median(df: pd.DataFrame, threshold: int = 0.3):
    """
        Fill the numerical columns with there median if the NA ration reaches the threshold
        Parameters: 
        df (pd.DataFrame): The input data frame
        threshold (float): The proportion of missing values (e.g. 0.4 = 40%)

        Returns:
        pd.DataFrame: The new data frame, with the filled columns
    """
    numerical_df = df.select_dtypes(include="number")

    na_ratio = numerical_df.isna().mean()
    columns_to_drop = na_ratio[na_ratio < threshold].index
    print(f"[INFO] Columns which will be filled with there median: {columns_to_drop}")
    df[columns_to_drop] = df[columns_to_drop].fillna(df[columns_to_drop].median())
    return df
    