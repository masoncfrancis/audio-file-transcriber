import os
import sys
import argparse

def list_files(input_dir, output_dir):
    # Check if the input directory exists
    if not os.path.exists(input_dir):
        print(f"Error: Input directory '{input_dir}' does not exist.")
        sys.exit(1)

    # TODO finish this

if __name__ == "__main__":
    # Set up command line argument parser
    parser = argparse.ArgumentParser(description="List files in a directory and output to a text file.")
    parser.add_argument('-i', '--input', help='Input directory path', required=True)
    parser.add_argument('-o', '--output', help='Output directory path', required=True)
    args = parser.parse_args()

    # Call the function to list files and write to a text file
    list_files(args.input, args.output)
