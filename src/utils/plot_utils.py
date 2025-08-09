# Vizualizáció segédfüggvények

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import missingno as msno

def plot_numerical_distributions(cols_name_pairs: list[list[str]], 
                                     title: list[str], 
                                     x_label: list[list[str]], df: pd.DataFrame):

    num_plots = len(cols_name_pairs)
    fig, axes = plt.subplots(num_plots, 1, figsize=(12, 4 * num_plots))  # Egy sorban 1 plot, de mindkét hisztogram

    if num_plots == 1:
        axes = [axes]  # ha csak 1 plot van, akkor listává tesszük, hogy iterálható legyen

    for i in range(num_plots):
        col_pair = cols_name_pairs[i]  # pl. ['p1_age', 'p2_age']
        col1, col2 = col_pair

        ax = axes[i]

        # Két hisztogram egymásra rajzolva, eltérő színnel és felirattal
        sns.histplot(data=df, x=col1, ax=ax, color='skyblue', label='Player 1', bins=50, alpha=0.6)
        sns.histplot(data=df, x=col2, ax=ax, color='sandybrown', label='Player 2', bins=50, alpha=0.6)

        ax.set_title(title[i])
        ax.set_ylabel('Value')
        ax.set_xlabel(x_label[i])
        ax.legend(title='Players')

    plt.tight_layout()
    plt.show()

def plot_missing_values_matrix(df: pd.DataFrame, show_only_missing_values: bool = True):
    """
    Plot the missing values.
    
    Params:
        df: (DataFrame) The input data.
        show_only_missing_values: (bool) If True, only show columns with missing values.
    """
    if(show_only_missing_values):
        missing_values = df.isna().sum()
        missing_cols = missing_values[missing_values > 0].sort_values(ascending=False).index
        df = df[missing_cols]
    msno.matrix(df)

def plot_target_distribution(df: pd.DataFrame, target_feature: str):
    """
    Plots and prints the distribution of the target variable 'target_feature'.

    This function creates a count plot of the 'target_feature' column using Seaborn,
    showing the frequency of each category. It also prints the absolute counts
    and percentage distribution of each class.

    Parameters: 
        df : pd.DataFrame
            The input DataFrame containing an 'target_feature' column.
        target_feature : str
            Name of the target feature

    Returns:
        None
            Displays a plot and prints statistics to the console.
    """
    plt.figure(figsize=(5,4))
    sns.countplot(x=target_feature, data=df, palette="viridis")
    plt.title(f"Terget feature distribution ({target_feature})")
    plt.show()

    target_count = df[target_feature].value_counts()
    target_percent = df[target_feature].value_counts(normalize=True) * 100

    print(f"{target_feature} count number:\n", target_count)
    print("Ration (%)\n", target_percent)