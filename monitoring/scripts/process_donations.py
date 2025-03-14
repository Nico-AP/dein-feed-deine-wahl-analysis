import os
import json
import pandas as pd
import glob
from tqdm import tqdm
import argparse
from monitoring.utils.utils import json_to_df

def process_donation_file(json_path, output_dir):
    """
    Process a single donation JSON file and convert it to CSV.
    
    Parameters:
    -----------
    json_path : str
        Path to the JSON file
    output_dir : str
        Directory to save the CSV file
    
    Returns:
    --------
    bool
        True if successful, False otherwise
    """
    try:
        # Extract participant ID from filename
        filename = os.path.basename(json_path)
        participant_id = filename.split('.')[0]
        
        # Read the JSON file
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Create a combined DataFrame with all activity types
        try:
            combined_df = json_to_df(data)
            
            # Add participant ID column
            combined_df['participant_id'] = participant_id
            
            # Create output filename
            output_filename = f"{participant_id}_activities.csv"
            output_path = os.path.join(output_dir, output_filename)
            
            # Save to CSV
            combined_df.to_csv(output_path, index=False)
            
            return True
            
        except Exception as e:
            # Handle other errors in the JSON processing
            print(f"Warning: Error processing {json_path}: {str(e)}")
            return False
            
    except Exception as e:
        print(f"Error processing {json_path}: {str(e)}")
        return False

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Process donation JSON files to CSV')
    parser.add_argument('--input_dir', default='data/donations', 
                        help='Directory containing donation JSON files (default: data/donations)')
    parser.add_argument('--output_dir', default='data/donations_as_csv', 
                        help='Directory to save processed CSV files (default: data/donations_as_csv)')
    parser.add_argument('--overview_file', default='data/overview/usable_overview.csv',
                        help='Path to usable_overview.csv file (default: data/overview/usable_overview.csv)')
    args = parser.parse_args()
    
    # Create output directory if it doesn't exist
    os.makedirs(args.output_dir, exist_ok=True)
    
    # Load the usable_overview.csv file to get valid participant IDs
    try:
        usable_df = pd.read_csv(args.overview_file)
        valid_participant_ids = set(usable_df['participant_id'].astype(str))
        print(f"Loaded {len(valid_participant_ids)} valid participant IDs from {args.overview_file}")
    except Exception as e:
        print(f"Error loading overview file: {str(e)}")
        return
    
    # Get list of all JSON files in the donations directory
    all_json_files = glob.glob(os.path.join(args.input_dir, '*.json'))
    
    if not all_json_files:
        print(f"No JSON files found in {args.input_dir}")
        return
    
    # Filter JSON files to only include those with valid participant IDs
    json_files = []
    for json_file in all_json_files:
        filename = os.path.basename(json_file)
        participant_id = filename.split('.')[0]
        if participant_id in valid_participant_ids:
            json_files.append(json_file)
    
    print(f"Found {len(json_files)} donation files to process out of {len(all_json_files)} total files")
    
    # Process each file with a progress bar
    successful = 0
    failed = 0
    
    for json_file in tqdm(json_files, desc="Processing donations"):
        if process_donation_file(json_file, args.output_dir):
            successful += 1
        else:
            failed += 1
    
    print(f"Processing complete: {successful} successful, {failed} failed")
    print(f"CSV files saved to {args.output_dir}")

if __name__ == "__main__":
    main()
