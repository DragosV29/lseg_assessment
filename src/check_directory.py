#This function will check the data and data input validity

import os
import csv
import logging
from logging_config import setup_logging
from validate_csv import is_valid_csv


#Check dir/file templates have data
def check_directory_recursively(directory, valid_output_file, invalid_output_file):
    valid_files = []
    invalid_files = []
    num_of_columns = 3 #each row of the files should have three columns
    #Go through the directory tree
    for root, dirs, files in os.walk(directory):
        dirs[:] = [d for d in dirs if not d.startswith('.')]    
        #check the directories
        visible_files = [ f for f in os.listdir(root) if not f.startswith('.') ]
        if not visible_files: #Directory is eMPTY
            print(f"Warning: The directory '{root}' is empty and will skip")
        else:
            for file in files:
                if not file.startswith('.'): #skip hidden files
                    file_path = os.path.join(root, file)
                    if os.path.getsize(file_path) == 0: #File is empty
                        print(f"Warning: The file '{file_path}' is empty")
                        invalid_files.append(file_path)
                    else:
                        if is_valid_csv(file_path, num_of_columns):
                            print(f"Checked: The file '{file_path}' is a valid csv")
                            valid_files.append(file_path)
                        else:
                            print(f"Checked: The file '{file_path}' is has inconsistent rows")  
                            invalid_files.append(file_path)
    

    #Write results to output file
    with open(valid_output_file, mode='w', newline='') as f_valid:
        for valid_file in valid_files:
            f_valid.write(valid_file + '\n')
            logging.info(f"valid file: {valid_file}")

    with open(invalid_output_file, mode='w', newline='') as f_invalid:
        for invalid_file in invalid_files:
            f_invalid.write(invalid_file + '\n')
            logging.warning(f"invalid file: {invalid_file}")
    
    #Return warning if there are invalid files
    if os.path.getsize(invalid_output_file) > 0: # The invalid_output_file is not empty
        print(f"Warning: There are invalid files listed in '{invalid_output_file}' ")
        logging.warning(f"There are invalid files listed in '{invalid_output_file}' ")
    else:
        print(f"Info: There are no invalid files ")
        logging.info(" There are no invalid files")   

    #Return warning if there are no valid files
    if os.path.getsize(valid_output_file) == 0: # The invalid_output_file is not empty
        print(f"Warning: There are no valid files listed in '{valid_output_file}' ")
        logging.warning(f"There are no valid files listed in '{valid_output_file}' ")  
    else:
        print(f"Info: Valid files listed in '{valid_output_file}' ")
        logging.info(f"Valid files listed in '{valid_output_file}' ")                        

