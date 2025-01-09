import os
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.audio.AudioClip import CompositeAudioClip

def add_background_music(project_name):
    """
    Adds background music to a final video. If the audio is shorter, it loops to match the video's duration.
    If the audio is longer, it trims to match the video's duration. The background music's volume is reduced.

    :param project_name: Name of the project folder.
    """
    try:
        # Define paths
        video_file = os.path.join(project_name, "output", "final", "final_video.mp4")
        audio_file = os.path.join("scripts", "background_music.mp3")
        output_file = os.path.join(project_name, "output", "final", "final_video_with_music.mp4")

        # Ensure files exist
        if not os.path.exists(video_file):
            raise FileNotFoundError(f"Video file {video_file} not found.")
        if not os.path.exists(audio_file):
            raise FileNotFoundError(f"Audio file {audio_file} not found.")

        # Load the video and audio clips
        video_clip = VideoFileClip(video_file)
        background_audio_clip = AudioFileClip(audio_file)

        # Reduce the volume of the background music
        background_audio_clip = background_audio_clip.with_volume_scaled(0.06)  # Set volume to 20%

        # Get durations
        video_duration = video_clip.duration
        audio_duration = background_audio_clip.duration

        # Adjust the audio duration to match the video
        if audio_duration < video_duration:
            # Loop the audio to match the video duration
            background_audio_clip = background_audio_clip.loop(duration=video_duration)
        elif audio_duration > video_duration:
            # Trim the audio to match the video duration
            background_audio_clip = background_audio_clip.subclipped(0, video_duration)

        # Combine the video's original audio with the background music
        original_audio = video_clip.audio
        composite_audio = CompositeAudioClip([original_audio, background_audio_clip])

        # Set the composite audio to the video
        video_with_audio = video_clip.with_audio(composite_audio)

        # Write the result to a file
        video_with_audio.write_videofile(output_file, codec="libx264", audio_codec="aac")

        print(f"Final video with background music saved to {output_file}")

    except Exception as e:
        print(f"Error adding background music: {e}")
        raise

# Example usage
# add_background_music("my_project")
