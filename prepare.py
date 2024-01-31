import subprocess
import shutil
import os
import sys
import platform

def is_git_installed():
    return shutil.which('git') is not None

def clone_repository(repo_url, destination_folder):
    print("\nGetting whisper.cpp from GitHub...\n")

    # Remove existing whisper.cpp folder if it exists
    if os.path.exists(destination_folder):
        print("Removing existing whisper.cpp folder...")
        shutil.rmtree(destination_folder)

    try:
        subprocess.run(['git', 'clone', repo_url, destination_folder], check=True)
        print(f"Repository cloned successfully to '{destination_folder}'")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        sys.exit()

if __name__ == "__main__":

    # Describe what the script is going to do and ask for confirmation
    print("This script will set up the environment for journal transcription.")
    print("Note: ffmpeg will be installed. If you don't want that, please do not continue. ")
    print("\nWould you like to continue? (y/n)")
    response = input()

    if response.lower() != 'y': # Exit if the user does not confirm
        print("Exiting...")
        sys.exit()

    # Continue with the script upon confirmation

    if not is_git_installed():
        print("\nGit is not installed. Please install Git and try again.")
        sys.exit()
    else:
        # Get the directory where the script is located
        script_directory = os.path.dirname(os.path.abspath(__file__))

        # Use the script directory as the destination folder
        destination_folder = script_directory + "/whisper.cpp"

        repo_url = 'https://github.com/ggerganov/whisper.cpp'

        clone_repository(repo_url, destination_folder)

        # Change the working directory to the destination folder
        os.chdir(destination_folder)

        # Build whisper.cpp
        print("\nBuilding whisper.cpp using make...\n")
        try:
            subprocess.run(['make'], check=True)
            print("\nwhisper.cpp built successfully\n")
        except subprocess.CalledProcessError as e:
            print(f"\nError: {e}")
            sys.exit()

        # Change the working directory back to the script directory
        os.chdir(script_directory)

        # Check if ffmpeg is installed
        if shutil.which('ffmpeg') is None:
            print("\nffmpeg is not installed. Please install ffmpeg and try again.")
            sys.exit()
            
