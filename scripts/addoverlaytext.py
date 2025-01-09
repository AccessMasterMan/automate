from moviepy import *
from moviepy.video.VideoClip import TextClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
from moviepy.video.io.VideoFileClip import VideoFileClip
import os
import json

def create_overlay_text_design(text, duration, video_size):
    """
    Creates a TextClip overlay with a specified design.

    :param text: The text to overlay.
    :param duration: Duration of the overlay in seconds.
    :param video_size: Tuple of video width and height.
    :return: A TextClip object with the overlay design.
    """
    try:
        print(f"Debug: Creating TextClip with text='{text}', duration={duration}, video_size={video_size}")
        text_clip = TextClip(
            text=text,
            font="/workspaces/automate/assets/migaebold.otf",  # Use the correct path or name for your font file
            font_size=80,
            color="white",
            stroke_color="black",
            stroke_width=2,
            method="caption",
            size=(int(video_size[0] * 0.8), None),  # Width is 80% of video width
            text_align="left",
            horizontal_align="left",
            vertical_align="bottom",
            duration=duration,  # Set the duration directly in the TextClip constructor
            margin=(90, 800)
        )

        return text_clip
    except Exception as e:
        print(f"Debug: Exception encountered in create_overlay_text_design: {e}")
        raise RuntimeError(f"Error creating TextClip: {e}")

def add_overlay_text_to_video(video_path, overlay_text, text_duration):
    """
    Adds overlay text to the beginning of a video with animations.

    :param video_path: Path to the video file.
    :param overlay_text: The text to overlay.
    :param text_duration: Duration of the overlay text in seconds.
    :return: A CompositeVideoClip object with the overlay text applied.
    """
    try:
        print(f"Debug: Adding overlay to video: {video_path}, overlay_text='{overlay_text}', text_duration={text_duration}")
        video = VideoFileClip(video_path)
        print(f"Debug: Video loaded. Size: {video.size}")
        text_clip = create_overlay_text_design(overlay_text, text_duration, video.size)


        # Define the entry animation
        #text_clip = text_clip.with_position(lambda t: (90, video.size[1] - 100 + 200 * (1 - min(t / 0.5, 1))))

        # Fade out animation
        text_clip = text_clip.with_effects([vfx.CrossFadeIn(1), vfx.CrossFadeOut(1)])

        final_video = CompositeVideoClip([video, text_clip])
        return final_video
    except Exception as e:
        print(f"Debug: Exception encountered in add_overlay_text_to_video: {e}")
        raise RuntimeError(f"Error adding overlay text to video: {e}")

def process_videos_with_overlay(project_name):
    """
    Processes all merged videos in a project directory and adds overlay text based on metadata.

    :param project_name: Name of the project folder.
    """
    try:
        print(f"Debug: Processing videos for project: {project_name}")
        data_file = os.path.join(project_name, "output", "raw", "data", "engine.json")
        processed_path = os.path.join(project_name, "output", "semifinal")

        if not os.path.exists(data_file):
            print(f"Debug: Metadata file not found at {data_file}")
            raise FileNotFoundError(f"Metadata file {data_file} not found.")

        with open(data_file, "r") as f:
            data = json.load(f)

        for i, part in enumerate(data.get("parts", []), start=1):
            video_file = os.path.join(processed_path, f"merged_part_{i}.mp4")
            output_file = os.path.join(processed_path, f"final_part_{i}.mp4")

            if not os.path.exists(video_file):
                print(f"Debug: Video file not found at {video_file}")
                raise FileNotFoundError(f"Video file {video_file} not found.")

            overlay_text = part.get("text_overlay", "No overlay text provided")
            print(f"Debug: Processing video: {video_file}, overlay_text='{overlay_text}'")
            final_video = add_overlay_text_to_video(video_file, overlay_text, text_duration=3.5)

            print(f"Debug: Writing final video to: {output_file}")
            final_video.write_videofile(output_file, codec="libx264", audio_codec="aac")
            print(f"Debug: Processed video with overlay saved to {output_file}")

    except Exception as e:
        print(f"Debug: Exception encountered in process_videos_with_overlay: {e}")
        raise RuntimeError(f"Error processing videos with overlay: {e}")

# Example usage
# process_videos_with_overlay("your_project_name")
