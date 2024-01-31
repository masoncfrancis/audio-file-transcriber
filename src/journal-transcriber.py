import os
import sys
import argparse

def list_files(input_dir, output_dir):
    # Check if the input directory exists
    if not os.path.exists(input_dir):
        print(f"Error: Input directory '{input_dir}' does not exist.")
        sys.exit(1)

    # Get the list of files in the input directory
    files = os.listdir(input_dir)

    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Generate the output file path
    output_file_path = os.path.join(output_dir, "file_list.txt")

    # Write the list of files to the output file
    with open(output_file_path, "w") as output_file:
        for file in files:
            output_file.write(file + "\n")

    print(f"File list has been written to '{output_file_path}'.")

if __name__ == "__main__":
    # Set up command line argument parser
    parser = argparse.ArgumentParser(description="List files in a directory and output to a text file.")
    parser.add_argument('-i', '--input', help='Input directory path', required=True)
    parser.add_argument('-o', '--output', help='Output directory path', required=True)
    args = parser.parse_args()

    # Call the function to list files and write to a text file
    list_files(args.input, args.output)
