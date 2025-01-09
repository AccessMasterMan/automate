import os
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy import VideoFileClip, concatenate_videoclips, vfx


def combine_final_clips(project_name):
    """
    Combines all final clips into a single video with transitions and saves it to the output folder.

    :param project_name: Name of the project folder.
    """
    try:
        print(f"Debug: Combining final clips for project: {project_name}")

        # Define paths
        semifinal_path = os.path.join(project_name, "output", "semifinal")
        output_path = os.path.join(project_name, "output", "final", "final_video.mp4")

        if not os.path.exists(semifinal_path):
            raise FileNotFoundError(f"Semifinal path {semifinal_path} does not exist.")

        # Gather all "final_part" clips
        final_clips = []
        for file_name in sorted(os.listdir(semifinal_path)):
            if file_name.startswith("final_part") and file_name.endswith(".mp4"):
                clip_path = os.path.join(semifinal_path, file_name)
                print(f"Debug: Adding clip to combine: {clip_path}")

                clip = VideoFileClip(clip_path)

                # Apply fade transitions
                #faded_clip = FadeIn(FadeOut(clip, 1), 1)  # 1-second fade-in and fade-out
                 # Apply fade transitions
                clip = clip.with_effects([vfx.FadeIn(0.7), vfx.CrossFadeOut(0.7)])
                #clip = FadeOut(1)  # 1-second fade-out
                final_clips.append(clip)

        if not final_clips:
            raise ValueError("No final clips found to combine.")

        # Concatenate clips with compose method
        print("Debug: Concatenating clips...")
        final_video = concatenate_videoclips(final_clips, method="compose")

        # Ensure the output directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        # Write the combined video to output
        print(f"Debug: Writing final combined video to: {output_path}")
        final_video.write_videofile(output_path, codec="libx264", audio_codec="aac")

        print(f"Debug: Final video saved to {output_path}")

    except Exception as e:
        print(f"Debug: Exception encountered in combine_final_clips_with_transitions: {e}")
        raise RuntimeError(f"Error combining final clips: {e}")

# Example usage
# combine_final_clips_with_transitions("your_project_name")
