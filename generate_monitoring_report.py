import pandas as pd
import os
import glob
from generate_overview import generate_summary
from utils.plotter import (
    plot_donations_by_date, 
    plot_data_points_by_category, 
    plot_timestamp_distribution,
    plot_vote_distribution
)
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

print(len(df_usable))
print(df_usable.head())

##### print out survey distributions

# Convert to numeric first (which preserves NaN), then describe only non-NaN values
stats = df_usable.loc[:,['Q1_gender','Q2_age','Q3_education','Q7_polInt-0']].describe(percentiles=[0.5]).round(2)

print(stats)

party_dict = {0:'SPD',
1:'CDU/CSU',
2:'Bündnis 90/Die Grünen',
3:'FDP',
4:'AfD',
5:'Die Linke',
6:'BSW',
7:'Andere Partei',
8:'Ungültig',
9:'Keine Angabe',
10:'Nicht wahlberechtigt',
11:'Nicht wählen'}

df_usable['Q5_first_vote'] = df_usable['Q5_first_vote'].map(party_dict)
df_usable['Q6_second_vote'] = df_usable['Q6_second_vote'].map(party_dict)

print(Counter(df_usable['Q5_first_vote']))
print(Counter(df_usable['Q6_second_vote']))

# Create a grouped bar plot for first and second votes
plot_vote_distribution(df_usable, save=True)

# Plot distribution of timestamps over days with 5am cutoff
plot_timestamp_distribution(df_usable, timestamp_column='end_time', save=True)
