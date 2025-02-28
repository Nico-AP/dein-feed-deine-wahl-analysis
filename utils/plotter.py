import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from collections import Counter

def plot_donations_by_date(df, save=False):
    
    # Convert end_time to datetime, dropping timezone info since it's all the same
    df['day_date'] = pd.to_datetime(df['end_time']).dt.date
    # Group by date and count rows
    daily_counts = df['day_date'].value_counts().sort_index()

    # Create the bar plot
    plt.figure(figsize=(12, 6), facecolor='white')  # Set figure background to white
    ax = plt.gca()
    ax.set_facecolor('white')  # Set plot area background to white
    bars = sns.barplot(x=daily_counts.index, y=daily_counts.values)

    # Add value labels on top of each bar
    for i, v in enumerate(daily_counts.values):
        ax.text(i, v, str(v), ha='center', va='bottom')

    # Customize the plot
    plt.title('Spenden nach Tagen', fontsize=14)
    plt.xlabel('Date')
    plt.ylabel('Number of Records')
    plt.xticks(rotation=45)
    plt.tight_layout()

    if save:
        plt.savefig('plots/donations_by_date.png')


def plot_data_points_by_category(df, save=False):
    subset = ['AngeseheneVideos_n_datapoints',
          'Likes_n_datapoints',
          'Suchen_n_datapoints',
          'Shares_n_datapoints',
          'Posts_n_datapoints',
          'Kommentare_n_datapoints',
          'FolgendeAccounts_n_datapoints',
          'GefolgteAccounts_n_datapoints',
          'BlockierteAccounts_n_datapoints']
    # Calculate mean, median, max, and min for each metric
    means = df[subset].mean()
    medians = df[subset].median()
    maxs = df[subset].max()
    mins = df[subset].min()

    # Create figure
    plt.figure(figsize=(15, 8), facecolor='white')
    ax = plt.gca()
    ax.set_facecolor('white')

    # Create bar positions
    x = np.arange(len(subset))
    width = 0.2  # Reduced width to accommodate more bars

    # Create bars
    mean_bars = ax.bar(x - 1.5*width, means, width, label='Mean', color='skyblue')
    median_bars = ax.bar(x - 0.5*width, medians, width, label='Median', color='lightgreen')
    max_bars = ax.bar(x + 0.5*width, maxs, width, label='Max', color='salmon')
    min_bars = ax.bar(x + 1.5*width, mins, width, label='Min', color='lightgray')

    # Set y-axis to logarithmic scale
    ax.set_yscale('log')

    # Add value labels on the bars
    def autolabel(rects):
        for rect in rects:
            height = rect.get_height()
            ax.annotate(f'{height:.1f}',
                    xy=(rect.get_x() + rect.get_width()/2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom', rotation=0)

    autolabel(mean_bars)
    autolabel(median_bars)
    autolabel(max_bars)
    autolabel(min_bars)

    # Customize the plot
    plt.title('Statistics of Data Points per Category (Log Scale)', fontsize=14)
    plt.xlabel('Categories')
    plt.ylabel('Number of Data Points (log scale)')

    # Rotate and align the tick labels so they look better
    plt.xticks(x, [label.replace('_n_datapoints', '') for label in subset], rotation=45, ha='right')

    # Add legend
    plt.legend()

    # Adjust layout to prevent label cutoff
    plt.tight_layout()

    if save:
        plt.savefig('plots/data_points_by_category.png')

def plot_timestamp_distribution(df, timestamp_column='end_time', save=True):
    """
    Plot the distribution of timestamps over days, with days defined as 5am to 5am.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        DataFrame containing the timestamp column
    timestamp_column : str
        Name of the column containing timestamps
    save : bool
        Whether to save the plot to a file
    """
    plt.figure(figsize=(12, 6), facecolor='white')
    
    # Convert timestamp column to datetime if it's not already
    if not pd.api.types.is_datetime64_any_dtype(df[timestamp_column]):
        df_temp = df.copy()
        df_temp['timestamp'] = pd.to_datetime(df[timestamp_column])
    else:
        df_temp = df.copy()
        df_temp['timestamp'] = df[timestamp_column]
    
    # Adjust the date to previous day if time is before 5am
    df_temp['adjusted_date'] = df_temp['timestamp'].dt.date
    early_morning_mask = df_temp['timestamp'].dt.hour < 5
    df_temp.loc[early_morning_mask, 'adjusted_date'] = df_temp.loc[early_morning_mask, 'timestamp'].dt.date - pd.Timedelta(days=1)
    
    # Count occurrences by adjusted date
    daily_counts = df_temp['adjusted_date'].value_counts().sort_index()
    
    # Create the bar plot
    ax = plt.gca()
    ax.set_facecolor('white')
    bars = plt.bar(daily_counts.index, daily_counts.values, color='coral')
    
    # Add value labels on top of each bar
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                 str(int(height)), ha='center', va='bottom')
        
    # Format the plot
    plt.title(f'Distribution of {timestamp_column} by Day (5am to 5am)', fontsize=14)
    plt.xlabel('Date (5am to 5am next day)')
    plt.ylabel('Count')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    
    if save:
        plt.savefig(f'plots/{timestamp_column}_distribution_5am_cutoff.png')
    
    return plt

def plot_vote_distribution(df, save=True):
    """
    Create a grouped bar plot for first and second votes.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        DataFrame containing the vote columns 'Q5_first_vote' and 'Q6_second_vote'
    save : bool
        Whether to save the plot to a file
    """
    # Filter out nan values before counting
    first_vote_counts = Counter([vote for vote in df['Q5_first_vote'] if not pd.isna(vote)])
    second_vote_counts = Counter([vote for vote in df['Q6_second_vote'] if not pd.isna(vote)])

    # Get all unique parties from both votes
    all_parties = sorted(set(list(first_vote_counts.keys()) + list(second_vote_counts.keys())))

    # Create lists for plotting, ensuring all parties are included in both
    first_votes = [first_vote_counts.get(party, 0) for party in all_parties]
    second_votes = [second_vote_counts.get(party, 0) for party in all_parties]

    # Set up the figure
    plt.figure(figsize=(14, 8), facecolor='white')
    ax = plt.gca()
    ax.set_facecolor('white')

    # Set width of bars
    bar_width = 0.35
    index = np.arange(len(all_parties))

    # Create the grouped bars
    bar1 = plt.bar(index - bar_width/2, first_votes, bar_width, 
                  color='skyblue', label='Erststimme (Direktkandidat)')
    bar2 = plt.bar(index + bar_width/2, second_votes, bar_width,
                  color='lightgreen', label='Zweitstimme (Partei)')

    # Add labels, title and legend
    plt.xlabel('Partei', fontsize=12)
    plt.ylabel('Anzahl', fontsize=12)
    plt.title('Verteilung der Erst- und Zweitstimmen', fontsize=14)
    plt.xticks(index, all_parties, rotation=45, ha='right')
    plt.legend()

    # Add value labels on top of each bar
    for i, v in enumerate(first_votes):
        if v > 0:  # Only add label if there's a value
            plt.text(i - bar_width/2, v, str(v), ha='center', va='bottom')

    for i, v in enumerate(second_votes):
        if v > 0:  # Only add label if there's a value
            plt.text(i + bar_width/2, v, str(v), ha='center', va='bottom')

    # Adjust layout and save
    plt.tight_layout()
    
    if save:
        plt.savefig('plots/vote_distribution_comparison.png')
    
    return plt
