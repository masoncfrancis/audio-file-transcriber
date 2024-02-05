import os
import sys
import argparse
import glob


# Function to handle command line arguments
def handleArguments(inputDir=None, outputDir=None, inputFile=None, outputFile=None):
    
    # Check for valid combinations of input and output
    if (inputDir is None and inputFile is None) or (outputDir is None and outputFile is None):
        print("Error: Either 'input_dir' and 'output_dir' must be provided together, or 'input_file' and 'output_file' must be provided together.")
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
        parser.print_help()
        sys.exit(1)

    # Parse command line arguments
    args = parser.parse_args()

    # Call the function to list files and write to a text file
    handleArguments(args.input_dir, args.output_dir, args.input_file, args.output_file)
