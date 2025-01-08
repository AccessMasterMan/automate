import os
import requests
from tqdm import tqdm
import json

# Pexels API key
PEXELS_API_KEY = "QzYiai5SAMXPcmL7gqWVYCOuR5WgaKAozlVakVomBP6SrXl2efOx0v8y"   # Replace with your actual Pexels API key

# Define the acceptable range for landscape videos (YouTube aspect sratio: ~16:9)
ACCEPTABLE_ASPECT_RATIO = (1.7, 1.9)  # Approximate range for 16:9
MIN_WIDTH = 1280
MIN_HEIGHT = 720
MAX_VIDEO_SIZE_MB = 20  # Maximum video file size in MB

# Search Pexels for videos
def search_pexels_video(keyword):
    try:
        headers = {"Authorization": PEXELS_API_KEY}
        params = {"query": keyword, "per_page": 10}  # Fetch multiple results to find the best match
        response = requests.get("https://api.pexels.com/videos/search", headers=headers, params=params)
        response.raise_for_status()
        results = response.json()

        if results.get("videos"):
            for video in results["videos"]:
                for file in video.get("video_files", []):
                    width = file.get("width", 0)
                    height = file.get("height", 0)
                    aspect_ratio = width / height if height > 0 else 0
                    file_size_mb = file.get("file_size", 0) / (1024 * 1024)  # Convert bytes to MB

                    # Check if the video matches our desired dimensions, aspect ratio, is HD, and is within size limit
                    if (
                        file.get("quality") == "hd" and
                        MIN_WIDTH <= width and MIN_HEIGHT <= height and
                        ACCEPTABLE_ASPECT_RATIO[0] <= aspect_ratio <= ACCEPTABLE_ASPECT_RATIO[1] and
                        file_size_mb <= MAX_VIDEO_SIZE_MB
                    ):
                        return file["link"]
            print(f"No suitable videos found for keyword: {keyword}")
            return None
        else:
            print(f"No videos found for keyword: {keyword}")
            return None
    except Exception as e:
        print(f"Error searching Pexels for keyword {keyword}: {e}")
        return None

# Download video from URL
def download_video(url, output_file):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        with open(output_file, "wb") as f:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
    except Exception as e:
        print(f"Failed to download video from {url}. Error: {e}")

# Process parts and fetch videos
def process_video_parts(project_name):
    # Define paths
    data_file_path = os.path.join(project_name, "output", "raw", "data", "engine.json")
    videos_directory = os.path.join(project_name, "output", "raw", "video")

    # Load JSON data
    if not os.path.exists(data_file_path):
        raise FileNotFoundError(f"The JSON file at {data_file_path} does not exist.")
    
    with open(data_file_path, "r") as file:
        json_data = json.load(file)

    # Ensure videos directory exists
    if not os.path.exists(videos_directory):
        os.makedirs(videos_directory)

    parts = json_data.get("parts", [])
    success = True

    # Initialize progress bar
    total_keywords = sum(len(part.get("video_keywords", [])) for part in parts)
    with tqdm(total=total_keywords, desc="Fetching Videos", unit="video") as pbar:
        for index, part in enumerate(parts):
            video_keywords = part.get("video_keywords", [])
            part_directory = os.path.join(videos_directory, f"part_{index + 1}")
            if not os.path.exists(part_directory):
                os.makedirs(part_directory)

            if video_keywords:
                for i, keyword in enumerate(video_keywords):
                    video_url = search_pexels_video(keyword)
                    if video_url:
                        output_file_path = os.path.join(part_directory, f"video_{i + 1}.mp4")
                        download_video(video_url, output_file_path)
                    else:
                        success = False
                    pbar.update(1)
            else:
                print(f"No keywords found for part {index + 1}")
                success = False

    return success
