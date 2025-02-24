import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

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
