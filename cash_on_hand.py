from pathlib import Path
import csv

# Define input and output file paths using pathlib
input_filename = Path.cwd() / "csv_reports" / "Cash_on_Hand.csv"
output_filename = Path.cwd() / "summary_report.txt"

# Function to compute cash deficits and write to the output file
def compute_cash_deficits():
    """
    The function computes cash deficits/surpluses by comparing each day's cash with the previous day's.
    No parameter required.
    """ 

    # Open the CSV file and read the contents
    with open(input_filename, 'r') as input_file:
        csv_reader = csv.reader(input_file)

        # Skip the header row
        next(csv_reader)

        # Create an empty list to store the "Day" and "Cash on Hand" values
        cash_data = []

        # Read each row in the CSV file and append the "Day" and "Cash on Hand"
        for row in csv_reader:
            if len(row) >= 2:
                day = int(row[0])
                cash_on_hand = int(row[1])
                cash_data.append((day, cash_on_hand))

    # Create lists
    cash_deficits = []
    cash_surpluses = []
    cash_def = []

    #Initialize days_deficit/surplus before the loop
    days_deficit = 0
    days_surplus = 0

    # Check for cash deficit by comparing current day's cash with previous day's cash
    for i in range(1, len(cash_data)):
        change_amount = cash_data[i][1] - cash_data[i - 1][1]

        # Record a cash deficit for all consecutive days
        if change_amount < 0:
            days_deficit += 1 
            deficit_amount = cash_data[i - 1][1] - cash_data[i][1]
            # Check if the deficit amount is positive
            if deficit_amount > 0:
                cash_deficits.append((cash_data[i][0], deficit_amount))
            days_surplus = 0 

        # Record a cash surplus for all consecutive days
        elif change_amount > 0:
            days_surplus += 1
            surplus_amount = cash_data[i][1] - cash_data[i - 1][1]
            if surplus_amount > 0:
                cash_surpluses.append((cash_data[i][0], surplus_amount))
            days_deficit = 0

        # Record a cash deficit if each day's cash is lower than the previous day
        if change_amount < 0:
            deficit_amount = cash_data[i - 1][1] - cash_data[i][1]
            cash_def.append((cash_data[i][0], deficit_amount))

    # Open the output file in append mode
    with open(output_filename, 'a') as output_file:
        # Check if there are consecutive days with cash deficit
        if days_deficit == 79 and cash_deficits:
            output_file.write("[CASH DEFICIT] CASH ON EACH DAY IS LOWER THAN THE PREVIOUS DAY\n")
            # Sort cash deficits in descending order by deficit amount
            cash_deficits = sorted(cash_deficits, key=get_deficit_amount, reverse=True)
            highest_deficit = cash_deficits[0]
            output_file.write(f"[HIGHEST CASH DEFICIT] DAY: {highest_deficit[0]}, AMOUNT: SGD{highest_deficit[1]}\n")

        # Check if there are consecutive days with cash surplus
        elif days_surplus ==79 and cash_surpluses:
            output_file.write("[CASH SURPLUS] CASH ON EACH DAY IS HIGHER THAN THE PREVIOUS DAY\n")
            # Sort cash deficits in descending order by surplus amount
            cash_surpluses = sorted(cash_surpluses, key=get_surplus_amount, reverse=True)
            highest_surplus = cash_surpluses[0]
            output_file.write(f"[HIGHEST CASH SURPLUS] DAY: {highest_surplus[0]}, AMOUNT: SGD{highest_surplus[1]}\n")
        
        # If no consecutive days with deficit or surplus, write individual deficits to the output file
        else:
            for day, amount in cash_def:
                output_file.write(f"[CASH DEFICIT] DAY: {day}, AMOUNT: SGD{amount}\n")
                
            # Sort cash deficits in descending order by deficit amount
            cash_def = sorted(cash_def, key=get_deficit_amount, reverse=True)

            # Write the top 3 cash deficits to the output file
            for i in range(min(3, len(cash_def))):
                output_file.write(f"[{['HIGHEST', '2ND HIGHEST', '3RD HIGHEST'][i]} CASH DEFICIT] DAY: {cash_def[i][0]}, AMOUNT: SGD{cash_def[i][1]}\n")

# Custom function for sorting by deficit/surplus amount
def get_deficit_amount(item):
    return item[1]
def get_surplus_amount(item):
    return item[1]

# Calling the function
compute_cash_deficits()


