import sqlite3
import logging
from datetime import datetime
import os
import json

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DataProcessor:
    # Initialize with ApiConnector instance and database file path
    def __init__(self, connector, db_file=os.path.join("data", "db_markets.db")):
        self.connector = connector  
        # ensure the data directory exists
        db_dir = os.path.dirname(db_file)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir, exist_ok=True)

        self.db_conn = sqlite3.connect(db_file, check_same_thread=False)
        self._init_db()
    
    # Set up database tables
    def _init_db(self):
        cursor = self.db_conn.cursor()
        cursor.executescript('''
            CREATE TABLE IF NOT EXISTS markets (
                market_id TEXT PRIMARY KEY,
                title TEXT,
                endDate TEXT,
                active INTEGER,
                closed INTEGER,
                description TEXT  -- Added for market identification
            );

        ''')
        self.db_conn.commit()


    def save_market(self, market):
        cursor = self.db_conn.cursor()
        print(market['id'])
        cursor.execute('''
            INSERT OR REPLACE INTO markets (market_id, title, endDate, active, closed, description)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            market['id'], # unique market identifier
            market['title'], # market title
            market['endDate'], # market end date
            int(market['active']), # active status as integer
            int(market['closed']), # closed status as integer
            market['description']  # Added for market identification
        ))
        self.db_conn.commit()

    
    def fetch_market(self, market_id):
        cursor = self.db_conn.cursor()
        cursor.execute('SELECT * FROM markets WHERE market_id = ?', (market_id,))
        return cursor.fetchone()
        

