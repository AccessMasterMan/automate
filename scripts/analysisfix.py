import os
import json

def fix_analysis_timestamps(project_name):
    """
    Fixes the timestamps in the analysis.json file to ensure synchronization with the video.
    """
    # Define file paths
    analysis_file_path = os.path.join(project_name, "output", "raw", "data", "analysis.json")
    audio_directory = os.path.join(project_name, "output", "raw", "audio")

    # Ensure analysis file exists
    if not os.path.exists(analysis_file_path):
        raise FileNotFoundError(f"The JSON file at {analysis_file_path} does not exist.")

    # Load analysis data
    with open(analysis_file_path, "r") as file:
        analysis_data = json.load(file)

    audio_analysis = analysis_data.get("audio_analysis", {}).get("parts", [])

    # Collect all audio files
    audio_files = [
        os.path.join(audio_directory, audio)
        for audio in os.listdir(audio_directory)
        if audio.endswith(".mp3") or audio.endswith(".wav")
    ]

    if not audio_files:
        raise FileNotFoundError("No audio files found in the audio directory.")

    # Ensure correct number of audio files match parts
    if len(audio_files) != len(audio_analysis):
        raise ValueError("Mismatch between number of audio files and analysis parts.")

    for audio_index, (audio_path, audio_part) in enumerate(zip(audio_files, audio_analysis)):
        # Get the audio duration (using pydub or similar library)
        from pydub.utils import mediainfo

        audio_info = mediainfo(audio_path)
        audio_duration = float(audio_info["duration"])

        for part in audio_part.get("parts", []):
            keywords = part.get("keywords", [])
            if not keywords:
                continue

            # Fix null timestamps and ensure correct synchronization
            for i, keyword_data in enumerate(keywords):
                if i == 0:
                    # Set the first keyword start_time to 0.0
                    keyword_data["start_time"] = 0.0

                # Handle end_time of the current keyword
                if i < len(keywords) - 1:
                    next_start_time = keywords[i + 1]["start_time"]
                    keyword_data["end_time"] = next_start_time
                else:
                    # Last keyword spans to the end of the audio
                    keyword_data["end_time"] = audio_duration

            # Handle null entries or missing keywords
            for keyword_data in keywords:
                if keyword_data["start_time"] is None or keyword_data["end_time"] is None:
                    num_keywords = len(keywords)
                    if num_keywords > 1:
                        intervals = audio_duration / num_keywords
                        for j, keyword in enumerate(keywords):
                            keyword["start_time"] = round(j * intervals, 3)
                            keyword["end_time"] = round((j + 1) * intervals, 3)
                    else:
                        keyword_data["start_time"] = 0.0
                        keyword_data["end_time"] = audio_duration

    # Save fixed analysis data
    with open(analysis_file_path, "w") as analysis_file:
        json.dump(analysis_data, analysis_file, indent=4)

    print(f"Fixed analysis data saved to {analysis_file_path}")

# Example usage
# fix_analysis_timestamps("your_project_name")
