import json
import os
import time
from elevenlabs import ElevenLabs
from tqdm import tqdm

# Initialize ElevenLabs client
client = ElevenLabs(api_key="sk_5fbd740e98e402b04802562e3d7c484feaf3eb7faf03940e")  # Replace with your actual API key

# Load and parse the JSON file
def load_json(file_path):
    with open(file_path, "r") as file:
        return json.load(file)

# Generate and save audio
def generate_audio(text, output_file):
    try:
        audio_generator = client.generate(
            text=text,
            voice="Brian",
            model="eleven_multilingual_v2",
        )
        with open(output_file, "wb") as f:
            for chunk in audio_generator:
                f.write(chunk)
        return True
    except Exception as e:
        print(f"Failed to generate audio for text: {text[:30]}... Error: {e}")
        return False

# Process parts and generate audio
def process_audio(project_name):
    # Define the paths
    data_file_path = os.path.join(project_name, "output", "raw", "data", "engine.json")
    output_directory = os.path.join(project_name, "output", "raw", "audio")

    # Load JSON data
    if not os.path.exists(data_file_path):
        raise FileNotFoundError(f"The JSON file at {data_file_path} does not exist.")
    json_data = load_json(data_file_path)

    # Ensure output directory exists
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    parts = json_data.get("parts", [])
    success = True

    # Initialize progress bar
    with tqdm(total=len(parts), desc="Generating Audio", unit="file") as pbar:
        for index, part in enumerate(parts):
            text_data = part.get("text_data", "")
            cta = part.get("cta", "")
            text_to_convert = text_data + (" " + cta if cta else "")

            if text_to_convert.strip():
                output_file_name = f"part_{index + 1}.mp3"
                output_file_path = os.path.join(output_directory, output_file_name)
                result = generate_audio(text_to_convert, output_file_path)
                if not result:
                    success = False
                time.sleep(1)  # Wait to ensure API stability
                pbar.update(1)

    return success
