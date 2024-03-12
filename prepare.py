import subprocess
import shutil
import os
import sys


def check_dependencies():
    print("\nChecking dependencies...\n")

    dependenciesInstalled = True

    # Check if git is installed
    if not shutil.which('git') is not None:
        print("Git is not installed.")
        dependenciesInstalled = False

    # Check if ffmpeg is installed
    if not shutil.which('ffmpeg') is not None:
        print("ffmpeg is not installed.")
        dependenciesInstalled = False

    # Check if make is installed
    if not shutil.which('make') is not None:
        print("make is not installed.")
        dependenciesInstalled = False

    if not dependenciesInstalled:
        print("Please install the missing dependencies and run this script again.")
        sys.exit()

    print("All dependencies are installed.")


def clone_repository(repo_url, destination_folder):
    try:
        subprocess.run(['git', 'clone', repo_url,
                       destination_folder], check=True)
        print(f"Repository cloned successfully to '{destination_folder}'")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        sys.exit()


if __name__ == "__main__":
    # Describe what the script is going to do and ask for confirmation
    print("This script will set up the environment for audio file transcription.")
    print("All changes made by this script will be confined to this folder. ")
    print("\nWould you like to continue? (y/n)")
    response = input()

    if response.lower() != 'y':  # Exit if the user does not confirm
        print("Exiting...")
        sys.exit()

    # Check if all dependencies are installed
    check_dependencies()

    # Get the directory where the script is located
    script_directory = os.path.dirname(os.path.abspath(__file__))

    # Use the script directory as the destination folder
    destination_folder = script_directory + "/whisper.cpp"

    print("\nGetting whisper.cpp from GitHub...\n")

    # Remove existing whisper.cpp folder if it exists
    if os.path.exists(destination_folder):
        print("Removing existing whisper.cpp folder...")
        shutil.rmtree(destination_folder)

    repo_url = 'https://github.com/ggerganov/whisper.cpp'

    clone_repository(repo_url, destination_folder)

    # Change the working directory to the destination folder
    os.chdir(destination_folder)

    # Build whisper.cpp
    print("\nBuilding whisper.cpp using make...\n")
    try:
        subprocess.run(['make'], check=True)
        print("\nwhisper.cpp built successfully\n")

        print("Downloading AI model...\n")
        subprocess.run(['bash', './models/download-ggml-model.sh', 'base.en'])
        print("\nAI model downloaded successfully\n")

    except subprocess.CalledProcessError as e:
        print(f"\nError: {e}")
        sys.exit()

    # Change the working directory back to the script directory
    os.chdir(script_directory)

    # All done
    print("Environment setup complete.")
