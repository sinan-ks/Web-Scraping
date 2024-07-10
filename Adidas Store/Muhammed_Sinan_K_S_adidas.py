import requests
import jsonlines
import time

API_URL = 'https://www.adidas.co.th/api/stores?sitePath=en&latitude=13.736717&longitude=100.523186&type=4'

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
    'Accept': 'application/json',
    'Content-Type': 'application/json',
}

def fetch_store_data(max_retries=3):
    retries = 0
    while retries < max_retries:
        try:
            response = requests.get(API_URL, headers=HEADERS, timeout=30)
            response.raise_for_status()
            data = response.json()
            print(data)  # Print the entire data
            stores = data.get('content', [])
            if stores:
                return stores
            else:
                print(f"No stores found in API response. Response: {data}")
                return []
        except requests.exceptions.RequestException as e:
            retries += 1
            if retries < max_retries:
                print(f"Error fetching data (Attempt {retries}/{max_retries}): {e}")
                time.sleep(5)  # Wait for 5 seconds before retrying
            else:
                print(f"Error fetching data after {max_retries} attempts: {e}")
    return []

def save_to_jsonl(store_data, filename):
    with jsonlines.open(filename, mode='w') as writer:
        writer.write_all(store_data)

def main():
    store_data = fetch_store_data()
    if store_data:
        filename = 'Muhammed_Sinan_K_S_adidas_stores.jsonl'
        save_to_jsonl(store_data, filename)
        print(f"Data successfully saved to {filename}")
    else:
        print("No store data fetched. Check logs for details.")

if __name__ == '__main__':
    main()