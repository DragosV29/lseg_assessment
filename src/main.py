import os
import logging
import shutil
from logging_config import setup_logging
from check_directory import check_directory_recursively
from validate_csv import is_valid_csv
from process_files import read_lines_from_csv_as_feed
from process_files import consume_feed_and_write_to_csv

def main(directory, valid_output_file, invalid_output_file): #Main function to orchestrate the scripts
    
    setup_logging()
    logging.info("Begin processing...")

    check_directory_recursively(directory, valid_output_file, invalid_output_file)
    logging.info("csv validation complete...")

    logging.info("starting to process the csv files...")

    "Process each file listed in the valid_output_file by directory"
    #keep files grouped by directory
    files_by_directory = {}

    #Read file paths and organize them by directory
    with open(valid_output_file, 'r', newline='', encoding='utf-8') as v_file:
        file_paths = [line.strip() for line in v_file]
    
    for file_path in file_paths:
        file_path = file_path.strip() #remove whitespaces/newlines
        if os.path.isfile(file_path):
            directory = os.path.dirname(file_path)
            if directory not in files_by_directory:
                files_by_directory[directory] = []
            files_by_directory[directory].append(file_path)

        main_dir = os.path.abspath(os.path.join(os.getcwd(), '..'))
        processed_dir_path = os.path.join(main_dir, "stock_price_data_files_processed")
        if  os.path.exists(processed_dir_path):
            shutil.rmtree(processed_dir_path)

    #Process each directory
    for directory, files in files_by_directory.items():
        num_files = len(files)
        logging.info(f"\nDirectory: {directory}")
        logging.info(f"Number of files found: {num_files}")

        #Ask the user for the number of files to process
        while True:
            print("")
            parts = directory.split('/')
            dir_name=parts[-1]

            user_input = input(f"{num_files} file(s) in {dir_name}. How many files would you like to process ? (1 or 2) \n")
            if user_input.isdigit() and int(user_input) in [1, 2]:
                num_to_process = int(user_input)
                random_number=""

                if num_to_process > num_files:
                    print(f"Warning: You requested to process {num_to_process} files, but there is only {num_files} valid file available.")
                    print(f"Info: Processing {num_files} valid file available.")
                    logging.warning(f"You requested to process {num_to_process} files, but there is only {num_files} valid file available.")
                    logging.info(f"Processing {num_files} valid file available.")

                elif num_to_process < num_files:
                    print(f"Info: You requested to process {num_to_process} file, and there are {num_files} valid files available.")
                    print("Info: Processing all files available.")
                    logging.info(f"You requested to process {num_to_process} file, and there are {num_files} valid files available.")
                    logging.info("Processing all files available.")


                else: 
                    print(f"Info: You requested to process {num_to_process} file(s), out of {num_files} valid file(s) available.")
                    print("Info: Processing valid files.")
                    logging.info(f"You requested to process {num_to_process} file(s), out of {num_files} valid file(s) available.")
                    logging.info("Processing valid files.")

                for i in range(num_files):
                    input_file = files[i] #Get the file path
                    output_file_name = (input_file.split('/'))[-1]
                    write_dir_name = f"stock_price_data_files_processed/{dir_name}"
                    write_dir_path = os.path.join(main_dir, write_dir_name)
                    output_file_path = os.path.join(write_dir_path, output_file_name)

                    if not os.path.exists(write_dir_path):
                        os.makedirs(write_dir_path)
                    feed=read_lines_from_csv_as_feed(input_file, num_lines=30)
                    consume_feed_and_write_to_csv(feed, output_file_path)
                    if not os.listdir(write_dir_path):
                        os.rmdir(write_dir_path)

                break #exit after processing all available files

            else:
                #Process the requested number of files
                print(f"Warning: Invalid input. There is only {num_files} in the directory. Input must be {num_files}")
                logging.warning(f"Warning: Invalid input. There is only {num_files} in the directory. Input must be {num_files}")



if __name__ == "__main__" :
    dir_name="output"
    main_dir= os.path.abspath(os.path.join(os.getcwd(), ".."))
    new_dir_path = os.path.join(main_dir,dir_name)
    if not os.path.exists(new_dir_path):
        os.makedirs(new_dir_path)
    directory_to_check = "../stock_price_data_files"
    valid_output_file = f"../{dir_name}/valid_output_file.txt"
    invalid_output_file = f"../{dir_name}/invalid_output_file.txt"
    main(directory_to_check,valid_output_file, invalid_output_file) #call the main function