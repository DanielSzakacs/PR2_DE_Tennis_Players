# Tennis Match Data Analysis & Feature Engineering

## Project Description

This project is a **Data Analysis**-focused pet project that processes and analyzes tennis players’ match data.  
The goal is to prepare a data model based on **historical match statistics** that can later be used to make predictions about match outcomes.

The project showcases:

- downloading and preprocessing raw data,
- data cleaning processes,
- generating new, useful statistical features,
- data analysis and visualization using Matplotlib as Seaborn

---

## Data Processing Workflow

1. **Data Download**

   - Raw data is downloaded in CSV format from a licensed source.
   - The `fetch_data.py` and `merge_players_data.py` scripts handle data merging.

2. **Data Cleaning**

   - Handling missing values
   - Type conversions (datetime, numeric, category)
   - Standardizing text fields
   - Converting measurement units

3. **Feature Engineering**

   - Aggregating historical match statistics (performance in the last N matches)
   - Opponent’s statistical indicators
   - Metrics for trends and performance changes

4. **EDA (Exploratory Data Analysis)**

   - Distribution analysis (histogram, boxplot)
   - Analysis of categorical variables (barplot, countplot)
   - Correlation analysis (heatmap)
   - Temporal trends (lineplot)

5. **Visualization**
   - **Python (Matplotlib, Seaborn)** – detailed analytical charts

---

## Technologies Used

- **Python**: `pandas`, `numpy`, `matplotlib`, `seaborn`
- **Jupyter Notebook**
- **Git / GitHub**

---

## Results & Insights

- Using historical match statistics and newly engineered features, we created a significantly more accurate dataset suitable for predictive modeling.
- During EDA, several strong correlations were found between certain player statistics and match victories.
- The Power BI dashboard enables interactive analysis of players’ past performances.
