import pandas as pd
import os
import glob
import pandas as pd
from generate_overview import generate_summary
from utils.plotter import plot_donations_by_date, plot_data_points_by_category

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
# plot donations by date
plot_donations_by_date(df_usable, save=True)

plot_data_points_by_category(df_usable, save=True)