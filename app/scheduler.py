from app import db
import random

def update_market_data():
    """Example job function to update market data"""
    symbols = ['AAPL', 'GOOGL', 'MSFT', 'AMZN']
    for symbol in symbols:
        price = random.uniform(100, 1000)
    db.session.commit()
