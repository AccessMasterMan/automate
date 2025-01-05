
# Importing necessary libraries
import time
from tqdm import tqdm

def get_user_input():
    print("Welcome to the AI YouTube Video Generator!")

    # Step 1: Get the title of the script
    title = input("Enter a title for your video (e.g., 'The Future of AI', 'Top 10 Travel Tips'): ")

    # Step 2: Get the type of script the user wants to generate
    script_type = input("What type of script would you like to generate? (e.g., Educational, Inspirational, Funny): ")

    # Step 3: Get additional notes or context for the script
    additional_notes = input("Provide any additional notes or context for the script (e.g., target audience, tone, specific points to cover): ")

    # Step 4: Get the desired video duration in minutes
    while True:
        try:
            duration_minutes = float(input("How long should the video be? (in minutes): "))
            break
        except ValueError:
            print("Please enter a valid number for the duration.")

    # Step 5: Get tags or keywords related to the video
    print("\nEnter tags or keywords related to the video content. These tags will help generate appropriate scripts and search for relevant videos later.")
    tags = input("Please provide tags, separated by commas (e.g., technology, innovation, AI): ")

    # Step 6: Calculate the approximate word count based on duration
    average_words_per_minute = 150  # Average speaking rate
    estimated_word_count = int(duration_minutes * average_words_per_minute)

    # Step 7: Display the inputs received
    print("\nReviewing your input...")
    for _ in tqdm(range(5), desc="Processing Input", unit="step"):
        time.sleep(0.2)  # Simulate processing time

    print("\nInputs Received:")
    print(f"Title: {title}")
    print(f"Script Type: {script_type}")
    print(f"Additional Notes: {additional_notes}")
    print(f"Video Duration: {duration_minutes} minutes")
    print(f"Estimated Word Count: {estimated_word_count} words")
    print(f"Tags: {tags}")

    # Returning inputs for further processing
    return title, script_type, additional_notes, duration_minutes, tags

