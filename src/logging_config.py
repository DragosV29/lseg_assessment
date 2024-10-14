import logging
import os

def setup_logging(log_dir='../logs', log_file_name='assessment.log'):
#clear the log file at the start of the script
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    log_file_path = os.path.join(log_dir, log_file_name)

    with open(log_file_path, 'w') as log_file:
        log_file.write('') #This will cleanup the log

    logging.basicConfig(
        filename=log_file_path, 
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )