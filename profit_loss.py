from pathlib import Path
import csv

# Create the file paths to the current working directory
input_csv_file = Path.cwd() / "csv_reports" / "Profit_and_Loss.csv"
output_text_file = Path.cwd() / "summary_report.txt"

def calculate_profit_deficit():
    """
    The function computes net profit deficits/surpluses by comparing each day's profit with the previous day's.
    No parameter required.
    """

    # Open the input CSV file
    with open(input_csv_file, newline='') as csvfile:

        # Read the CSV file using the csv.reader
        reader = csv.reader(csvfile)
        # Skip the header row 
        next(reader)

        # Initialize prev_net_profit before the loop
        prev_net_profit = 0

        # Initialize all list before the loop
        deficit_amount_list = []
        surplus_amount_list = []
        def_amount_list = []

        # Initialize days_deficit/surplus before the loop
        days_deficit = 0
        days_surplus = 0

        # Open the output text file in write mode
        with open(output_text_file, 'a') as output_file:
            # Iterate through the data (list of lists)
            for row in reader:

                # Increment the day count
                day = int(row[0])

                # Convert the 'Net Profit' value for the current day to an integer
                current_net_profit = int(row[4])

                # Initialize deficit_amount and surplus_amount
                deficit_amount = 0 
                surplus_amount = 0

                # Calculate the net profit difference between current and previous days
                net_profit_difference = current_net_profit - prev_net_profit

                # Check for a deficit in net profit
                if net_profit_difference < 0:
                    days_deficit += 1
                    days_surplus = 0
                    deficit_amount = prev_net_profit - current_net_profit
                    # Append deficit information to the list
                    if deficit_amount > 0 :
                        deficit_amount_list.append({'day': day, 'amount': deficit_amount})

                # Check for a surplus in net profit
                elif net_profit_difference > 0:
                    days_surplus += 1
                    days_deficit = 0
                    surplus_amount = current_net_profit - prev_net_profit
                    # Append surplus information to the list
                    if surplus_amount > 0:
                        surplus_amount_list.append({'day': day, 'amount': surplus_amount})

                if day > 11 and current_net_profit < prev_net_profit:
                    deficit_amount = prev_net_profit - current_net_profit
                    # Append deficit information to the list
                    def_amount_list.append({'day': day, 'amount': deficit_amount})

                # Store the 'Net Profit' value for the current day as previous day's 
                # net profit for the next iteration
                prev_net_profit = current_net_profit
   

            # Check if there are consecutive days with net profit deficit
            if days_deficit == 79 and deficit_amount_list:
                output_file.write("[NET PROFIT DEFICIT] NET PROFIT ON EACH DAY IS LOWER THAN THE PREVIOUS DAY\n")
                # Sort net profit deficits in descending order by deficit amount
                deficit_amount_list = sorted(deficit_amount_list, key=get_deficit_amount, reverse=True)
                highest_deficit = deficit_amount_list[0]
                output_file.write(f"[HIGHEST PROFIT DEFICIT] DAY: {highest_deficit['day']}, AMOUNT: USD{highest_deficit['amount']}\n")

            # Check if there are consecutive days with net profit surplus
            elif days_surplus == 79 and surplus_amount_list:
                output_file.write("[NET PROFIT SURPLUS] NET PROFIT ON EACH DAY IS HIGHER THAN THE PREVIOUS DAY\n")
                # Sort net profit deficits in descending order by surplus amount
                surplus_amount_list = sorted(surplus_amount_list, key=get_surplus_amount, reverse=True)
                highest_surplus = surplus_amount_list[0]
                output_file.write(f"[HIGHEST PROFIT SURPLUS] DAY: {highest_surplus['day']}, AMOUNT: USD{highest_surplus['amount']}\n")
            
            # If no consecutive days with deficit or surplus, write individual deficit amounts to the output file
            else:
                for item in def_amount_list:
                    output_file.write(f"[NET PROFIT DEFICIT] DAY: {item['day']}, AMOUNT: USD{item['amount']}\n")

                # Sort net profit deficits in descending order by deficit amount
                def_amount_list = sorted(def_amount_list, key=get_deficit_amount, reverse=True)

                # Write the top 3 deficit amounts to the output file
                for i in range(min(3, len(def_amount_list))):
                    output_file.write(f"[{['HIGHEST', '2ND HIGHEST', '3RD HIGHEST'][i]} NET PROFIT DEFICIT] DAY: {def_amount_list[i]['day']}, AMOUNT: USD{def_amount_list[i]['amount']}\n")

# Custom function for sorting by deficit amount
def get_deficit_amount(item):
    return item['amount']

def get_surplus_amount(item):
    return item['amount']

# Calling the function
calculate_profit_deficit()
