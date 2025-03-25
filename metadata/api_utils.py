import requests

from metadata import settings


def get_video_metadata(video_id):
    """
    Fetch video metadata from the API.

    Args:
        video_id (str): The ID of the video to retrieve.

    Returns:
        dict: Video metadata if successful, None if an error occurs.
    """
    url = settings.VIDEO_GET_ENDPOINT + video_id
    headers = {"Authorization": f"Token {settings.AUTH_TOKEN}"}

    try:
        response = requests.get(url, headers=headers)
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

    url = settings.VIDEO_PATCH_ENDPOINT + video_id + '/update/'
    headers = {
        "Authorization": f"Token {settings.AUTH_TOKEN}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error updating video metadata: {e}")
        return None
