import os

from dotenv import load_dotenv

load_dotenv()

AUTH_TOKEN = os.getenv('AUTH_TOKEN', None)
VIDEO_GET_ENDPOINT = os.getenv('VIDEO_GET_ENDPOINT', None)
VIDEO_PATCH_ENDPOINT = os.getenv('VIDEO_PATCH_ENDPOINT', None)
VIDEO_LIST_ENDPOINT = os.getenv('VIDEO_LIST_ENDPOINT', None)
METADATA_OUTPUT_PATH = './data/metadata/'
