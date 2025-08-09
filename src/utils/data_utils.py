# Adattisztító függvények

import pandas as pd 


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
    print(f"[INFO] Threshold: {threshold}")
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
    

def get_missing_values_summary(df: pd.DataFrame):
    """
        Creates a Dataframe with the summary of missing values and their percentiage
    """
    missing_values = df.isnull().sum()
    missing_values = missing_values[missing_values > 0].sort_values(ascending=False)

    missing_percent = (df.isnull().mean() * 100).sort_values(ascending=False)
    missing_df = pd.DataFrame({
        "missing_count": missing_values,
        "missing_percent": missing_percent[missing_values.index].round(2)
    })
    return missing_df