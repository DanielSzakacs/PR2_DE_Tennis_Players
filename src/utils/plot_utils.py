# Vizualizáció segédfüggvények

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

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