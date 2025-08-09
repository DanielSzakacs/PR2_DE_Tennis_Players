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

def plot_summary_numerical_features(df: pd.DataFrame, target_col: str):
    """
    Generates summary statistics and visualizations for numeric features.

    For each numeric column (excluding the target column), this function calculates:
      - Percentage of missing values
      - Minimum, maximum, mean, median, and standard deviation
    Additionally, it creates:
      - A histogram with a KDE curve
      - A boxplot to visualize distribution and outliers

    Args:
        df (pd.DataFrame): 
            The input DataFrame containing numeric and other features.
        target_col (str, optional): 
            The name of the target column to exclude from numeric analysis. Defaults to 'is_winner'.

    Returns:
        pd.DataFrame: 
            A DataFrame containing summary statistics for all analyzed numeric features, 
            sorted by missing percentage in descending order.

    Notes:
        - Histograms and boxplots are displayed for each numeric feature.
        - Missing percentage is calculated as the fraction of NaN values multiplied by 100.
    """
    numerical_df = df.select_dtypes(include="number")
    numerical_cols = [col for col in numerical_df if col != target_col]
    summary_stats = []
    for col in numerical_cols:
        # Missing data ratio
        missing_pct = df[col].isna().mean() * 100

        # Stats
        col_min = df[col].min()
        col_max = df[col].max()
        col_mean = df[col].mean()
        col_median = df[col].median()
        col_std = df[col].std()

        summary_stats.append({
            'column': col,
            'missing_pct': missing_pct,
            'min': col_min,
            'max': col_max,
            'mean': col_mean,
            'median': col_median,
            'std': col_std
        })

        # Vizulise
        fig, axes = plt.subplots(1,2, figsize=(10,4))

        sns.histplot(df[col], bins=30, kde=True, color='lightblue', ax=axes[0])
        axes[0].set_title(f"{col} - Histogram")

        sns.boxplot(x=df[col], ax=axes[1], color='lightgreen')
        axes[1].set_title(f"{col} - Boxplot")

        plt.tight_layout()
        plt.show()
    
    # Stats into a DataFrame
    num_summary_df = pd.DataFrame(summary_stats)
    num_summary_df.sort_values(by='missing_pct', ascending=False)

    return num_summary_df