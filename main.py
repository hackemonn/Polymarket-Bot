from src.api_connector import PolymarketConnector as ApiConnector
from src.data_processor import DataProcessor
from src.order_manager import OrderManager
from datetime import datetime
import requests
import json

status = True

def main():
    print(f"Welcome to Polymarket bot — {datetime.utcnow().isoformat()}Z")
    connector = ApiConnector(
            host="https://clob.polymarket.com",
            chain_id=137,
            private_key="df5a6d98a81c136f54c6dd2184c1efa6d1afc568e2a9114e5ffb474917e788f8",
            funder="df5a6d98a81c136f54c6dd2184c1efa6d1afc568e2a9114e5ffb474917e788f8"
            #demo key, do not use in production
    )
    processor = DataProcessor(connector)
    while(status):
        print("Select the option you want to perform:\n1. Fetch market data\n2. Exit")

        option = int(input())
        
        if option == 2:
            print("Exiting the program. Goodbye!")
            break
        elif option == 1:
            #get the slug of the market you want to fetch data for
            market_slug = str(input("Enter the market slug: "))
            
            url = "https://gamma-api.polymarket.com/events/slug/" + market_slug

            try:
                response = requests.get(url)
                data = response.json()
                with open('data/market_temp.json', 'w') as f:
                    json.dump(data, f, indent=4)
                print(f"Market data saved to data/market_temp.json")
                processor.save_market(data)
                print(f"Market data for '{market_slug}' saved to database.")
            except Exception as e:
                print(f"Error fetching market data: {e}")
                return


            #Now we are going to process the data and store it in the database
            
        elif option != 1:
            print("Invalid option. Please try again.")
    
    
    

if __name__ == "__main__":
    main()