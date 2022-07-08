import csv
import requests
from datetime import datetime
from operator import itemgetter
from sqlalchemy.orm import Session


from aggregator.db.engine.utils import getDbEngine
from aggregator.db.models.market import Market
from aggregator.db.models.trades import Trades

if __name__ == "__main__":
    start = int(datetime.strptime("01/01/2020", '%m/%d/%Y').timestamp())
    end = int(datetime.strptime("12/29/2021", '%m/%d/%Y').timestamp())
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
    }
    engine = getDbEngine()
    with Session(engine) as sess, requests.Session() as req:
        symbols = sess.query(Trades.symbol).distinct().all()
        for cymbal in symbols:
            symbol = cymbal[0]
            url = f"https://query1.finance.yahoo.com/v7/finance/download/{symbol}?period1={start}&period2={end}&interval=1d&events=history&includeAdjustedClose=true"
            yahoo = req.get(url, headers=headers)
            lines = (line for line in yahoo.iter_lines(decode_unicode=True))
            history = csv.DictReader(lines)
            for row in history:
                date, open, high, low, close, adjusted_close, volume = itemgetter(
                    "Date", "Open", "High", "Low", "Close", "Adj Close", "Volume")(row)
                data = Market(symbol=symbol, date=date, open=open, high=high, low=low,
                              close=close, adjusted_close=adjusted_close, volume=volume)
                sess.add(data)
            sess.commit()
