import overheads, cash_on_hand, profit_loss

# Function to call all the other functions
def main():
    overheads.overhead_function()
    cash_on_hand.compute_cash_deficits() 
    profit_loss.calculate_profit_deficit()
