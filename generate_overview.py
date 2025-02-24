import json
import sys

import pandas as pd
import os
import time

from datetime import datetime
from dotenv import load_dotenv
from rich.console import Console
from tqdm import tqdm

from utils.data_request import request_data
from utils.utils import save_json_file, flatten_responses


console = Console()

load_dotenv()

API_KEY = os.getenv('API_KEY', None)
PROJECT_ID = os.getenv('PROJECT_ID', None)
BASE_URL = os.getenv('BASE_URL', None)
OVERVIEW_ENDPOINT = os.getenv('OVERVIEW_ENDPOINT', None)
DONATION_ENDPOINT = os.getenv('DONATION_ENDPOINT', None)
RESPONSE_ENDPOINT = os.getenv('RESPONSE_ENDPOINT', None)

def print_to_console(msg):
    sys.stdout.write('\033[F')  # Move cursor up to overwrite the last task message
    sys.stdout.write('\033[K')  # Clear the line
    console.print(msg, end='')
    sys.stdout.write('\033[E')  # Moves cursor down one line
    sys.stdout.flush()


def get_participation_overview():
    """
    Retrieve basic overview data from the ddm API.
    :return: The result as a pandas dataframe, the raw response data.
    """
    console.print('[white]Get participation overview from DDM...[/]')
    overview_data = request_data(OVERVIEW_ENDPOINT, API_KEY)
    participant_data = overview_data['participants']
    df = pd.DataFrame(participant_data)
    df.rename(columns={'external_id': 'participant_id'}, inplace=True)
    return df, overview_data


def get_response_data():
    """
    Retrieve questionnaire response data from the ddm API.
    :return: The result as a pandas dataframe.
    """
    console.print('[white]Get response data from DDM...[/]')
    response_data = request_data(RESPONSE_ENDPOINT, API_KEY)
    responses = response_data['responses']
    flat_responses = flatten_responses(responses)
    df = pd.DataFrame(flat_responses)
    df.rename(columns={'participant': 'participant_id'}, inplace=True)
    return df


def load_donation_overview():
    """
    Read donation overview from disk.
    Create a new list, if overview does not yet exist.
    :return: A list of dictionaries.
    """
    overview_path = './data/overview/donation_overview.json'
    if not os.path.exists(overview_path):
        return []

    with open(overview_path, 'r') as json_file:
        return json.load(json_file)


def download_donation(endpoint, token, participant_id):
    """
    Checks if the donation of the participant has already been downloaded to
    disk. If not, downloads it through the DDM API.

    :param endpoint: URL of API endpoint.
    :param token: Project API Token.
    :param participant_id: External participant ID.
    :return: None
    """

    # Check if donation file already exists.
    path = f'./data/donations/{participant_id}.json'
    if os.path.exists(path):
        print_to_console(f'[cyan]Processing {participant_id}: [bold green]Data for participant already downloaded.')
        return

    # If not, download.
    print_to_console(f'[cyan]Processing {participant_id}: [bold yellow]Downloading data from DDM.')

    payload = {'participants': participant_id}
    donation_data = request_data(endpoint, token, payload, timeout=20)
    save_json_file(path, donation_data)
    time.sleep(0.5)
    return


def exclude_unhandled_participants(donation_overview):
    return [p for p in donation_overview if p['handled']]


def get_participant_list(donation_overview):
    return [p['participant_id'] for p in donation_overview]


def get_participants_to_handle(donation_overview, df_participants):
    all_participants = df_participants['participant_id'].tolist()
    handled_participants = get_participant_list(donation_overview)
    return list(set(all_participants) - set(handled_participants))


def extract_blueprint_information(blueprint, donation):
    bp_id = str(blueprint['id'])
    bp_name = blueprint['name'].replace(' ', '')

    bp_donation = donation['blueprints'].get(bp_id, {})
    if len(bp_donation['donations']) == 0:
        return {
            f'{bp_name}_consent': None,
            f'{bp_name}_status': None,
            f'{bp_name}_n_datapoints': None,
        }
    donation_info = bp_donation['donations'][0]
    if bp_donation:
        donated_data = len(donation_info['data'])
    else:
        donated_data = None

    return {
        f'{bp_name}_consent': donation_info.get('consent'),
        f'{bp_name}_status': donation_info.get('status'),
        f'{bp_name}_n_datapoints': donated_data,
    }


def process_participant(participant, blueprint_data, participation_overview):
    print_to_console(f'[cyan]Processing {participant}: [bold yellow]Starting.')

    d = dict()
    d['participant_id'] = participant

    # Check step of participant in participation_overview
    step = participation_overview.query(f'participant_id == "{participant}"')['current_step'].iloc[0]
    if step < 2:
        print_to_console(f'[cyan]Processing {participant}: [bold yellow]Donation not finished - no download.')
        d['handled'] = False
        return d.copy()

    download_donation(DONATION_ENDPOINT, API_KEY, participant)
    with open(f'./data/donations/{participant}.json', 'r') as json_file:
        donation = json.load(json_file)

    for blueprint in blueprint_data:
        d.update(extract_blueprint_information(blueprint, donation))

    d['handled'] = True
    return d.copy()


def generate_summary(df):
    # Filter entries before start of data collection -> must be refined.
    df = df[df['start_time'] > '2025-02-16']

    # Filter test cases.
    df = df[df['Q2_age'] != '99']

    n_started = df.shape[0]
    n_finished = df['completed'].eq(True).sum()
    n_donated = df['AngeseheneVideos_consent'].eq(True).sum()

    console.print(f'----------------------------------------------------------')
    console.print(f'[bold white]Here come the stats:')
    console.print(f'[yellow]Total started: {n_started}')
    console.print(f'[white]Total completed: {n_finished}')
    console.print(f'[green]Total donated: {n_donated}')
    console.print(f'----------------------------------------------------------')


def ensure_directories_exist():
    """Create necessary data directories if they don't exist."""
    os.makedirs('./data/donations', exist_ok=True)
    os.makedirs('./data/overview', exist_ok=True)


def main():
    console.print('[white]Start script...[/]')
    
    # Create necessary directories
    ensure_directories_exist()
    
    # Load dataframes.
    df_participation, overview_data = get_participation_overview()
    df_responses = get_response_data()

    # Check if local donation overview table already exists and load if necessary.
    donation_overview = load_donation_overview()
    donation_overview = exclude_unhandled_participants(donation_overview)
    participants_to_handle = get_participants_to_handle(donation_overview, df_participation)
    blueprint_data = overview_data['blueprints']

    console.print('')
    pbar = tqdm(total=len(participants_to_handle), dynamic_ncols=True, position=0, leave=True,  colour="magenta")
    for participant in participants_to_handle:
        donation_overview.append(process_participant(participant, blueprint_data, df_participation))
        pbar.update(1)
    pbar.update(1)

    sys.stdout.write('\033[E')
    sys.stdout.write('\033[E')
    console.print('')
    console.print('[bold green]✅ All participants processed![/]')

    console.print('[white]Write donation overview to disc.[/]')
    save_json_file('./data/donations/donation_overview.json', donation_overview)

    # Merge everything.
    df_donations = pd.DataFrame(donation_overview)
    merged_df = df_participation.merge(df_responses, on='participant_id', how='outer').merge(
        df_donations, on='participant_id', how='outer')
    merged_df.head()

    # Save merged DataFrame to CSV.
    console.print('[white]Write participation overview to disc.[/]')
    timestamp = datetime.now().strftime('%Y-%m-%d-%H-%M')
    merged_df.to_csv(f'./data/overview/overview_{timestamp}.csv', index=False)

    generate_summary(merged_df)

    console.print('[bold green]✅ Process finished![/]')

if __name__ == '__main__':
    main()
