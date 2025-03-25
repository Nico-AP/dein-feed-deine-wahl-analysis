import argparse

from metadata.utils import get_video_list_for_participant


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=(
            'Extracts the IDs of watched videos in 2025 by a given participant.'
        )
    )
    parser.add_argument('--participant_id', help='ID of the participant (i.e., the ID contained in the donation file name).')
    args = parser.parse_args()
    if args.participant_id is None:
        print('No participant ID provided. Exiting.')
    else:
        get_video_list_for_participant(args.participant_id)
