import os
import sys
import argparse

def handleArguments(inputDir=None, outputDir=None, inputFile=None, outputFile=None):
    # Check for valid combinations of input and output
    if (inputDir is None and inputFile is None) or (outputDir is None and outputFile is None):
        print("Error: Either 'input_dir' and 'output_dir' must be provided together, or 'input_file' and 'output_file' must be provided together.")
        sys.exit(1)

    # Check for invalid combinations
    if inputDir and outputFile:
        print("Error: 'input_dir' cannot be provided with 'output_file'.")
        sys.exit(1)

    if inputFile and outputDir:
        print("Error: 'input_file' cannot be provided with 'output_dir'.")
        sys.exit(1)

    if inputDir and not os.path.exists(inputDir):
        print(f"Error: Input directory '{inputDir}' does not exist.")
        sys.exit(1)

    if inputFile and not os.path.exists(inputFile):
        print(f"Error: Input file '{inputFile}' does not exist.")
        sys.exit(1)


if __name__ == "__main__":
    # set up parser
    parser = argparse.ArgumentParser(description="List files in a directory and output to a text file.")

    # Define argument groups
    input_group = parser.add_mutually_exclusive_group(required=True)
    output_group = parser.add_mutually_exclusive_group(required=True)

    # Add arguments to groups
    input_group.add_argument('-id', '--input-dir', help='Input directory path')
    input_group.add_argument('-if', '--input-file', help='Input file path')

    output_group.add_argument('-od', '--output-dir', help='Output directory path')
    output_group.add_argument('-of', '--output-file', help='Output file path')

    # Print usage information if no arguments are provided
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    # Parse command line arguments
    args = parser.parse_args()

    # Call the function to list files and write to a text file
    handleArguments(args.input_dir, args.output_dir, args.input_file, args.output_file)
