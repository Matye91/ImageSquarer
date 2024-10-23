import os
import csv

def rename_files_based_on_csv(folder_path, csv_path):
    # Check if folder path is valid
    if not os.path.isdir(folder_path):
        print("The provided folder path is not valid.")
        return

    # Open the CSV file
    try:
        with open(csv_path, mode='r', newline='', encoding='utf-8') as csvfile:
            csv_reader = csv.reader(csvfile, delimiter=';')
            
            # Loop through each row in the CSV
            for row in csv_reader:
                # Skip rows that don't have at least two columns
                if len(row) < 2:
                    print(f"Skipping row {row}: not enough columns")
                    continue
                
                old_filename = row[0].strip()  # First column is the current file name
                new_filename = row[1].strip()  # Second column is the new file name
                
                # Create full paths for the old and new file names
                old_file_path = os.path.join(folder_path, old_filename)
                new_file_path = os.path.join(folder_path, new_filename)
                
                # Check if the file with the old name exists
                if os.path.isfile(old_file_path):
                    # Rename the file
                    os.rename(old_file_path, new_file_path)
                    print(f"Renamed {old_filename} to {new_filename}")
                else:
                    print(f"File {old_filename} not found in the folder.")
    
    except FileNotFoundError:
        print(f"The CSV file {csv_path} was not found.")
    except Exception as e:
        print(f"An error occurred while processing the CSV file: {e}")

if __name__ == "__main__":
    # Prompt the user for the folder path
    folder_path = input("Please enter the folder path containing the files: ")
    
    # Prompt the user for the CSV file path
    csv_path = input("Please enter the path to the CSV file: ")
    
    # Process the CSV and rename files
    rename_files_based_on_csv(folder_path, csv_path)
