import json
import requests
import time
from tqdm import tqdm
import os
import pandas as pd


def save_json_file(path, data):
    with open(path, 'w') as json_file:
        json.dump(data, json_file, indent=4)


def flatten_responses(responses):
    """
    Response dict has initially the following structure:
    {
        'participant_id': _,
        'response_data': {'var_1': _, 'var_2': _, etc.}
    }

    Flattens this structure to:
    {
        'participant_id': _,
        'var_1': _,
        'var_2': _,
        etc.
    }
    """
    flat_responses = []
    for response in responses:
        d = dict()
        for key, value in response.items():
            if key == 'response_data':
                for k, v in value.items():
                    d[k] = v
            else:
                d[key] = value
        flat_responses.append(d.copy())
    return flat_responses


def get_pol_videos(endpoint, auth_token, output_file=None, date=None, username=None):
    """
    Fetch political videos from the API with pagination support and save to file.
    
    Parameters:
    -----------
    endpoint : str
        The API endpoint URL
    auth_token : str
        Authentication token for the API
    output_file : str, optional
        Path to save the output CSV file. If None, data is only returned but not saved.
    date : str, optional
        Filter videos by date (format: YYYY-MM-DD)
    username : str, optional
        Filter videos by username
        
    Returns:
    --------
    pandas.DataFrame
        DataFrame containing the video data
    """
    headers = {
        'Authorization': f'Token {auth_token}',
        'Content-Type': 'application/json'
    }

    all_results = []
    
    # Set initial URL based on parameters
    if date and username:
        url = f"{endpoint}?date={date}&username={username}"
    elif date:
        url = f"{endpoint}?date={date}"
    elif username:
        url = f"{endpoint}?username={username}"
    else:
        url = endpoint

    # Get first response to get total count
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        return pd.DataFrame()
        
    data = response.json()
    total_records = data['count']
    all_results.extend(data['results'])
    
    # Initialize progress bar
    pbar = tqdm(total=total_records, desc="Fetching videos", unit="records")
    pbar.update(len(data['results']))
    
    # Continue with pagination
    url = data['next']
    while url:
        response = requests.get(url, headers=headers)
        
        if response.status_code != 200:
            print(f"\nError: {response.status_code}")
            break
            
        data = response.json()
        all_results.extend(data['results'])
        
        # Update progress bar
        pbar.update(len(data['results']))
        
        # Update URL for next iteration
        url = data['next']
        
        # Optional: add a small delay to be nice to the API
        time.sleep(0.5)

    pbar.close()
    print(f"\nTotal records fetched: {len(all_results)}")
    
    # Convert to DataFrame
    df = pd.DataFrame(all_results)
    
    # Save to file if output_file is specified
    if output_file:
        print(f"Saving data to {output_file}")
        df.to_csv(output_file, index=False)
        
    return df
