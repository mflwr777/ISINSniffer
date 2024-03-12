import investpy
import pandas as pd
import requests

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.expand_frame_repr', False)
pd.set_option('display.width', None)

def fetch_etf_data(search_by, values):
    results = pd.DataFrame()
    for value in values:
        if search_by == 1:  # symbol
            temp_df = investpy.search_etfs(by='symbol', value=value.strip())
        else:  # name
            temp_df = investpy.search_etfs(by='name', value=value.strip())

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
    print("Welcome to the ETF Information Fetcher!")
    search_by = input("Enter 1 to search by 'symbol' or 2 to search by 'name': ")
    while search_by not in ['1', '2']:
        print("Invalid choice. Please enter 1 or 2.")
        search_by = input("Enter 1 to search by 'symbol' or 2 to search by 'name': ")
    search_by = int(search_by)

    example_input = "SPY, VTI" if search_by == 1 else "SPDR S&P 500 ETF Trust, Vanguard Total Stock Market ETF"
    user_input = input(f"Enter the ETF values separated by commas (e.g., {example_input}): ")
    values = [value.strip() for value in user_input.split(',')]

    print(f"Fetching information for: {values}")
    etf_data = fetch_etf_data(search_by, values)

    if not etf_data.empty:
        print("Here are the results found:")
        etf_data.index += 1  # Start index from 1 instead of 0
        print(etf_data.to_string(index=True))

        while True:
            row_choice_input = input("Enter the row number for the ETF quote search (starting from 1): ")
            try:
                row_choice = int(row_choice_input)
                if 1 <= row_choice <= len(etf_data):
                    chosen_symbol = etf_data.iloc[row_choice - 1]['symbol']
                    print(f"Fetching quote search for symbol: {chosen_symbol}")
                    quote_data = fetch_quote_search(chosen_symbol)

                    if quote_data != "Failed to fetch quote data.":
                        print("Quote search results:")
                        print("Articles:")
                        for article in quote_data["articles"]:
                            print(f"Description: {article['Description']}\nURL: {article['URL']}\n")

                        print("Quotes:")
                        for quote in quote_data["quotes"]:
                            print(f"ID: {quote['id']}, Description: {quote['description']}, Symbol: {quote['symbol']}, Exchange: {quote['exchange']}, Country: {quote['flag']}, Type: {quote['type']}\n")
                    else:
                        print("Failed to fetch quote search results for the given symbol.")
                    break  # Successfully executed, exit loop
                else:
                    print("Invalid row number. Please enter a number within the displayed range, starting from 1.")
            except ValueError:
                print("Invalid input. Please enter a valid integer.")
    else:
        print("No results found for the given inputs.")

if __name__ == "__main__":
    main()