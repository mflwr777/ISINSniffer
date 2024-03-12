import investpy
import pandas as pd
import requests

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.expand_frame_repr', False)
pd.set_option('display.width', None)

def fetch_data(asset_type, search_by, values):
    if asset_type == 1:  # Stocks
        search_func = investpy.search_stocks
    elif asset_type == 2:  # Indices
        search_func = investpy.search_indices
    elif asset_type == 3:  # Currency Crosses
        search_func = investpy.search_currency_crosses
    elif asset_type == 4:  # Commodities
        search_func = investpy.search_commodities
    elif asset_type == 5:  # ETFs
        search_func = investpy.search_etfs
    else:
        raise ValueError("Invalid asset type.")

    results = pd.DataFrame()
    for value in values:
        if search_by == 1:  # Symbol or Name
            temp_df = search_func(by='symbol' if asset_type not in [3, 4, 5] else 'name', value=value.strip())
        else:  # Name or Full Name
            temp_df = search_func(by='name' if asset_type not in [3, 4, 5] else 'full_name', value=value.strip())

        if not temp_df.empty:
            results = pd.concat([results, temp_df], ignore_index=True)

    return results

def fetch_quote_search(query):
    url = f"https://api.investing.com/api/search/v2/search?q={query}"
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        json_data = response.json()
        articles = json_data.get('articles', [])
        quotes = json_data.get('quotes', [])

        # Process and format articles
        formatted_articles = [{"Description": article['description'], "URL": "https://www.investing.com" + article['url']} for article in articles]

        # Return formatted articles and raw quotes
        return {"articles": formatted_articles, "quotes": quotes}
    else:
        return "Failed to fetch quote data."

def main():
    print("Welcome to the Asset Information Fetcher!")

    asset_type = input("Enter 1 for Stocks, 2 for Indices, 3 for Currency Crosses, 4 for Commodities, or 5 for ETFs: ")
    while asset_type not in ['1', '2', '3', '4', '5']:
        print("Invalid choice. Please enter 1, 2, 3, 4, or 5.")
        asset_type = input("Enter 1 for Stocks, 2 for Indices, 3 for Currency Crosses, 4 for Commodities, or 5 for ETFs: ")
    asset_type = int(asset_type)

    if asset_type == 1:
        print("You have selected Stocks.")
        search_by_prompt = "Enter 1 to search by 'symbol' or 2 to search by 'name': "
    elif asset_type == 2:
        print("You have selected Indices.")
        search_by_prompt = "Enter 1 to search by 'symbol' or 2 to search by 'name': "
    elif asset_type == 3:
        print("You have selected Currency Crosses.")
        search_by_prompt = "Enter 1 to search by 'name' or 2 to search by 'full_name': "
    elif asset_type == 4:
        print("You have selected Commodities.")
        search_by_prompt = "Enter 1 to search by 'name' or 2 to search by 'full_name': "
    else:
        print("You have selected ETFs.")
        search_by_prompt = "Enter 1 to search by 'symbol' or 2 to search by 'name': "

    search_by = input(search_by_prompt)
    while search_by not in ['1', '2']:
        print("Invalid choice. Please enter 1 or 2.")
        search_by = input(search_by_prompt)
    search_by = int(search_by)

    if asset_type == 1:
        example_input = "MSFT, AAPL" if search_by == 1 else "Microsoft, Apple"
    elif asset_type == 2:
        example_input = "^DJI, ^GSPC" if search_by == 1 else "Dow Jones Industrial Average, S&P 500"
    elif asset_type == 3:
        example_input = "EUR/USD, GBP/USD" if search_by == 1 else "Euro / US Dollar, British Pound / US Dollar"
    elif asset_type == 4:
        example_input = "Gold, Silver" if search_by == 1 else "Gold Spot, Silver Spot"
    else:
        example_input = "SPY, VTI" if search_by == 1 else "SPDR S&P 500 ETF Trust, Vanguard Total Stock Market ETF"

    user_input = input(f"Enter the values separated by commas (e.g., {example_input}): ")
    values = [value.strip() for value in user_input.split(',')]

    print(f"Fetching information for: {values}")
    data = fetch_data(asset_type, search_by, values)

    if not data.empty:
        print("Here are the results found:")
        data.index += 1  # Start index from 1 instead of 0
        print(data.to_string(index=True))

        while True:
            row_choice_input = input("Enter the row number for the quote search (starting from 1): ")
            try:
                row_choice = int(row_choice_input)
                if 1 <= row_choice <= len(data):
                    if asset_type == 1:  # Stocks
                        query = data.iloc[row_choice - 1]['isin']
                    elif asset_type == 2:  # Indices
                        query = data.iloc[row_choice - 1]['full_name']
                    elif asset_type == 3:  # Currency Crosses
                        query = data.iloc[row_choice - 1]['name']
                    elif asset_type == 4:  # Commodities
                        query = data.iloc[row_choice - 1]['name']
                    else:  # ETFs
                        query = data.iloc[row_choice - 1]['symbol']

                    print(f"Fetching quote search for: {query}")
                    quote_data = fetch_quote_search(query)

                    if quote_data != "Failed to fetch quote data.":
                        print("Quote search results:")
                        print("Articles:")
                        for article in quote_data["articles"]:
                            print(f"Description: {article['Description']}\nURL: {article['URL']}\n")
                        print("Quotes:")
                        for quote in quote_data["quotes"]:
                            print(f"ID: {quote['id']}, Description: {quote['description']}, Symbol: {quote['symbol']}, Exchange: {quote['exchange']}, Country: {quote['flag']}, Type: {quote['type']}\n")
                    else:
                        print("Failed to fetch quote search results for the given query.")
                    break  # Successfully executed, exit loop
                else:
                    print("Invalid row number. Please enter a number within the displayed range, starting from 1.")
            except ValueError:
                print("Invalid input. Please enter a valid integer.")
    else:
        print("No results found for the given inputs.")

if __name__ == "__main__":
    main()