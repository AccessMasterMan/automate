import os
import json
from tqdm import tqdm
import assemblyai as aai

# Set AssemblyAI API key
aai.settings.api_key = "f35f8619ff924afeace793906eff2327"  # Replace with your AssemblyAI API key

# Define paths
ENGINE_FILE = "engine.json"
ANALYSIS_FILE = "analysis.json"

def analyze_speech_with_assemblyai(project_name):
    # Define file paths
    data_file_path = os.path.join(project_name, "output", "raw", "data", ENGINE_FILE)
    output_analysis_path = os.path.join(project_name, "output", "raw", "data", ANALYSIS_FILE)
    audio_directory = os.path.join(project_name, "output", "raw", "audio")

    # Ensure data file exists
    if not os.path.exists(data_file_path):
        raise FileNotFoundError(f"The JSON file at {data_file_path} does not exist.")

    # Load engine data
    with open(data_file_path, "r") as file:
        engine_data = json.load(file)

    parts = engine_data.get("parts", [])

    if not os.path.exists(audio_directory):
        raise FileNotFoundError(f"Audio directory {audio_directory} not found.")

    # Initialize analysis structure
    analysis_data = {"audio_analysis": {"parts": []}}

    # Collect all audio files
    audio_files = [
        os.path.join(audio_directory, audio) for audio in os.listdir(audio_directory) if audio.endswith(".mp3") or audio.endswith(".wav")
    ]

    # Ensure correct mapping of audio files to parts
    if len(audio_files) != len(parts):
        raise ValueError("The number of audio files does not match the number of parts in the engine data.")

    # Process each audio file
    for part_index, part in enumerate(tqdm(parts, desc="Processing Parts", unit="part")):
        audio_path = audio_files[part_index]  # Map the current part to its corresponding audio file

        # Configure AssemblyAI transcription with auto_highlights enabled
        config = aai.TranscriptionConfig(auto_highlights=True)

        # Transcribe the audio file
        transcript = aai.Transcriber().transcribe(audio_path, config)

        keywords = part.get("video_keywords", [])
        keyword_timestamps = []

        # Search for each keyword in the transcription highlights
        for keyword in keywords:
            found = False
            for result in transcript.auto_highlights.results:
                if result.text.lower() == keyword.lower():
                    found = True
                    for timestamp in result.timestamps:
                        start_time = timestamp.start / 1000  # Convert ms to seconds
                        end_time = timestamp.end / 1000
                        keyword_timestamps.append({
                            "keyword": result.text,
                            "start_time": start_time,
                            "end_time": end_time
                        })

            if not found:
                keyword_timestamps.append({
                    "keyword": keyword,
                    "start_time": None,
                    "end_time": None
                })

        # Append part analysis
        analysis_data["audio_analysis"]["parts"].append({
            "audio_index": part_index + 1,
            "parts": [{
                "part_index": part_index + 1,
                "keywords": keyword_timestamps
            }]
        })

    # Save analysis data
    with open(output_analysis_path, "w") as analysis_file:
        json.dump(analysis_data, analysis_file, indent=4)

    print(f"Analysis saved to {output_analysis_path}")

# Example usage
# analyze_speech_with_assemblyai("your_project_name")
