from openai import OpenAI
import json
import os

# Initialize the OpenAI client
def initialize_client():
    """Load the OpenAI client with the API key."""
    config_path = os.path.join(os.path.dirname(__file__), "../configure/api_keys.json")
    config_path = os.path.normpath(config_path)

    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Configuration file not found at {config_path}")

    with open(config_path, "r") as file:
        config = json.load(file)
        api_key = config.get("openai_api_key")
        if not api_key:
            raise ValueError("OpenAI API key not found in configuration file.")

    return OpenAI(api_key=api_key)


def generate_storyline(topic, max_tokens=100):
    """Generate a storyline based on the input topic."""
    client = initialize_client()

    try:
        print(f"Generating storyline for topic: {topic}")
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "developer",
                    "content": (
                        "You are a creative assistant. Write an engaging and detailed storyline or narrative for a "
                        f"YouTube video about '{topic}'. The tone should be informative and captivating, with clear "
                        "historical facts and intriguing insights."
                    ),
                },
                {
                    "role": "user",
                    "content": topic,
                },
            ],
            max_tokens=max_tokens,
            temperature=0.7,
        )
        storyline = completion.choices[0].message["content"].strip()
        return storyline
    except Exception as e:
        print(f"Error generating storyline: {e}")
        return None


def save_storyline(storyline, output_path="output/storyline.txt"):
    """Save the generated storyline to a file."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w") as file:
        file.write(storyline)
    print(f"Storyline successfully saved to {output_path}.")
