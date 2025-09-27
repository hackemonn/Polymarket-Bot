from src.api_connector import PolymarketConnector

class OrderManager:
    def __init__(self, connector: PolymarketConnector):
        self.connector = connector

    def place_market_order(self, market_id, token_id, side, quantity):
        """
        Place a market order (buy/sell at current market price)
        side: 'buy' or 'sell'
        """
        return self.connector.place_order(
            market_id=market_id,
            token_id=token_id,
            action=side,
            quantity=quantity,
            order_type="market"
        )

    def place_limit_order(self, market_id, token_id, side, quantity, price):
        """
        Place a limit order at a specified price
        """
        return self.connector.place_order(
            market_id=market_id,
            token_id=token_id,
            action=side,
            quantity=quantity,
            price=price,
            order_type="limit"
        )


    def cancel_order(self, order_id):
        """Cancel a single order"""
        return self.connector.cancel_order(order_id)

    def cancel_all_orders(self):
        """Cancel all open orders"""
        return self.connector.cancel_all_orders()

    def get_open_orders(self):
        """Return a list of all open orders"""
        return self.connector.get_open_orders()

    def get_order_by_id(self, order_id):
        """Return details of a specific order"""
        return self.connector.get_order(order_id)

    def modify_order(self, order_id, quantity=None, price=None):
        """
        Modify an existing order.
        Only quantity or price can be changed (or both)
        """
        return self.connector.modify_order(order_id, quantity=quantity, price=price)


    def get_average_price(self, market_id, token_id):
        """
        Calculate average executed price for a token
        Optional: can also implement in strategy
        """
        trades = self.connector.get_trades(market_id, token_id)
        if not trades:
            return None
        total_value = sum(t["price"] * t["quantity"] for t in trades)
        total_qty = sum(t["quantity"] for t in trades)
        return total_value / total_qty if total_qty > 0 else None

