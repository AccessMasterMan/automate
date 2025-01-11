import os
import json
from tqdm import tqdm
import assemblyai as aai

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

    # Process each audio file with a single progress bar
    with tqdm(total=len(parts), desc="Analyzing your audio", unit="file") as progress_bar:
        for part_index, part in enumerate(parts):
            audio_path = audio_files[part_index]  # Map the current part to its corresponding audio file

            # Transcribe the audio file
            transcriber = aai.Transcriber()
            transcript = transcriber.transcribe(audio_path)

            # Check for transcription errors
            if transcript.status == aai.TranscriptStatus.error:
                raise RuntimeError(f"Transcription failed for audio file {audio_path}: {transcript.error}")

            keywords = part.get("video_keywords", [])
            keyword_timestamps = []

            # Search for each keyword in the transcription words
            for keyword in keywords:
                found = False
                for word_data in transcript.words:
                    if word_data.text.lower() == keyword.lower():
                        found = True
                        keyword_timestamps.append({
                            "keyword": keyword,
                            "start_time": word_data.start / 1000,  # Convert ms to seconds
                            "end_time": word_data.end / 1000
                        })
                        break
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

            # Update the progress bar
            progress_bar.update(1)

    # Save analysis data
    with open(output_analysis_path, "w") as analysis_file:
        json.dump(analysis_data, analysis_file, indent=4)

    print(f"Analysis saved to {output_analysis_path}")

# Example usage
# analyze_speech_with_assemblyai("your_project_name")
