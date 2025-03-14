import pandas as pd
import os
import glob
from monitoring.scripts.generate_overview import generate_summary
from monitoring.utils.plotter import (
    plot_data_points_by_category,
    plot_timestamp_distribution,
    plot_vote_distribution
)
from monitoring.utils.survey_codes import PARTY_DICT
from collections import Counter

# Get list of all CSV files in the overview directory
overview_files = glob.glob('./data/overview/overview_*.csv')
# Find most recent file based on modification time
latest_file = max(overview_files, key=os.path.getmtime)
# Read the most recent CSV file
df = pd.read_csv(latest_file)
# print summary and save filtered overview for usable ones for further analysis
generate_summary(df, save_usable=True)

# load filtered overview for usable ones for further analysis
df_usable = pd.read_csv('./data/overview/usable_overview.csv')

# plot donations by date, without the 5am adjustment if of interest
# plot_donations_by_date(df_usable, save=True)

plot_data_points_by_category(df_usable, save=True)

##### print out survey distributions

# Convert to numeric first (which preserves NaN), then describe only non-NaN values
stats = df_usable.loc[:,['Q1_gender','Q2_age','Q3_education','Q7_polInt-0']].describe(percentiles=[0.5]).round(2)

print(stats)

# Use the imported PARTY_DICT instead of defining it inline
df_usable['Q5_first_vote'] = df_usable['Q5_first_vote'].map(PARTY_DICT)
df_usable['Q6_second_vote'] = df_usable['Q6_second_vote'].map(PARTY_DICT)

print(Counter(df_usable['Q5_first_vote']))
print(Counter(df_usable['Q6_second_vote']))

# Create a grouped bar plot for first and second votes
plot_vote_distribution(df_usable, save=True)

# Plot distribution of timestamps over days with 5am cutoff
plot_timestamp_distribution(df_usable, timestamp_column='end_time', save=True)
