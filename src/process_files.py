import csv
import os
import logging
import random
import math



#Read 30 lines from a CSV starting a random line and yyelds them one by one
def read_lines_from_csv_as_feed(input_file, num_lines=30):
    try:
        with open(input_file, mode='r', newline='') as file:
            reader = list(csv.reader(file))
            total_rows = len(reader)

            #Get a random starting line without going out of range
            start_line = random.randint(0, total_rows - num_lines)

            #Yield 30 lines starting from random start line
            for i in range(start_line, start_line + num_lines):
                yield reader[i]
    except Exception as e:
        logging.error(f"Error reading from CSV file '{input_file}': {e}")
        print(f"Failed to read from CSV file '{input_file}'. Check log for details")

def calculate_standard_deviation(values,mean):
    variance = sum((x - mean) ** 2 for x in values) / len(values)
    return math.sqrt(variance)

def consume_feed_and_write_to_csv(feed, output_file):
    values = [] #Hold the values to calculate the mean
    lines = [] #Store the lines

    #Extract the values from the feed
    for line in feed:
        #get value from third column
        value = float(line[2]) #Convert the value to float for calculation
        values.append(value)
        lines.append(line)

    #Calculate the mean of the values
    mean_value = sum(values) / len(values) if values else 0

    #Calculate the std deviation
    std_deviation = calculate_standard_deviation(values, mean_value)

    #Define the threshold for outliers (2 standard deviations beyond the mean)
    threshold = 2 * std_deviation

    outlier_lines = [] #To store the outlier lines

    for line in lines:
        value = float(line[2]) #Get the value for the difference
        diff = value - mean_value #Calculate the difference
        percent_deviation = ((diff) / mean_value) * 100 #Calculate % deviation

        if abs(diff) > threshold:
            outlier_lines.append([line[0], line[1], value, mean_value, diff, percent_deviation]) #Store outlier information 
        
    if outlier_lines:
        try:
            with open(output_file, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(outlier_lines)
            print(f"Outlier lines have been written to {output_file}")
            logging.info(f"Outlier lines have been written to {output_file}")
        except Exception as e:
            logging.error(f"Failed to write to CSV file '{output_file}': {e}")
            print(f"Failed to write to CSV file '{output_file}'. Check log for details")
    else:
        print("No outliers found in the sampled data")
        logging.info(f"No outliers found in the sampled data")