import requests

from metadata import settings


def create_csv_result(dict_result):
    return

def get_metadata_for_videos(video_list, output="json"):
    result = {}
    for video_id in video_list:
        metadata = get_video_metadata(video_id)
        if metadata:
            result[video_id] = metadata

    if output == "json":
        return result

    elif output == "csv":
        csv_result = create_csv_result(result)
        return csv_result

def get_video_metadata(video_id):
    """
    Fetch video metadata from the API.

    Args:
        video_id (str): The ID of the video to retrieve.

    Returns:
        dict: Video metadata if successful, None if an error occurs.
    """
    url = settings.VIDEO_GET_ENDPOINT + video_id

    try:
        response = requests.get(
            url, headers={"Authorization": f"Token {settings.AUTH_TOKEN}"})
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching video metadata: {e}")
        return None

def update_video_metadata(video_id, data):
    """
    Update video metadata via API.

    Args:
        video_id (str): The ID of the video to update.
        data (dict): Dictionary containing the metadata fields to update.

    Returns:
        dict: API response if successful, None if an error occurs.
    """

    url = settings.VIDEO_PATCH_ENDPOINT + video_id
    try:
        response = requests.patch(
            url,
            json=data,
            headers={"Authorization": f"Token {settings.AUTH_TOKEN}",
                     "Content-Type": "application/json"}
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error updating video metadata: {e}")
        return None
