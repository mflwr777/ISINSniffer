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
    else:
        raise ValueError("Invalid asset type.")

    results = pd.DataFrame()
    for value in values:
        if search_by == 1:  # Symbol
            temp_df = search_func(by='symbol', value=value.strip())
        else:  # Name
            temp_df = search_func(by='name', value=value.strip())

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

    asset_type = input("Enter 1 for Stocks or 2 for Indices: ")
    while asset_type not in ['1', '2']:
        print("Invalid choice. Please enter 1 or 2.")
        asset_type = input("Enter 1 for Stocks or 2 for Indices: ")
    asset_type = int(asset_type)

    search_by = input("Enter 1 to search by 'symbol' or 2 to search by 'name': ")
    while search_by not in ['1', '2']:
        print("Invalid choice. Please enter 1 or 2.")
        search_by = input("Enter 1 to search by 'symbol' or 2 to search by 'name': ")
    search_by = int(search_by)

    example_input = "MSFT, AAPL" if asset_type == 1 and search_by == 1 else "Microsoft, Apple" if asset_type == 1 else "^DJI, ^GSPC" if search_by == 1 else "Dow Jones Industrial Average, S&P 500"
    user_input = input(f"Enter the values separated by commas (e.g., {example_input}): ")
    values = [value.strip() for value in user_input.split(',')]

    print(f"Fetching information for: {values}")
    data = fetch_data(asset_type, search_by, values)

    if not data.empty:
        print("Here are the results found:")
        print(data)

        while True:
            row_choice_input = input("Enter the row number for the quote search (starting from 0): ")
            try:
                row_choice = int(row_choice_input)
                if 0 <= row_choice < len(data):
                    if asset_type == 1:  # Stocks
                        query = data.iloc[row_choice]['isin']
                    else:  # Indices
                        query = data.iloc[row_choice]['full_name']

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
                    print("Invalid row number. Please enter a number within the displayed range, starting from 0.")
            except ValueError:
                print("Invalid input. Please enter a valid integer.")
    else:
        print("No results found for the given inputs.")

if __name__ == "__main__":
    main()