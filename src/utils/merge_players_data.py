import pandas as pd 
from tqdm import tqdm
tqdm.pandas(desc="Merge players data with there match odds")

def _form_odds(name): 
    if pd.isnull(name):
        return None
    parts = name.replace(".", "").replace("-", "").replace("'", "").split()
    if(len(parts) > 2):
        return None
    
    return f"{parts[0][:3].lower()} {parts[1].lower()}"

def _form_atp(name): 
    if pd.isnull(name):
        return None
    parts = name.replace(".", "").replace("-", "").replace("'", "").split()
    if(len(parts) > 2):
        return None
    
    return f"{parts[1][:3].lower()} {parts[0][0].lower()}"

def merge_on_name_and_date(df1: pd.DataFrame, df2: pd.DataFrame, date_col: str = "date"):
    """
    Merge two tennis match datasets based on normalized player names and match dates.
    Handles swapped winner/loser order in the odds dataset (df2).

    Parameters:
        df1 (pd.DataFrame): Match statistics with full player names.
        df2 (pd.DataFrame): Odds data with abbreviated player names.
        date_col (str): Name of the date column (default: "date").

    Returns:
        pd.DataFrame: Merged DataFrame containing matches with aligned names and dates.
    """
    df1 = df1.copy()
    df2 = df2.copy()

    df1.columns = df1.columns.str.lower()
    df2.columns = df2.columns.str.lower()

    # Normalize the keys in the df1 (players games stas)
    df1["winner_key"] = df1["winner"].apply(_form_atp)
    df1["loser_key"] = df1["loser"].apply(_form_atp)
    df1[date_col] = pd.to_datetime(df1[date_col], format="%Y%m%d")

    # Normalize the keys in the df2 (odds)
    df2["winner_key"] = df2["winner"].apply(_form_odds)
    df2["loser_key"] = df2["loser"].apply(_form_odds)
    df2[date_col] = pd.to_datetime(df2[date_col], format="%Y-%m-%d")

    match_key_dict = {
        (row[date_col], frozenset([row["winner_key"], row["loser_key"]])): row["winner_key"]
        for _, row in df1.iterrows()
    }
    def fix_order(row):
        match_key = (row[date_col], frozenset([row["winner_key"], row["loser_key"]]))
        correct_winner = match_key_dict.get(match_key)

        if correct_winner is not None and row["winner_key"] != correct_winner:
            # swap keys and original names
            row["winner_key"], row["loser_key"] = row["loser_key"], row["winner_key"]
            row["winner"], row["loser"] = row["loser"], row["winner"]
        return row
    # Apply fix_order with progress bar
    df2 = df2.progress_apply(fix_order, axis=1)

    # Merge on date and normalized names
    merged = pd.merge(
        df1,
        df2,
        on=[date_col, "winner_key", "loser_key"],
        suffixes=("_df1", "_df2"),
        how="left",
    )
    return merged



# ATP
# atp_df = pd.DataFrame({
#     'date': ['2024-01-01', '2024-01-01', '2024-01-01'],
#     'winner': ['Grigor Dimitrov', 'Luca Van Assche', 'Yannick Hanfmann'],
#     'loser': ['Jordan Thompson', 'Xy', 'James Duckworth']
# })

# # Odds
# odds_df = pd.DataFrame({
#     'date': ['2024-01-01', '2024-01-01', '2024-01-01'],
#     'winner': ['Dimitrov G.', 'Van Assche L.', 'Hanfmann Y.'],
#     'loser': ['Thompson J.', 'Xy', 'Duckworth J.']
# })

# atp_df = pd.read_csv("./data/raw/atp_men_2000_2024/all_from_2000_to_2024.csv")
# odds_df = pd.read_csv("./data/raw/atp_odds_2001_2024/all_from_2001_to_2024.csv")
# atp_df = atp_df.rename(columns={"tourney_date": "date", "winner_name": "winner", "loser_name": "loser"})
# odds_df = odds_df.rename(columns={"Date": "date", "Winner": "winner", "Loser": "loser"})

# This test code runs all the time
# merge = merge_on_name_and_date(atp_df, odds_df)
# print(merge)

def merge_players_to_matches(players_df, original_df):
    """
        Merge the players data back together player1 vs player2 based on ther tourney_id, match_num, player_name and tourney_date
    """
    players_df = players_df.drop_duplicates(subset=['tourney_id', 'match_num', 'player_name', 'tourney_date'])

    original_df['tourney_date'] = pd.to_datetime(original_df['tourney_date'])
    players_df['tourney_date'] = pd.to_datetime(players_df['tourney_date'])

    # Csak a szükséges oszlopokat tartjuk meg players_df-ben
    id_cols = ['tourney_id', 'match_num', 'player_name', 'tourney_date']
    stat_cols = [col for col in players_df.columns if col not in id_cols + ['id', 'hand', 'ioc', 'ht', 'age']]
    players_df_reduced = players_df[id_cols + stat_cols]


    # Winner merge
    merged = original_df.merge(
        players_df_reduced,
        left_on=['tourney_id', 'match_num', 'winner_name', 'tourney_date'],
        right_on=['tourney_id', 'match_num', 'player_name', 'tourney_date'],
        how='left'
    ).rename(columns={col: f'winner_{col}' for col in stat_cols})

    merged = merged.drop(columns=['player_name'])

    # Loser merge
    merged = merged.merge(
        players_df_reduced,
        left_on=['tourney_id', 'match_num','loser_name', 'tourney_date'],
        right_on=['tourney_id', 'match_num', 'player_name', 'tourney_date'],
        how='left'
    ).rename(columns={col: f'loser_{col}' for col in stat_cols})

    merged = merged.drop(columns=['player_name'])
    return merged