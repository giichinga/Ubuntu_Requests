import os
import requests
from urllib.parse import urlparse
from datetime import datetime

def fetch_image():
    # Prompt user for an image URL
    url = input("Enter the image URL: ").strip()

    # Directory to save images
    save_dir = "Fetched_Images"
    os.makedirs(save_dir, exist_ok=True)

    try:
        # Fetch the image with streaming enabled
        response = requests.get(url, stream=True, timeout=10)
        response.raise_for_status()  # Raise an error for bad HTTP responses

        # Extract filename from URL if possible
        parsed_url = urlparse(url)
        filename = os.path.basename(parsed_url.path)

        if not filename:  # If URL doesn't end with a filename
            # Generate a unique filename
            filename = f"image_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"

        filepath = os.path.join(save_dir, filename)

        # Save image in binary mode
        with open(filepath, "wb") as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)

        print(f"✅ Image saved successfully as {filepath}")

    except requests.exceptions.MissingSchema:
        print("❌ Invalid URL. Please include http:// or https://")
    except requests.exceptions.ConnectionError:
        print("❌ Connection error. Please check your internet connection or URL.")
    except requests.exceptions.Timeout:
        print("❌ Request timed out. The server may be too slow or unresponsive.")
    except requests.exceptions.HTTPError as http_err:
        print(f"❌ HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"❌ An unexpected error occurred: {err}")

if __name__ == "__main__":
    fetch_image()

