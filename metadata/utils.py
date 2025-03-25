import csv
import json
from datetime import datetime


def get_video_list_for_participant(participant_id, save_to_csv=True, this_year=True):
    """
    Extracts the IDs of watched videos by a given participant.
    Either returns them as a list or saves them to csv.

    CSVs are saved in ./data/donations/video_lists/<participant_id>.csv
    """
    # Get donation of participant
    file_path = f'./data/donations/{participant_id}.json'
    with open(file_path, 'r') as json_file:
        file_content = json.load(json_file)

    # Extract video IDs
    donations = file_content['blueprints']['1']['donations'][0]['data']
    video_ids = []
    for entry in donations:
        if this_year:
            date = datetime.strptime(entry['Date'], "%Y-%m-%d %H:%M:%S")
            if date.year != 2025:
                continue

        video_ids.append(entry['Link'].split('/video/')[1].strip('/'))

    # Save to csv
    if save_to_csv:
        output_path = f'./data/donations/video_lists/{participant_id}.csv'
        with open(output_path, 'w', newline="") as file:
            writer = csv.writer(file)
            for video_id in video_ids:
                writer.writerow([video_id])
        return
    else:
        return video_ids
