import pandas as pd 
from tqdm import tqdm
tqdm.pandas(desc="Merge players data with there match odds")

def _normalize_names(name: str):
    """
    Normalize player names by removing dots, hyphens, apostrophes,
    and converting to lowercase.
    
    Parameters:
        name (str): Short format player name (e.g. "Popyrin A.")
    
    Returns:
        str: Normalized player name (e.g. "popyrin a")
    """
    if pd.isnull(name):
        return ""
    name = name.replace(".", "").replace("-", "").replace("'", "")
    return name.lower()

def _normalize_full_name(name: str):
    """
    Normalize full player names by converting to a comparable short format:
    [last name] [first initial], in lowercase.

    Parameters:
        name (str): Full player name (e.g. "Alexei Popyrin")

    Returns:
        str: Normalized name (e.g. "popyrin a")
    """
    if pd.isnull(name):
        return ""
    parts = name.replace(".", "").replace("-", "").replace("'", "").split()
    if len(parts) < 2:
        return name.lower()
    last = parts[-1]
    first_init = parts[0][0] if len(parts[0]) > 0 else ""
    if len(parts) == 3:
        middle = parts[1]
        return f"{middle} {last} {first_init}".lower()
    return f"{last} {first_init}".lower()
    
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
    df1["winner_key"] = df1["winner"].apply(_normalize_full_name)
    df1["loser_key"] = df1["loser"].apply(_normalize_full_name)
    df1[date_col] = pd.to_datetime(df1[date_col])

    # Normalize the keys in the df2 (odds)
    df2["winner_key"] = df2["winner"].apply(_normalize_names)
    df2["loser_key"] = df2["loser"].apply(_normalize_names)
    df2[date_col] = pd.to_datetime(df2[date_col])

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
        how="left"
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

# merge = merge_on_name_and_date(atp_df, odds_df)
# print(merge)
