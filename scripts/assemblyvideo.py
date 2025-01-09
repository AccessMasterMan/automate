import os
import json
from moviepy import VideoFileClip, concatenate_videoclips

def assemble_videos_with_transitions(project_name):
    #Define paths
    analysis_file_path = os.path.join(project_name, "output", "raw", "data", "analysis.json")
    video_directory = os.path.join(project_name, "output", "raw", "video")

    # Ensure analysis file exists
    if not os.path.exists(analysis_file_path):
        raise FileNotFoundError(f"The analysis file at {analysis_file_path} does not exist.")

    # Load analysis data
    with open(analysis_file_path, "r") as file:
        analysis_data = json.load(file)

    # Process each part
    for audio_entry in analysis_data["audio_analysis"]["parts"]:
        audio_index = audio_entry["audio_index"]
        output_clips = []

        for part_entry in audio_entry["parts"]:
            part_index = part_entry["part_index"]
            keywords = part_entry["keywords"]
            part_videos_path = os.path.join(video_directory, f"part_{part_index}")

            if not os.path.exists(part_videos_path):
                raise FileNotFoundError(f"Video directory {part_videos_path} not found.")

            video_files = sorted(
                [os.path.join(part_videos_path, file) for file in os.listdir(part_videos_path) if file.endswith(".mp4")]
            )

            for keyword, video_path in zip(keywords, video_files):
                start_time = keyword["start_time"]
                end_time = keyword["end_time"]
                duration = end_time - start_time

                clip = VideoFileClip(video_path)
                clip = clip.with_duration(duration)  # Adjust duration to match timing

                output_clips.append(clip)

        # Concatenate clips for this part
        if output_clips:
            final_video = concatenate_videoclips(output_clips, method="compose")
            output_path = os.path.join(project_name, f"output/raw/video/post_part_{audio_index}.mp4")
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            final_video.write_videofile(output_path, codec="libx264", audio_codec="aac")

# Example usage
# assemble_videos_with_transitions("your_project_name")
