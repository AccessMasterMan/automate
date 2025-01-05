import os
import time
from tqdm import tqdm

from scripts.getinput import get_user_input;
from scripts.processinput import process_user_input;

def display_welcome_screen():
    terminal_art = r"""
 __     ______  ____   _____ _   _ 
 \ \   / / __ \|  _ \ / ____| \ | |
  \ \_/ / |  | | |_) | (___ |  \| |
   \   /| |  | |  _ < \___ \| . ` |
    | | | |__| | |_) |____) | |\  |
    |_|  \____/|____/|_____/|_| \_|
    
    YGen - Your Project Generator
    Programmed by Valentine Emmanuel
    """
    print(terminal_art)

def create_project():
    print("Welcome to the Project Generator!")

    # Step 1: Ask for the project name
    project_name = input("Enter the name of your new project: ").strip()
    
    # Ensure the project name is valid
    if not project_name:
        print("Error: Project name cannot be empty.")
        return
    
    # Step 2: Define the folder structure
    base_path = os.path.join(os.getcwd(), project_name)
    output_path = os.path.join(base_path, "output")
    raw_path = os.path.join(output_path, "raw")
    processed_path = os.path.join(output_path, "processed")
    raw_subfolders = ["script", "audio", "video", "data"]

    # Combine all folders into a single list
    folders_to_create = [base_path, output_path, raw_path, processed_path] + \
                        [os.path.join(raw_path, subfolder) for subfolder in raw_subfolders]

    # Step 3: Create the folder structure with a single progress bar
    print("\nCreating your project...")
    for folder in tqdm(folders_to_create, desc="Progress", unit="folder"):
        os.makedirs(folder, exist_ok=True)
        time.sleep(0.1)  # Simulate folder creation delay

    print("\nProject structure created successfully!")
    print(f"Your project is located at: {base_path}")


def cancel_project():
    print("\nCanceling... Goodbye!")
    time.sleep(1)

def show_menu():
    while True:
        display_welcome_screen()
        print("\nMenu:")
        print("1. Generate a New Project")
        print("2. Cancel and Exit")
        
        choice = input("\nEnter your choice (1-2): ").strip()
        
        if choice == "1":
            create_project()
            title, script_type, additional_notes, duration_minutes, tags = get_user_input()
            process_user_input(title, script_type, additional_notes, duration_minutes, tags)

            
        elif choice == "2":
            cancel_project()
            break
        else:
            print("\nInvalid choice. Please try again.")
            time.sleep(1)
