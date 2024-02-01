from pathlib import Path
import csv

# Creation of overhead_function 
def overhead_function():
    """
    The function will give the highest overhead of the business over the 90 days.
    No parameter required.
    """ 

    # Assign overheads file located in the current working 
    # directory to variable file_path
    file_path = Path.cwd()/"csv_reports"/"Overheads.csv"
    summary_report = Path.cwd()/"summary_report.txt"

    # Open the file in read mode with UTF-8 encoding and no newline conversion
    with file_path.open(mode = "r",encoding = "UTF-8", newline="") as file:
        
        # Create a csv.reader object to read the file
        reader = csv.reader(file)
        
        # Skip the header row in the CSV file
        next(reader)
    
    # Create an empty list to store category and overhead data
        overheads_list = []

        # Iterate through each row in the CSV file
        for row in reader:

            # Convert the second element of the row to float type and append 
            # the category and overhead as a list to overheads_list
            overheads_list.append([row[0],float(row[1])])

    # Create an empty dictionary to store category as keys 
    # and overhead values as values
    overheads_dict = {}

    # Iterate through each item in overheads_list
    for category, overheads in overheads_list:

        # Check if the category already exists in the dictionary
        if category in overheads_dict:
            # If the category exists, update the value with the maximum 
            # of the current overhead and the existing value
            overheads_dict[category] = max(overheads_dict[category], overheads)

        else:
            # If the category doesn't exist, add a new entry to the 
            # dictionary with the current overhead value
            overheads_dict[category] = overheads
    
    # Find the highest overhead value from the dictionary values
    highest_number = max(overheads_dict.values())

# Open the summary_report text file with append mode
    with summary_report.open(mode="a", encoding = "UTF-8", newline = "") as file_2:

    # Iterate through the dictionary items   
        for category, value in overheads_dict.items():

    # Check if the overhead value matches the highest overhead value
            if value == highest_number:

            # Write the highest overhead with the category and respective value 
            # to the summary report file
                file_2.write(f"[HIGHEST OVERHEAD] {category.upper()}: {highest_number}%\n")

# Calling the function
overhead_function()