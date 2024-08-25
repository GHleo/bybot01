
from Key import api_secret, api_key
#import requests
from pybit.unified_trading import HTTP
#from pybit import helpers
import logging
import os

Accounts = ['Unified Trading', 'Funding']

session = HTTP(
    testnet=False,
    api_key=api_key,
    api_secret=api_secret,
)
# ws = WebSocket(
#     testnet=True,
#     channel_type="private",
#     api_key=api_key,
#     api_secret=api_secret,
# )

loopItems = 0 #Count for mainLoop
trades = 2 #Total trades
levUP, levDn = 0,0
posInfoOrderID = ''
pnlTotal = 0.00

chVarDelay_GL = 0.5

pair = '' # pair - for trading
base = ['USDT', 'BUSD']
quote = ['BTC', 'ETH', 'BNB', 'SOL', 'WLD', 'AVAX', 'GMT', 'TRX', 'MATIC','ALGO','IOTA','XEM','CAKE','DOGE']
getQuote = ''
init = False
calculate = False
UpTrand, DnTrand = False, False
tradeOpened = False
cntTrades = ['0', '1', '2', '3', '4'] # for count trades
CTrades = [0,0] # get count for trades 0-long, 1-short
#crrTrades = [0,0] # Current trades for short and long
ratioSh, ratioLn = 1, 1
firstIn = ['0','0.05','0.1','0.2','0.3','0.4','0.5','0.6','0.7','0.8','1','1.2','1.4','1.5','1.75','2','2.5','3']
#firstInLng = ['0','0.1','0.25','0.5','1','1.5','1.75','2','2.5','3','3.5','4','5','6','7','8','9','10','15','20']
lev= ['2', '3', '4', '5','6','7','8','9','10','15','20','25','30','35','40','45','50','100']
#LevS=[0,0] # get count for lev 0-short, 1-long
TBal=[0,0] # get count for lev 0-short, 1-long

#costTP_ShortU, costSL_ShortU = [0, 0], [0, 0] # Costs TP and SL for  short
#costTP_LongU, costSL_LongU = [0, 0], [0, 0] # Costs TP and SL for long
#costTP_ShortDn, costSL_ShortDn = [0, 0], [0, 0] # Costs TP and SL for  short
#costTP_LongDn, costSL_LongDn = [0,0,0,0], [0,0,0,0] # Costs TP and SL for long
costTP_Short, costSL_Short = [0, 0, 0, 0], [0, 0, 0, 0] # Costs TP and SL for  short
costTP_Long, costSL_Long = [0,0,0,0], [0,0,0,0] # Costs TP and SL for long
lossesLngU, profitsLngU = [0,0,0,0], [0,0,0,0] # losses and profits for long then UP
lossesLngDn, profitsLngDn = [0,0,0,0], [0,0,0,0] # losses and profits for long then Down
# = [0.0, 0.0]  # 0-initial balance, 1-balance * leverage then UP
balanceShRatU, balanceLngRatU = [0,0,0,0],[0,0,0,0] #balances per Ratio
#balancesShDn, balancesLngDn = [0.0, 0.0],[0.0, 0.0] # 0-initial balance, 1-balance * leverage then DONW
balanceShOnLev, balanceLnOnLev = 0.0, 0.0
balanceShRatDn, balanceLngRatDn = [0,0,0,0],[0,0,0,0] #balances per Ratio
#balancesShRatio, balancesLngRatio = [0,0,0,0],[0,0,0,0] #balances per Ratio
positLngUp, positShUp = [0, 0], [0, 0] #positions in trades then UP
positLngDn,positShDn = [0, 0], [0, 0] #positions in trades then Down
positLng,positSh = [0, 0, 0, 0], [0, 0, 0, 0] #positions in trades then Down
lossesShU, profitsShU = [0, 0, 0, 0], [0, 0, 0, 0] # losses and profits for short then UP
lossesShDn, profitsShDn = [0, 0, 0, 0], [0, 0, 0, 0] # losses and profits for short then Down
costsUP, costsDn = [0,0,0,0], [0,0,0,0] # Costs pair(first in) for long and short then UP and Down
#lngCheck, shCheck = 0,0 #Check box for Long or Short
pricePrc = 0 #price precision

shTPfirst = [0,0,0,0] # profit (%) for Short for UP
shSLfirst = [0,0,0,0] # stop loss (%) for Short for UP
lngTPfirst = [0,0,0,0] # profit (%) for Short for UP
lngSLfirst = [0,0,0,0] # stop loss (%) for Long for UP

shTPfirstDn = [0,0,0,0] # profit (%) for Short then Down
shSLfirstDn = [0,0,0,0] # stop loss (%) for Short then Down
lngTPfirstDn = [0,0,0,0] # profit (%) for Short then Down
lngSLfirstDn = [0,0,0,0] # stop loss (%) for Long then Donw

firstInPrcUP = [0.0] # first in (%) then UP
firstInPrcDn = [0.0] # first in (%) then Down


orderID_buy, orderID_sellTP, orderID_sellSL = 'null', 'null', 'null' # id order for Long
orderID_sell, orderID_buyTP, orderID_buySL = 'null', 'null', 'null' # id order for Short
retMsg_sell, retMsg_buy = '','' #get status orders
#orderSStatus, orderBStatus = False, False
isUp, isDown = True, True

orderCostLn = 0.0 # Current cost then order create for Long
orderCostDn = 0.0 # Current cost then order create for Short

iOrder = 0 # count fo order
iTimesTS = 0 # count for move cost of take profit and stop loss

# Подключаем логирование
logging.basicConfig(
    format="%(asctime)s [%(levelname)-5.5s] %(message)s",
    level=logging.INFO,
    handlers=[
        logging.FileHandler("{path}/logs/{fname}.log".format(path=os.path.dirname(os.path.abspath(__file__)), fname="tradeLog")),
        logging.StreamHandler()])
log = logging.getLogger('')

##