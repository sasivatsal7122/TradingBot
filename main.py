from time import sleep
import configparser

from utils import *

config = configparser.ConfigParser()
config.read('config.ini')

API_KEY = config['Data']['API_KEY']
STOCKER_TICKERS_LIST = config['Data']['stockticker'].split(",")

MASTER_DATA = dict()
def Perc(Price, Percent):
    return ((Price/100)*Percent)+Price
def collectOpen_Close_data(stockerTickerValue):
    oc_data = getOpenandClose(stockerTickerValue)
    return oc_data

def collectSMA_data(stockerTickerValue):
    smaDay_50 = getSMA(stockerTickerValue).getDay(50)
    smaWeek_50 = getSMA(stockerTickerValue).getWeek(50)
    smaDay_200 = getSMA(stockerTickerValue).getDay(200)
    
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
    emaDay_3 = getEMA(stockerTickerValue).getDay(3)
    emaWeek_3 = getEMA(stockerTickerValue).getWeek(3)
    emaMonth_3 = getEMA(stockerTickerValue).getMonth(3)


    emaDay_9 = getEMA(stockerTickerValue).getDay(9)
    emaWeek_9 = getEMA(stockerTickerValue).getWeek(9)
    emaMonth_9 = getEMA(stockerTickerValue).getMonth(9)
    
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
    macd_day = getMACD(stockerTickerValue).getDay()
    macd_week = getMACD(stockerTickerValue).getWeek()
    
    master_macdData = {
        "day":macd_day,
        "week":macd_week
    }
    
    return master_macdData

def collectRSI_data(stockerTickerValue):
    rsi_day = getRSI(stockerTickerValue).getDay()
    rsi_week = getRSI(stockerTickerValue).getWeek()
    rsi_month = getRSI(stockerTickerValue).getMonth()
    
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
    # print(MASTER_DATA)
    print(f"\n=========== Trade Summary ===========\n")
    print(MASTER_DATA[stockerTicker]["open_close"]["symbol"])
    print(f'Price: {MASTER_DATA[stockerTicker]["open_close"]["close"]}')
    Price = MASTER_DATA[stockerTicker]["open_close"]["close"]
    GrowthPerc2 = Perc(Price, 2.5)
    GrowthPerc5 = Perc(Price, 5)
    GrowthPerc7 = Perc(Price, 7.5)
    GrowthPerc10 = Perc(Price, 10)

    # print(f'AAPL Window 50 SMA(Daily): {MASTER_DATA[stockerTicker]["SMA"]["window_50"]["day"]}')
    if MASTER_DATA[stockerTicker]["SMA"]["window_50"]["day"][0]["value"] > MASTER_DATA[stockerTicker]["open_close"]["close"]:
        # print("Market is bearish(50 SMA Daily)")
        if GrowthPerc2 >= MASTER_DATA[stockerTicker]["SMA"]["window_50"]["day"][0]["value"]:
            DSMAScore50 = 10
        elif GrowthPerc5 > MASTER_DATA[stockerTicker]["SMA"]["window_50"]["day"][0]["value"]:
            DSMAScore50 = 7.5
        elif GrowthPerc7 > MASTER_DATA[stockerTicker]["SMA"]["window_50"]["day"][0]["value"]:
            DSMAScore50 = 5
        else:
            DSMAScore50 = 2.5

    else:
        DSMAScore50 = 0
        # print("Market is bullish(50 SMA Daily)")
    # print(f'AAPL Window 50 SMA(Weekly): {MASTER_DATA[stockerTicker]["SMA"]["window_50"]["week"]}')
    if MASTER_DATA[stockerTicker]["SMA"]["window_50"]["week"][0]["value"] > MASTER_DATA[stockerTicker]["open_close"]["close"]:
        # print("Market is bearish(50 SMA Weekly)")
        if GrowthPerc2 >= MASTER_DATA[stockerTicker]["SMA"]["window_50"]["week"][0]["value"]:
            WSMAScore50 = 10
        elif GrowthPerc5 > MASTER_DATA[stockerTicker]["SMA"]["window_50"]["week"][0]["value"]:
            WSMAScore50 = 7.5
        elif GrowthPerc7 > MASTER_DATA[stockerTicker]["SMA"]["window_50"]["week"][0]["value"]:
            WSMAScore50 = 5
        else:
            WSMAScore50 = 2.5

    else:
        # print("Market is bullish(50 SMA Weekly)")
        WSMAScore50 = 0
    # print(f'AAPL Window 200 SMA(Daily): {MASTER_DATA[stockerTicker]["SMA"]["window_200"]["day"]}')
    if MASTER_DATA[stockerTicker]["SMA"]["window_200"]["day"][0]["value"] > MASTER_DATA[stockerTicker]["open_close"]["close"]:
        # print("Market is bearish(200 SMA Daily)")
        if GrowthPerc2 >= MASTER_DATA[stockerTicker]["SMA"]["window_200"]["day"][0]["value"]:
            DSMAScore200 = 10
        elif GrowthPerc5 > MASTER_DATA[stockerTicker]["SMA"]["window_200"]["day"][0]["value"]:
            DSMAScore200 = 7.5
        elif GrowthPerc7 > MASTER_DATA[stockerTicker]["SMA"]["window_200"]["day"][0]["value"]:
            DSMAScore200 = 5
        else:
            DSMAScore200 = 2.5
    else:
        # print("Market is bullish(200 SMA Daily)")
        DSMAScore200 = 0

    if MASTER_DATA[stockerTicker]["EMA"]["window_3"]["day"][0]["value"] >= MASTER_DATA[stockerTicker]["open_close"]["close"]:
        # print("Market is bearish(EMA Daily Window 3)")
        if Price == MASTER_DATA[stockerTicker]["EMA"]["window_3"]["day"][0]["value"]:
            DEMA3Score = 5
        else:
            DEMA3Score = 0
    else:
        # print("Market is bullish(EMA Daily Window 3)")
        DEMA3Score = 10

    if MASTER_DATA[stockerTicker]["EMA"]["window_3"]["week"][0]["value"] >= MASTER_DATA[stockerTicker]["open_close"]["close"]:
        # print("Market is bearish(EMA Weekly Window 3)")
        if Price == MASTER_DATA[stockerTicker]["EMA"]["window_3"]["week"][0]["value"]:
            WEMA3Score = 5
        else:
            WEMA3Score = 0
    else:
        # print("Market is bullish(EMA Weekly Window 3)")
        WEMA3Score = 10

    if MASTER_DATA[stockerTicker]["EMA"]["window_3"]["month"][0]["value"] >= MASTER_DATA[stockerTicker]["open_close"]["close"]:
        # print("Market is bearish(EMA Monthly Window 3)")
        if Price == MASTER_DATA[stockerTicker]["EMA"]["window_3"]["month"][0]["value"]:
            MEMA3Score = 5
        else:
            MEMA3Score = 0
    else:
        # print("Market is bullish(EMA Monthly Window 3)")
        MEMA3Score = 10

    if MASTER_DATA[stockerTicker]["EMA"]["window_9"]["day"][0]["value"] >= MASTER_DATA[stockerTicker]["open_close"]["close"]:
        # print("Market is bearish(EMA Daily Window 9)")
        if Price == MASTER_DATA[stockerTicker]["EMA"]["window_9"]["week"][0]["value"]:
            DEMA9Score = 5
        else:
            DEMA9Score = 0
    else:
        # print("Market is bullish(EMA Daily Window 9)")
        DEMA9Score = 10

    if MASTER_DATA[stockerTicker]["EMA"]["window_9"]["week"][0]["value"] >= MASTER_DATA[stockerTicker]["open_close"]["close"]:
        # print("Market is bearish(EMA Weekly Window 9)")
        if Price == MASTER_DATA[stockerTicker]["EMA"]["window_9"]["week"][0]["value"]:
            WEMA9Score = 5
        else:
            WEMA9Score = 0
    else:
        # print("Market is bullish(EMA Weekly Window 9)")
        WEMA9Score = 10


    if MASTER_DATA[stockerTicker]["EMA"]["window_9"]["month"][0]["value"] >= MASTER_DATA[stockerTicker]["open_close"]["close"]:
        # print("Market is bearish(EMA Monthly Window 9)")
        if Price == MASTER_DATA[stockerTicker]["EMA"]["window_9"]["month"][0]["value"]:
            MEMA9Score = 5
        else:
            MEMA9Score = 0
    else:
        # print("Market is bullish(EMA Monthly Window 9)")
        MEMA9Score = 10
    HistogramD = MASTER_DATA[stockerTicker]["MACD"]["day"][0]["histogram"]
    HistogramW = MASTER_DATA[stockerTicker]["MACD"]["week"][0]["histogram"]
    if MASTER_DATA[stockerTicker]["MACD"]["day"][0]["histogram"]<0:
        # print("Market is bearish(MACD Daily)")
        DMACD = 0
    else:
        # print("Market is bullish(MACD Daily)")
        if HistogramD < 0.25:
            DMACD = 10
        elif HistogramD < 0.5:
            DMACD = 7.5
        elif HistogramD < 0.75:
            DMACD = 5
        else:
            DMACD = 2.5

    if MASTER_DATA[stockerTicker]["MACD"]["week"][0]["histogram"]<0:
        # print("Market is bearish(MACD Weekly)")
        WMACD = 0
    else:
        # print("Market is bullish(MACD Weekly)")
        if HistogramW < 0.25:
            WMACD = 10
        elif HistogramW < 0.5:
            WMACD = 7.5
        elif HistogramW < 0.75:
            WMACD = 5
        else:
            WMACD = 2.5

    if MASTER_DATA[stockerTicker]["RSI"]["day"][0]["value"] > 70:
        # print("Overbought(RSI)")
        DRSIScore = 10
    elif MASTER_DATA[stockerTicker]["RSI"]["day"][0]["value"] < 30:
        # print("Oversold(RSI Daily)")
        DRSIScore = 0
    elif MASTER_DATA[stockerTicker]["RSI"]["day"][0]["value"] > 30 and MASTER_DATA[stockerTicker]["RSI"]["day"][0]["value"] < 40:
        # print("Buy Zone(RSI Daily)")
        DRSIScore = 7.5
    elif MASTER_DATA[stockerTicker]["RSI"]["day"][0]["value"] > 60 and MASTER_DATA[stockerTicker]["RSI"]["day"][0]["value"] < 70:
        # print("Sell Zone(RSI Daily)")
        DRSIScore = 2.5
    else:
        # print("Market is neutral(RSI Daily)")
        DRSIScore = 5

    if MASTER_DATA[stockerTicker]["RSI"]["week"][0]["value"] > 70:
        # print("Overbought(RSI Weekly)")
        WRSIScore = 10
    elif MASTER_DATA[stockerTicker]["RSI"]["week"][0]["value"] < 30:
        # print("Oversold(RSI Weekly)")
        WRSIScore = 0
    elif MASTER_DATA[stockerTicker]["RSI"]["week"][0]["value"] > 30 and MASTER_DATA[stockerTicker]["RSI"]["week"][0]["value"] < 40:
        # print("Buy Zone(RSI Weekly)")
        WRSIScore = 7.5
    elif MASTER_DATA[stockerTicker]["RSI"]["week"][0]["value"] > 60 and MASTER_DATA[stockerTicker]["RSI"]["week"][0]["value"] < 70:
        # print("Sell Zone(RSI Weekly)")
        WRSIScore = 2.5
    else:
        # print("Market is neutral(RSI Weekly)")
        WRSIScore = 5

    if MASTER_DATA[stockerTicker]["RSI"]["month"][0]["value"] > 70:
        # print("Overbought(RSI Monthly)")
        MRSIScore = 10
    elif MASTER_DATA[stockerTicker]["RSI"]["month"][0]["value"] < 30:
        # print("Oversold(RSI Monthly)")
        MRSIScore = 0
    elif MASTER_DATA[stockerTicker]["RSI"]["month"][0]["value"] > 30 and MASTER_DATA[stockerTicker]["RSI"]["month"][0]["value"] < 40:
        # print("Buy Zone(RSI Monthly)")
        MRSIScore = 7.5
    elif MASTER_DATA[stockerTicker]["RSI"]["month"][0]["value"] > 60 and MASTER_DATA[stockerTicker]["RSI"]["month"][0]["value"] < 70:
        # print("Sell Zone(RSI Monthly)")
        MRSIScore = 2.5
    else:
        # print("Market is neutral(RSI Monthly)")
        MRSIScore = 5

    DailyScorePercentEMA3SMA50 = ((DSMAScore50 + DEMA3Score + DMACD + DRSIScore)/40)*100
    DailyScorePercentEMA3SMA200 = ((DSMAScore200 + DEMA3Score + DMACD + DRSIScore)/40)*100
    DailyScorePercentEMA9SMA50 = ((DEMA9Score + DMACD + DRSIScore + DSMAScore50)/40)*100
    DailyScorePercentEMA9SMA200 = ((DEMA9Score + DMACD + DRSIScore + DSMAScore200)/40)*100
    WeeklyScorePercentEMA3SMA50 = ((WSMAScore50 + WEMA3Score + WMACD + WRSIScore)/40)*100
    WeeklyScorePercentEMA9SMA50 = ((WEMA9Score + WMACD + WRSIScore + WSMAScore50)/40)*100
    MonthlyScorePercentEMA3 = ((MEMA3Score + MRSIScore)/20)*100
    MonthlyScorePercentEMA9 = ((MEMA9Score + MRSIScore)/20)*100
    # print(f'DSMAScore50:{DSMAScore50}   DEMA3Score:{DEMA3Score}   DMACD:{DMACD}   DRSIScore:{DRSIScore}')
    print(f"\n=========== Trade Score ===========\n")
    print(f"Daily Score Percent(SMA 50 & EMA 3): {DailyScorePercentEMA3SMA50}%")
    # print(f"DSMAScore50:{DSMAScore50}   DEMA3Score:{DEMA3Score}   DMACD:{DMACD}   DRSIScore:{DRSIScore}")
    print(f"Daily Score Percent(SMA 200 & EMA 3): {DailyScorePercentEMA3SMA200}%")
    # print(f"DSMAScore200:{DSMAScore200}  DEMA3Score:{DEMA3Score}   DMACD:{DMACD}   DRSIScore:{DRSIScore}")
    print(f"Daily Score Percent(SMA 50 & EMA 9): {DailyScorePercentEMA9SMA50}%")
    # print(f"DSMAScore50:{DSMAScore50}   DEMA9Score:{DEMA9Score}   DMACD:{DMACD}   DRSIScore:{DRSIScore}")
    print(f"Daily Score Percent(SMA 200 & EMA 9): {DailyScorePercentEMA9SMA200}%")
    # print(f"DSMAScore200:{DSMAScore200}  DEMA9Score:{DEMA9Score}   DMACD:{DMACD}   DRSIScore:{DRSIScore}")
    print(f"Weekly Score Percent(SMA 50 & EMA 3): {WeeklyScorePercentEMA3SMA50}%")
    # print(f"WSMAScore50:{WSMAScore50}  WEMA3Score:{WEMA3Score}   WMACD:{WMACD}   WRSIScore:{WRSIScore}")
    print(f"Weekly Score Percent(SMA 50 & EMA 9): {WeeklyScorePercentEMA9SMA50}%")
    # print(f"WSMAScore50:{WSMAScore50}  WEMA9Score:{WEMA9Score}   WMACD:{WMACD}   WRSIScore:{WRSIScore}")
    print(f"Monthly Score Percent(EMA 3): {MonthlyScorePercentEMA3}%")
    # print(f"MEMA3Score:{MEMA3Score}   MRSIScore:{MRSIScore}")
    print(f"Monthly Score Percent(EMA 9): {MonthlyScorePercentEMA9}%")
    # print(f"MEMA9Score:{MEMA9Score}   MRSIScore:{MRSIScore}")
    print(f"\n=========== Trade Score ===========\n")
