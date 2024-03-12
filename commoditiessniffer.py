import investpy
import pandas as pd
import requests

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.expand_frame_repr', False)
pd.set_option('display.width', None)

def fetch_commodity_data(search_by, values):
    results = pd.DataFrame()
    for value in values:
        if search_by == 1:  # name
            temp_df = investpy.search_commodities(by='name', value=value.strip())
        else:  # full_name
            temp_df = investpy.search_commodities(by='full_name', value=value.strip())

        if not temp_df.empty:
            results = pd.concat([results, temp_df], ignore_index=True)
    return results

def fetch_quote_search(commodity):
    url = f"https://api.investing.com/api/search/v2/search?q={commodity}"
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
    print("Welcome to the Commodity Information Fetcher!")
    search_by = input("Enter 1 to search by 'name' or 2 to search by 'full_name': ")
    while search_by not in ['1', '2']:
        print("Invalid choice. Please enter 1 or 2.")
        search_by = input("Enter 1 to search by 'name' or 2 to search by 'full_name': ")
    search_by = int(search_by)

    example_input = "Gold, Silver" if search_by == 1 else "Gold Spot, Silver Spot"
    user_input = input(f"Enter the commodity names separated by commas (e.g., {example_input}): ")
    values = [value.strip() for value in user_input.split(',')]

    print(f"Fetching information for: {values}")
    commodity_data = fetch_commodity_data(search_by, values)

    if not commodity_data.empty:
        print("Here are the results found:")
        commodity_data.index += 1  # Start index from 1 instead of 0
        print(commodity_data.to_string(index=True))

        while True:
            row_choice_input = input("Enter the row number for the commodity quote search (starting from 1): ")
            try:
                row_choice = int(row_choice_input)
                if 1 <= row_choice <= len(commodity_data):
                    chosen_commodity = commodity_data.iloc[row_choice - 1]['name']
                    print(f"Fetching quote search for commodity: {chosen_commodity}")
                    quote_data = fetch_quote_search(chosen_commodity)

                    if quote_data != "Failed to fetch quote data.":
                        print("Quote search results:")
                        print("Articles:")
                        for article in quote_data["articles"]:
                            print(f"Description: {article['Description']}\nURL: {article['URL']}\n")

                        print("Quotes:")
                        for quote in quote_data["quotes"]:
                            print(f"ID: {quote['id']}, Description: {quote['description']}, Symbol: {quote['symbol']}, Exchange: {quote['exchange']}, Country: {quote['flag']}, Type: {quote['type']}\n")
                    else:
                        print("Failed to fetch quote search results for the given commodity.")

                    break  # Successfully executed, exit loop
                else:
                    print("Invalid row number. Please enter a number within the displayed range, starting from 1.")
            except ValueError:
                print("Invalid input. Please enter a valid integer.")
    else:
        print("No results found for the given inputs.")

if __name__ == "__main__":
    main()