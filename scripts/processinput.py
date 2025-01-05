import time
from tqdm import tqdm

# Part 2: Processing User Input
# Placeholder for further processing

def process_user_input(title, script_type, additional_notes, duration_minutes, tags):
    text_prompt = f"""You are a video script generator. Your output must strictly follow the JSON format below.

    Video Title: "{title}"
    Video Type : {script_type}
    Video Duration: approximately {duration_minutes}  minutes stritly  
    Video Tag : {tags}
    Structure:
    The script should be divided into multiple parts. Each part must contain:


    text_data: The story or content (divided into segements).
    video_keywords: A list of 2 or 3 relevant keywords for each part. Ensure the keywords are distinct and not overly repetitive.
    visual_cue: Description of the scene that aligns with the text (consider specifying a style: e.g., minimalist, real footage, etc.).
    text_overlay (optional): Use only when necessary to highlight important points, such as list items (e.g., "Lagos" in "Top Ten Cities to Visit").
    transition: Description of the transition between scenes. Consider using consistent transitions (e.g., all fades, all slides) unless variation is necessary for flow.
    cta (optional): A call to action for audience engagement. This may be used at any point, not just the final part.
    The video_tags section must include up to 3 relevant and specific tags.

    Ensure the response is in valid JSON format without any extra text outside the JSON object.

    Example Response:
    json
    Copy code
    {{
    "video_title": "{title}",
    "video_length": "{duration_minutes} minute",
    "background_music": "Calm, reflective instrumental music",
    "narration_tone": "Calm and introspective",
    "visual_style": "Real-life footage with subtle animations",
    "parts": [
        {{
        "text_data": "I hate how I can’t let go of past mistakes. They linger in my mind and hold me back.",
        "video_keywords": ["regret", "mistakes", "self-doubt"],
        "visual_cue": "A person gazing at a mirror with a disappointed expression, reflecting on past mistakes.",
        "text_overlay": "I can't let go of past mistakes",
        "transition": "fade"
        }},
        {{
        "text_data": "I’m often too hard on myself, expecting perfection when I know it’s impossible.",
        "video_keywords": ["self-criticism", "perfectionism", "expectations"],
        "visual_cue": "A person stressing over a task, trying to perfect it.",
        "transition": "slide"
        }},
        {{
        "text_data": "Overthinking every little decision drives me crazy, making even small tasks feel overwhelming.",
        "video_keywords": ["overthinking", "anxiety", "stress"],
        "visual_cue": "A person overwhelmed by choices and unable to focus.",
        "transition": "zoom"
        }},
        {{
        "text_data": "But by facing these flaws, I've learned to accept them and become a better version of myself.",
        "video_keywords": ["acceptance", "growth", "self-improvement"],
        "visual_cue": "A person smiling, relieved, and taking a deep breath, with clarity.",
        "text_overlay": "Become a better version of yourself",
        "transition": "crossfade",
        "cta": "Comment below and share how you embrace imperfection."
        }}
    ],
    "video_tags": ["self-reflection", "personal growth", "embracing flaws"]
    }}
    Important Notes: {additional_notes}

    lastly:::

    The text_overlay field is optional and should only be used when necessary to highlight important elements like list items, key phrases, or subtitles.
    Use distinct video keywords in each section. Avoid repetition to keep the script fresh.
    Consider a consistent visual style (e.g., real-life footage, animation) to match the tone and purpose of the video.
    Transitions should generally be consistent across the video unless there's a narrative reason to vary them.
    Call to action (cta) can be used in any part, not just at the end of the video but shouldn't be too many.
    """

    print(text_prompt)

    print("\nSimulating OpenAI API Request...")
    for _ in tqdm(range(10), desc="Generating AI Script", unit="step"):
        time.sleep(0.3)  # Simulate script generation time

    print("\nAI Script generation is complete!")
    print("\nScript Preview:")
    print(f"--- Title: {title} ---")
    print(f"--- This is a placeholder script for a {script_type} video. ---")
    print(f"Additional Notes: {additional_notes}")
    print(f"Duration: {duration_minutes} minutes")
    print(f"Tags for this video: {tags}")
