import pandas as pd 
import os
from dotenv import load_dotenv

load_dotenv()
DEFAULT_INTERIM_DATA_PATH = os.getenv("DEFAULT_INTERIM_DATA_PATH")

def load_interim_data(url: str = DEFAULT_INTERIM_DATA_PATH):
    if os.path.isfile(url):
        return pd.read_csv(url, parse_dates=["date"], low_memory=False).sort_values(by="date").reset_index(drop=True)
    else: 
        print("[ERROR] Interim file do not exist")
