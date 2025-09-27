from src.api_connector import PolymarketConnector as ApiConnector
from src.data_processor import DataProcessor
from.src.order_manager import OrderManager
from datetime import datetime


def main():
    connector = ApiConnector(
        host="https://clob.polymarket.com",
        chain_id=137,
        private_key="df5a6d98a81c136f54c6dd2184c1efa6d1afc568e2a9114e5ffb474917e788f8",
        funder="df5a6d98a81c136f54c6dd2184c1efa6d1afc568e2a9114e5ffb474917e788f8"
    )
    
    #print(datetime.utcfromtimestamp(connector.get_server_time()))
    
    processor = DataProcessor()
    
    
    try:
        fetch = connector.get_markets()
    except Exception as e:
        print(f"Error fetching market data: {e}")
        return
    try: 
        fetch2 = connector.get_market("0x9deb0baac40648821f96f01339229a422e2f5c877de55dc4dbf981f95a1e709c")
    except Exception as e:
        print(f"Error fetching specific market data: {e}")
        return
    
    
    processor.process_markets()

    order_manager = OrderManager(connector)
   
    
    

if __name__ == "__main__":
    main()