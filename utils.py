from datetime import datetime, timedelta
import requests
import json
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

API_KEY = config['Data']['API_KEY']

def getOpenandClose(stockTicker):
    current_date = datetime.now()
    day_before = current_date - timedelta(days=1)
    TIMESTAMP = day_before.strftime('%Y-%m-%d')
    res = requests.get(f"https://api.polygon.io/v1/open-close/{stockTicker}/{TIMESTAMP}?adjusted=true&apiKey={API_KEY}")
    return res.json()

class getSMA:
    def __init__(self, stockTicker):
        self.stockTicker = stockTicker
        
    def getDay(self,window):
        URL = f"https://api.polygon.io/v1/indicators/sma/{self.stockTicker}?timespan=day&adjusted=true&window={window}&series_type=close&order=desc&apiKey={API_KEY}"
        res = requests.get(URL)
        return res.json()['results']['values']
    def getWeek(self,window):
        URL = f"https://api.polygon.io/v1/indicators/sma/{self.stockTicker}?timespan=week&adjusted=true&window={window}&series_type=close&order=desc&apiKey={API_KEY}"
        res = requests.get(URL)
        return res.json()['results']['values']

class getEMA:
    def __init__(self, stockTicker):
        self.stockTicker = stockTicker
        
    def getDay(self,window):
        URL = f"https://api.polygon.io/v1/indicators/ema/{self.stockTicker}?timespan=day&adjusted=true&window={window}&series_type=close&order=desc&apiKey={API_KEY}"
        res = requests.get(URL)
        return res.json()['results']['values']
    def getWeek(self,window):
        URL = f"https://api.polygon.io/v1/indicators/ema/{self.stockTicker}?timespan=week&adjusted=true&window={window}&series_type=close&order=desc&apiKey={API_KEY}"
        res = requests.get(URL)
        return res.json()['results']['values']
    def getMonth(self,window):
        URL = f"https://api.polygon.io/v1/indicators/ema/{self.stockTicker}?timespan=month&adjusted=true&window={window}&series_type=close&order=desc&apiKey={API_KEY}"
        res = requests.get(URL)
        return res.json()['results']['values']

class getMACD:
    def __init__(self, stockTicker):
        self.stockTicker = stockTicker
        
    def getDay(self):
        URL = f"https://api.polygon.io/v1/indicators/macd/{self.stockTicker}?timespan=day&adjusted=true&short_window=12&long_window=26&signal_window=9&series_type=close&order=desc&apiKey={API_KEY}"
        res = requests.get(URL)
        return res.json()['results']['values']
    def getWeek(self):
        URL = f"https://api.polygon.io/v1/indicators/macd/{self.stockTicker}?timespan=week&adjusted=true&short_window=12&long_window=26&signal_window=9&series_type=close&order=desc&apiKey={API_KEY}"
        res = requests.get(URL)
        return res.json()['results']['values']

class getRSI:
    def __init__(self, stockTicker):
        self.stockTicker = stockTicker
        
    def getDay(self):
        URL = f"https://api.polygon.io/v1/indicators/rsi/{self.stockTicker}?timespan=day&adjusted=true&window=14&series_type=close&order=desc&apiKey={API_KEY}"
        res = requests.get(URL)
        return res.json()['results']['values']
    def getWeek(self):
        URL = f"https://api.polygon.io/v1/indicators/rsi/{self.stockTicker}?timespan=week&adjusted=true&window=14&series_type=close&order=desc&apiKey={API_KEY}"
        res = requests.get(URL)
        return res.json()['results']['values']
    def getMonth(self):
        URL = f"https://api.polygon.io/v1/indicators/rsi/{self.stockTicker}?timespan=month&adjusted=true&window=14&series_type=close&order=desc&apiKey={API_KEY}"
        res = requests.get(URL)
        return res.json()['results']['values']

def saveData(data):
    with open(f"data.json","w") as f:
        json.dump(data,f,indent=4)

def currentTime():
    import datetime
    return datetime.datetime.now().strftime("%H:%M:%S")
