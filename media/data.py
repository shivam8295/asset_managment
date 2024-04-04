import requests
import pandas as pd
import time

def fetch_all_data(api_url, headers):
    all_data = []

    while api_url:
        try:
            response = requests.get(api_url, headers=headers)
            response.raise_for_status()

            api_data = response.json()

            # Extract the list of profiles from the 'data' key
            profiles = api_data.get('data', [])

            # Add the profiles to the result
            all_data.extend(profiles)

            # Check if there's a next page
            next_page = api_data.get('links', {}).get('next')
            api_url = next_page if next_page else None

            # Introduce a delay to avoid rate limiting
            time.sleep(1)  # Adjust the sleep time as needed

            # Print progress
            print(f"Fetched {len(all_data)} profiles...")

        except requests.exceptions.RequestException as e:
            print(f"Error fetching data from API: {e}")
            break

    return all_data

# Specify the start date in the format YYYY-MM-DD
start_date = '2023-12-04'
url = f'https://a.klaviyo.com/api/profiles/?page[size]=50&since={start_date}'  # Adjust the batch size
headers = {
    'revision': '2022-12-31',
    'Accept': 'application/json',
    'Authorization': 'Klaviyo-API-Key pk_d5e028c1df82e29914b8f4a2f0acd0bff8',
}

try:
    # Fetch all data
    all_data = fetch_all_data(url, headers)

    # Print final progress
    print(f"Total profiles fetched: {len(all_data)}")

    # Define CSV file path
    csv_file_path = 'output.csv'

    # Convert the profiles to a DataFrame
    df = pd.json_normalize(all_data)

    # Write to CSV
    df.to_csv(csv_file_path, index=False)

    print(f"Data written to {csv_file_path} successfully")

except Exception as e:
    print(f"Error: {e}")

