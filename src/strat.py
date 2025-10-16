import numpy as np
from datetime import datetime
import sqlite3
from src.api_connector import PolymarketConnector
from src.order_manager import OrderManager
from src.data_processor import DataProcessor
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ValueBettingStrategy:
    def __init__(self, connector: PolymarketConnector, order_manager: OrderManager, 
                 data_processor: DataProcessor, edge_threshold=0.05, capital_per_trade=100):
        self.connector = connector
        self.order_manager = order_manager
        self.data_processor = data_processor
        self.edge_threshold = edge_threshold
        self.capital_per_trade = capital_per_trade  # $100 from $3K
        self.db_conn = sqlite3.connect('trades.db')
        self._init_db()

    def _init_db(self):
        cursor = self.db_conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS trades (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                market_id TEXT,
                yes_price REAL,
                fair_prob REAL,
                std_dev REAL,
                edge REAL,
                decision TEXT,
                amount REAL
            )
        ''')
        self.db_conn.commit()

    async def decide_trade(self, market_id):
        market_data = await self.connector.get_market(market_id)
        yes_price = market_data['tokens'][0]['price'] if market_data['tokens'] else 0.5
        historical = self.data_processor.get_historical_data(market_id, limit=50)
        probs = [d['yes_price'] for d in historical] or [0.5]
        
        fair_prob = np.mean(probs)
        std_dev = np.std(probs) if len(probs) > 1 else 0.1
        edge = fair_prob - yes_price
        
        if abs(edge) > self.edge_threshold and std_dev < 0.2:
            decision = "BUY YES" if edge > 0 else "BUY NO"
            amount = self.capital_per_trade
        else:
            decision = "HOLD"
            amount = 0
        
        log = {
            'timestamp': datetime.now().isoformat(),
            'market_id': market_id,
            'yes_price': yes_price,
            'fair_prob': fair_prob,
            'std_dev': std_dev,
            'edge': edge,
            'decision': decision,
            'amount': amount
        }
        cursor = self.db_conn.cursor()
        cursor.execute('''
            INSERT INTO trades (timestamp, market_id, yes_price, fair_prob, std_dev, edge, decision, amount)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (log['timestamp'], log['market_id'], log['yes_price'], log['fair_prob'], 
              log['std_dev'], log['edge'], log['decision'], log['amount']))
        self.db_conn.commit()
        
        if decision != "HOLD":
            await self.order_manager.execute_trade(market_id, decision, amount)
        logger.info(f"Decision for {market_id}: {decision}, edge={edge:.3f}")
        return decision, amount, log

    async def simulate_risk(self, market_id, num_sims=1000):
        historical = self.data_processor.get_historical_data(market_id, limit=50)
        probs = [d['yes_price'] for d in historical] or [0.5]
        fair_prob = np.mean(probs)
        std_dev = np.std(probs) if len(probs) > 1 else 0.1
        simulated_returns = np.random.normal(fair_prob - 0.5, std_dev, num_sims)
        return {
            'win_rate': np.mean(simulated_returns > 0),
            'avg_return': np.mean(simulated_returns),
            'worst_drawdown': np.min(np.cumsum(simulated_returns)),
            'sims': num_sims
        }