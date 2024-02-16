import investpy
import pandas as pd
import requests

def fetch_stock_data(search_by, values):
    results = pd.DataFrame()
    for value in values:
        if search_by == 1:  # symbol
            temp_df = investpy.search_stocks(by='symbol', value=value.strip())
        else:  # name
            temp_df = investpy.search_stocks(by='name', value=value.strip())
        
        if not temp_df.empty:
            results = pd.concat([results, temp_df], ignore_index=True)
    return results

def fetch_quote_search(isin):
    url = f"https://api.investing.com/api/search/v2/search?q={isin}"
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
    print("Welcome to the Stock Information Fetcher!")
    search_by = input("Enter 1 to search by 'symbol' or 2 to search by 'name': ")
    while search_by not in ['1', '2']:
        print("Invalid choice. Please enter 1 or 2.")
        search_by = input("Enter 1 to search by 'symbol' or 2 to search by 'name': ")
    search_by = int(search_by)

    example_input = "MSFT, AAPL" if search_by == 1 else "Microsoft, Apple"
    user_input = input(f"Enter the values separated by commas (e.g., {example_input}): ")
    values = user_input.split(',')
    
    print(f"Fetching information for: {values}")
    stock_data = fetch_stock_data(search_by, values)
    
    if not stock_data.empty:
        print("Here are the results found:")
        print(stock_data)
        row_choice = int(input("Enter the row number for the ISIN of the stock for a quote search: ")) - 1
        if 0 <= row_choice < len(stock_data):
            chosen_isin = stock_data.loc[row_choice, 'isin']
            print(f"Fetching quote search for ISIN: {chosen_isin}")
            quote_data = fetch_quote_search(chosen_isin)
            
            print("Quote search results:")
            print("Articles:")
            for article in quote_data["articles"]:
                print(f"Description: {article['Description']}\nURL: {article['URL']}\n")
            
            print("Quotes:")
            for quote in quote_data["quotes"]:
                print(f"ID: {quote['id']}, Description: {quote['description']}, Symbol: {quote['symbol']}, Exchange: {quote['exchange']}, Country: {quote['flag']}, Type: {quote['type']}\n")
        else:
            print("Invalid row number.")
    else:
        print("No results found for the given inputs.")

if __name__ == "__main__":
    main()
