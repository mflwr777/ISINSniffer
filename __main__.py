# Description: This script fetches stock information using the investpy library.
# It prompts the user to input the stock symbols or names and fetches the information.
# The user can choose to search by symbol or name.
# The script uses the `investpy` library to fetch the stock information.

import investpy
import pandas as pd

def fetch_stock_data(search_by, values):
    results = pd.DataFrame()
    for value in values:
        if search_by == 'symbol':
            temp_df = investpy.search_stocks(by='symbol', value=value.strip())
        else:  # search_by == 'name'
            temp_df = investpy.search_stocks(by='name', value=value.strip())
        
        # Filter exact matches if necessary and append to results
        if not temp_df.empty:
            # Filtering out the exact matches might not be straightforward for names due to various naming conventions
            results = pd.concat([results, temp_df], ignore_index=True)
    return results

def main():
    print("Welcome to the Stock Information Fetcher!")
    search_by = input("Do you want to search by 'symbol' or 'name'? ").lower()
    while search_by not in ['symbol', 'name']:
        print("Invalid choice. Please type 'symbol' or 'name'.")
        search_by = input("Do you want to search by 'symbol' or 'name'? ").lower()

    example_input = "MSFT, AAPL" if search_by == 'symbol' else "Microsoft, Apple"
    user_input = input(f"Enter the {search_by}s separated by commas (e.g., {example_input}): ")
    values = user_input.split(',')
    
    print(f"Fetching information for {search_by}s: {values}")
    stock_data = fetch_stock_data(search_by, values)
    
    if not stock_data.empty:
        print("Here are the results found:")
        print(stock_data)
    else:
        print("No results found for the given inputs.")

if __name__ == "__main__":
    main()
