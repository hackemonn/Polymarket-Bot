from py_clob_client.client import ClobClient

class PolymarketConnector:
    

    def __init__(self, host: str, chain_id: int, private_key: str, funder: str):
        self.host = host
        self.chain_id = chain_id
        self.private_key = private_key
        self.funder = funder
        self.client = None
        self.api_creds = None
        self.connect()

    
    def connect(self):
        
        try:
            self.client = ClobClient(
                host=self.host,
                key=self.private_key,
                chain_id=self.chain_id,
                signature_type=0,  # default signature type
                funder=self.funder
            )
            self.api_creds = self.client.set_api_creds(self.client.create_or_derive_api_creds())
            print("Connected to Polymarket CLOB successfully (Level 2)")
        except Exception as e:
            print(f"Failed to connect to Polymarket CLOB: {e}")
            raise

    def fetch_markets(self):
        
        try:
            return self.client.get_markets()  # adjust based on actual client method
        except Exception as e:
            print(f"Error fetching markets: {e}")
            return []

    def place_order(self, market_id: str, outcome_id: int, amount: float, side: str):
        """
        Places an order on the CLOB.
        side: 'buy' or 'sell'
        """
        try:
            order = self.client.place_order(
                market_id=market_id,
                outcome_id=outcome_id,
                amount=amount,
                side=side
            )
            print(f"Placed order on market {market_id}: {side} {amount}")
            return order
        except Exception as e:
            print(f"Failed to place order on market {market_id}: {e}")
            return None
    def cancel_order(self, order_id: str):
        """
        Cancels a specific order by its ID.
        """
        try:
            resp = self.client.cancel_order(order_id)
            print(f"Cancelled order {order_id}")
            return resp
        except Exception as e:
            print(f"Failed to cancel order {order_id}: {e}")
            return None

    def cancel_all_orders(self):
        """
        Cancels *all* open orders for this account.
        """
        try:
            resp = self.client.cancel_all_orders()
            print("Cancelled ALL open orders")
            return resp
        except Exception as e:
            print(f"Failed to cancel all orders: {e}")
            return None
        
    def get_server_time(self):
        """
        Fetches the current server time from the CLOB.
        """
        try:
            server_time = self.client.get_server_time()
            print(f"Server time: {server_time}")
            return server_time
        except Exception as e:
            print(f"Failed to fetch server time: {e}")
            return None
        
    def get_market(self, market_id: int):
        """
        Fetches details for a specific market by its ID.
        """
        try:
            market = self.client.get_market(market_id)
            print(f"Fetched market {market_id}: {market}")
            return market
        except Exception as e:
            print(f"Failed to fetch market {market_id}: {e}")
            return None
    
    def get_markets(self):
        """
        Fetches a list of all markets.
        """
        try:
            markets = self.client.get_markets()
            print(f"Fetched {len(markets)} markets")
            return markets
        except Exception as e:
            print(f"Failed to fetch markets: {e}")
            return []
        
    def get_order(self, order_id: str):
        """
        Fetches details for a specific order by its ID.
        """
        try:
            order = self.client.get_order(order_id)
            print(f"Fetched order {order_id}: {order}")
            return order
        except Exception as e:
            print(f"Failed to fetch order {order_id}: {e}")
            return None
    
    def get_open_orders(self):
        """
        Fetches all open orders for this account.
        """
        try:
            orders = self.client.get_orders()
            print(f"Fetched {len(orders)} open orders")
            return orders
        except Exception as e:
            print(f"Failed to fetch open orders: {e}")
            return []
    
    def get_order_book(self, market_id: int):
        """
        Fetches the order book for a specific market.
        """
        try:
            order_book = self.client.get_order_book(market_id)
            print(f"Fetched order book for market {market_id}")
            return order_book
        except Exception as e:
            print(f"Failed to fetch order book for market {market_id}: {e}")
            return None

    
    
