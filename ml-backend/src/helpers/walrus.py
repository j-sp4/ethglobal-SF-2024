import requests
import os
import json
from .logger import logger

def get_file_from_walrus(blob_id: str, save_path: str):
    walrus_aggregator = os.getenv("WALRUS_AGGREGATOR")
    url = f"{walrus_aggregator}/v1/{blob_id}"
    response = requests.get(url)
    
    if response.status_code == 200:
        with open(save_path, 'wb') as file:
            file.write(response.content)
    else:
        raise Exception(f"Failed to download file: {response.status_code}, {response.text}")

def upload_file_to_walrus(filepath: str):
    walrus_publisher = os.getenv("WALRUS_PUBLISHER")
    url = f"{walrus_publisher}/v1/store"
    with open(filepath, 'rb') as file:
        response = requests.put(url, files={'file': file})
        logger.debug(f"Uploaded file to Walrus with response: {response}")
    try:
        # Parse the JSON response
        response_data = response.json()  # Use response.json() for direct parsing
        logger.debug(f"Response JSON: {response_data}")
    except json.JSONDecodeError as e:
        raise Exception(f"Failed to parse JSON response: {e}, Response text: {response.text}")
    
    # Extract and return the blobId
    blob_id = response_data.get("newlyCreated", {}).get("blobObject", {}).get("blobId")
    if blob_id is None:
        raise Exception("Blob ID not found in response")
    return blob_id
