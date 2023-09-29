from time import sleep
import configparser

from utils import *

config = configparser.ConfigParser()
config.read('config.ini')

API_KEY = config['Data']['API_KEY']
STOCKER_TICKERS_LIST = config['Data']['stockticker'].split(",")

MASTER_DATA = dict()

def collectOpen_Close_data(stockerTickerValue):
    oc_data = getOpenandClose(stockerTickerValue);sleep(13)
    return oc_data

def collectSMA_data(stockerTickerValue):
    smaDay_50 = getSMA(stockerTickerValue).getDay(50);sleep(13)
    smaWeek_50 = getSMA(stockerTickerValue).getWeek(50);sleep(13)
    smaDay_200 = getSMA(stockerTickerValue).getDay(200);sleep(13)
    
    master_smaData = {
        "window_50":{
            "day":smaDay_50,
            "week":smaWeek_50
        },
        "window_200":{
            "day":smaDay_200
        }
    }
    
    return master_smaData

def collectEMA_data(stockerTickerValue):
    emaDay_3 = getEMA(stockerTickerValue).getDay(3);sleep(13)
    emaWeek_3 = getEMA(stockerTickerValue).getWeek(3);sleep(13)
    emaMonth_3 = getEMA(stockerTickerValue).getMonth(3);sleep(13)


    emaDay_9 = getEMA(stockerTickerValue).getDay(9);sleep(13)
    emaWeek_9 = getEMA(stockerTickerValue).getWeek(9);sleep(13)
    emaMonth_9 = getEMA(stockerTickerValue).getMonth(9);sleep(13)
    
    master_emaData = {
        "window_3":{
            "day":emaDay_3,
            "week":emaWeek_3,
            "month":emaMonth_3
        },
        "window_9":{
            "day":emaDay_9,
            "week":emaWeek_9,
            "month":emaMonth_9
        }
    }
    
    return master_emaData


def collectMACD_data(stockerTickerValue):
    macd_day = getMACD(stockerTickerValue).getDay();sleep(13)
    macd_week = getMACD(stockerTickerValue).getWeek();sleep(13)
    
    master_macdData = {
        "day":macd_day,
        "week":macd_week
    }
    
    return master_macdData

def collectRSI_data(stockerTickerValue):
    rsi_day = getRSI(stockerTickerValue).getDay();sleep(13)
    rsi_week = getRSI(stockerTickerValue).getWeek();sleep(13)
    rsi_month = getRSI(stockerTickerValue).getMonth();sleep(13)
    
    master_rsiData = {
        "day":rsi_day,
        "week":rsi_week,
        "month":rsi_month
    }
    
    return master_rsiData

def collectData(stockerTickerValue):
    print("started collecting open/close data....")
    OPEN_CLOSE_DATA = collectOpen_Close_data(stockerTickerValue)
    
    print("started collecting SMA data....")
    SMA_DATA = collectSMA_data(stockerTickerValue)
    
    print("started collecting EMA data....")
    EMA_DATA = collectEMA_data(stockerTickerValue)
    
    print("started collecting MACD data....")
    MACD_DATA = collectMACD_data(stockerTickerValue)
    
    print("started collecting RSI data....")
    RSI_DATA = collectRSI_data(stockerTickerValue)
    print("finished collecting data....")
    
    combinedMaster_data = {
        stockerTickerValue:{
            "open_close": OPEN_CLOSE_DATA,
            "SMA": SMA_DATA,
            "EMA": EMA_DATA,
            "MACD": MACD_DATA,
            "RSI": RSI_DATA
            
        }
    }
    
    return combinedMaster_data

if __name__=="__main__":
    for stockerTicker in STOCKER_TICKERS_LIST:
        print(f"\n=========== {currentTime()} ===========\n")
        print(f"Collecting Data for {stockerTicker}\n")
        data = collectData(stockerTicker)
        print(f"\nFinished Collecting Data for {stockerTicker}")
        
        MASTER_DATA.update(data)
    print("Saving Data....")
    saveData(MASTER_DATA)
    print("Finished Saving Data....")
