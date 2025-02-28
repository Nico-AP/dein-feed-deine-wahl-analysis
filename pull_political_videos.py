import os
import argparse
from dotenv import load_dotenv
from utils.utils import get_pol_videos

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Pull political videos from the API')
    parser.add_argument('--date', help='Filter by date (YYYY-MM-DD)')
    parser.add_argument('--username', help='Filter by username')
    parser.add_argument('--output', default='data/pol_videos.csv', 
                        help='Output file path (default: data/political_videos/pol_videos.csv)')
    args = parser.parse_args()
    
    # Load environment variables
    load_dotenv()
    POLVIDEOS_ENDPOINT = os.getenv('POLVIDEOS_ENDPOINT', None)
    AUTH_TOKEN = os.getenv('AUTH_TOKEN', None)
    
    if not POLVIDEOS_ENDPOINT or not AUTH_TOKEN:
        print("Error: Missing environment variables. Please check your .env file.")
        return
    
    # Fetch the videos using the enhanced function
    df = get_pol_videos(
        endpoint=POLVIDEOS_ENDPOINT, 
        auth_token=AUTH_TOKEN,
        output_file=args.output,
        date=args.date,
        username=args.username
    )
    
    print(f"Data shape: {df.shape}")

if __name__ == "__main__":
    main()