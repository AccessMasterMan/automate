import os
import json
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.video.fx import Loop

def merge_audio_with_video(project_name):
    """
    Merges audio files with corresponding video files in a project structure.
    Uses project metadata to process all parts of the video.

    :param project_name: Name of the project folder.
    """
    # Define paths based on project_name
    audio_path = os.path.join(project_name, "output", "raw", "audio")
    video_path = os.path.join(project_name, "output", "raw", "video")
    data_file = os.path.join(project_name, "output", "raw", "data", "engine.json")

    # Ensure the paths exist
    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"Audio directory {audio_path} not found.")
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Video directory {video_path} not found.")
    if not os.path.exists(data_file):
        raise FileNotFoundError(f"Data file {data_file} not found.")

    # Load the data file
    with open(data_file, "r") as f:
        data = json.load(f)

    # Process each part
    for i, part in enumerate(data.get("parts", []), start=1):
        audio_file = os.path.join(audio_path, f"part_{i}.mp3")
        video_file = os.path.join(video_path, f"post_part_{i}.mp4")
        output_file = os.path.join(project_name, "output", "semifinal", f"merged_part_{i}.mp4")

        # Ensure files exist
        if not os.path.exists(audio_file):
            raise FileNotFoundError(f"Audio file {audio_file} not found.")
        if not os.path.exists(video_file):
            raise FileNotFoundError(f"Video file {video_file} not found.")

        # Load the video and audio clips
        video_clip = VideoFileClip(video_file)
        audio_clip = AudioFileClip(audio_file)

        # Get the duration of the audio
        audio_duration = audio_clip.duration

        # Adjust the video duration to match the audio
        if video_clip.duration < audio_duration:
            # Loop the video to match the audio duration
            video_clip = Loop(duration=audio_duration).apply(video_clip)

        elif video_clip.duration > audio_duration:
            # Trim the video to match the audio duration
            video_clip = video_clip.subclipped(0, audio_duration)

        # Set the audio to the video
        video_with_audio = video_clip.with_audio(audio_clip)

        # Write the result to a file
        video_with_audio.write_videofile(output_file, codec="libx264", audio_codec="aac")

        print(f"Merged part {i} saved to {output_file}")

# Example usage
# merge_audio_with_video("my_project")