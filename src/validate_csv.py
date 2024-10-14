import csv

#Extended validation
def is_valid_csv(file_path, num_of_columns):
    try:
        with open(file_path, 'r', newline='', encoding='utf-8') as file:
            reader =  csv.reader(file)

            for row in reader:
                if len(row) != num_of_columns: #Compares the number of columns of each row with the number of columns that it should have, i.e. 3 in our case
                    return False #Inconsistent row found
        return True
    except Exception as e:
        logging.error(f"Error validating rows {file_path}: {e}")
        return False    
