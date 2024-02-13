import os
import sys
import shutil
import argparse
import glob
import subprocess


def check_dependencies():
    print("\nChecking dependencies...\n")

    dependenciesInstalled = True

    if not os.path.isfile('./whisper.cpp/main'):
        print("\nwhisper.cpp may not be downloaded or built correctly")
        print("Please run prepare.py again to correct this")
        dependenciesInstalled = False

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
        print("\nPlease install the missing dependencies and try again")
        sys.exit()

    print("All dependencies are installed.")


# Function to handle command line arguments
def handleArguments(inputDir=None, outputDir=None, inputFile=None, outputFile=None):
    # Check for valid combinations of input and output
    if (inputDir is None and inputFile is None) or (outputDir is None and outputFile is None):
        print(
            "Error: Either 'input_dir' and 'output_dir' must be provided together, or 'input_file' and 'output_file' must be provided together.")
        sys.exit(1)

    # Check for invalid combinations of input and output
    if inputDir and outputFile:
        print("Error: 'input_dir' cannot be provided with 'output_file'.")
        sys.exit(1)

    # Check for invalid combinations of input and output
    if inputFile and outputDir:
        print("Error: 'input_file' cannot be provided with 'output_dir'.")
        sys.exit(1)

    # Check for valid input directory
    if inputDir and not os.path.exists(inputDir):
        print(f"Error: Input directory '{inputDir}' does not exist.")
        sys.exit(1)

    # Check for valid output file
    if inputFile and not os.path.exists(inputFile):
        print(f"Error: Input file '{inputFile}' does not exist.")
        sys.exit(1)


# Handles the transcription of files in a directory
def processDir(inputDir):
    fileList = getFileList(inputDir)
    for file in fileList:
        processFile(file, file + ".txt")


def processFile(inputFile, outputFile):
    # convert file to appropriate wav format using ffmpeg
    convertedFilePath = convertAudio(inputFile, outputFile)
    transcribeFile(convertedFilePath, outputFile)


# Converts file to audio format needed by whisper.cpp
def convertAudio(inputFile, outputFile):
    print("Preparing audio file " + inputFile + " for transcription")
    command = [
    "ffmpeg",
    "-i", inputFile,
    "-ar", "16000",
    "-ac", "1",
    "-c:a", "pcm_s16le",
    outputFile + ".wav"
    ]

    # Run the command
    subprocess.run(command)
    return outputFile + ".wav"


def transcribeFile(inputFile, outputFile):
    print("Transcribing file...")

    # Get the directory where the script is located
    script_directory = os.path.dirname(os.path.abspath(__file__))

    # Use the script directory to find the whisper.cpp installation
    whisperFolder = script_directory + "/whisper.cpp"
    os.chdir(whisperFolder)

    command = "./main -f " + inputFile + " -otxt -m models/ggml-base.en.bin"
    subprocess.run(command, shell=True)


    # rename the file to specified name
    os.rename(inputFile + ".wav.txt", outputFile)

    # remove the file created by ffmpeg
    os.remove(inputFile + ".wav")

    print("Transcription of " + inputFile + " finished")


# Function to list audio files in the input directory
def getFileList(inputDir):
    # Define audio extensions
    audioExtensions = ['*.mp3', '*.wav', '*.ogg', '*.flac', '*.aiff', '*.aac']

    # List audio files
    files = []
    for ext in audioExtensions:
        for file in glob.glob(os.path.join(inputDir, '**', ext), recursive=True):
            files.append(file)

    return files


if __name__ == "__main__":

    check_dependencies()  # check to make sure dependencies are installed

    # set up parser
    parser = argparse.ArgumentParser(description="Transcribe audio file(s)")

    # Define argument groups
    inputGroup = parser.add_mutually_exclusive_group(required=True)
    outputGroup = parser.add_mutually_exclusive_group(required=True)

    # Add arguments to groups
    inputGroup.add_argument('-id', '--input-dir', help='Input directory path')
    inputGroup.add_argument('-if', '--input-file', help='Input file path')

    outputGroup.add_argument('-od', '--output-dir', help='Output directory path')
    outputGroup.add_argument('-of', '--output-file', help='Output file path')

    # Print usage information if no arguments are provided
    if len(sys.argv) == 1:
        print("\n")
        parser.print_help()
        sys.exit(1)

    # Parse command line arguments
    args = parser.parse_args()

    # Check to make sure arguments are passed in properly
    handleArguments(args.input_dir, args.output_dir, args.input_file, args.output_file)

    # Check if we are working with directories or files
    singleFile = False
    if args.input_file and args.output_file:
        singleFile = True

    if singleFile:
        processFile(args.input_file, args.output_file)
    else:
        processDir(args.input_dir) # TODO implement output file argument
