import os
from moviepy import VideoFileClip
from tqdm import tqdm

# Define YouTube landscape dimensions
TARGET_WIDTH = 1920
TARGET_HEIGHT = 1080
TARGET_ASPECT_RATIO = TARGET_WIDTH / TARGET_HEIGHT

def resize_and_crop_video(input_path, output_path):
    try:
        clip = VideoFileClip(input_path).without_audio()  # Remove audio from the video
        video_width, video_height = clip.size
        video_aspect_ratio = video_width / video_height

        if video_aspect_ratio > TARGET_ASPECT_RATIO:
            # Video is wider than 16:9, scale height and crop width
            scaled_clip = clip.resized(height=TARGET_HEIGHT)
            new_width = int(TARGET_HEIGHT * video_aspect_ratio)
            x1 = (new_width - TARGET_WIDTH) // 2
            cropped_clip = scaled_clip.cropped(x1=x1, x2=x1 + TARGET_WIDTH)
        elif video_aspect_ratio < TARGET_ASPECT_RATIO:
            # Video is taller than 16:9, scale width and crop height
            scaled_clip = clip.resized(width=TARGET_WIDTH)
            new_height = int(TARGET_WIDTH / video_aspect_ratio)
            y1 = (new_height - TARGET_HEIGHT) // 2
            cropped_clip = scaled_clip.cropped(y1=y1, y2=y1 + TARGET_HEIGHT)
        else:
            # Video already matches 16:9, scale directly
            cropped_clip = clip.resized(width=TARGET_WIDTH, height=TARGET_HEIGHT)

        # Write the output video
        cropped_clip.write_videofile(output_path, codec="libx264", audio_codec="aac")
        clip.close()
        cropped_clip.close()
    except Exception as e:
        print(f"Error processing video {input_path}: {e}")

# Process videos in the "videos" folder
def process_videos_for_youtube(project_name):
    videos_directory = os.path.join(project_name, "output", "raw", "video")

    if not os.path.exists(videos_directory):
        raise FileNotFoundError(f"The directory {videos_directory} does not exist.")

    # Collect all video files
    video_parts = [os.path.join(videos_directory, part) for part in os.listdir(videos_directory) if os.path.isdir(os.path.join(videos_directory, part))]
    all_videos = []
    for part in video_parts:
        videos = [os.path.join(part, video) for video in os.listdir(part) if video.endswith(".mp4")]
        all_videos.extend(videos)

    # Single progress bar for all videos
    with tqdm(total=len(all_videos), desc="Processing Videos", unit="video") as pbar:
        for video_path in all_videos:
            part_directory = os.path.dirname(video_path)
            output_file_path = os.path.join(part_directory, f"resized_{os.path.basename(video_path)}")

            # Resize and crop the video
            resize_and_crop_video(video_path, output_file_path)
            pbar.update(1)

    # Clean up old files and rename
    with tqdm(total=len(all_videos), desc="Cleaning Up Videos", unit="video") as cleanup_pbar:
        for video_path in all_videos:
            resized_path = os.path.join(os.path.dirname(video_path), f"resized_{os.path.basename(video_path)}")

            if os.path.exists(resized_path):
                os.remove(video_path)  # Remove the original file
                new_path = os.path.join(os.path.dirname(video_path), os.path.basename(video_path).replace("resized_", ""))
                os.rename(resized_path, new_path)  # Rename the resized file

            cleanup_pbar.update(1)

# Example usage
# process_videos_for_youtube("your_project_name_here")
