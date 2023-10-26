import tkinter as tk
#from tkinter import messagebox as msg
from datetime import datetime as dt
import threading
import time
import config as cnfg
import math

from decimal import Decimal

def thread(fn):
    def execute(*args, **kwargs):
        threading.Thread(target=fn, args=args, kwargs=kwargs).start()
    return execute
def run_progressbar(_pb00, delay_):
    _pb00["maximum"] = 100  # 4,5min cccc
    for i in range(100):
        time.sleep(delay_)
        _pb00["value"] = i  # increment progressbar
        _pb00.update()  # have to call update() in loop

def fhUSDM_initUP(lblPriceInUP_):
    #global balanceSh3, balanceSh3Lev, fee3, mc3
    feeMarket, feeLimit = getFee(cnfg.pair)

    currGb=lastPrice() #get current pricel
    #wBalTotal, shBal, shBalT, lngBal, lngBalT, shQty, lngQty = balQty(currGb)
    qprecision, priceScale, tickSize = quantityPrecision(cnfg.pair)
    qtyStep = int(str(qprecision)[::-1].find('.'))
    cnfg.pricePrc = priceScale

    #------------------------ First block in TRADING -------------------------
    cnfg.costsUP[0]=round(currGb*(1+cnfg.firstInPrcUP[0]/100),priceScale)# cost for short then UP 1th in ($)
    # print('fhUSDM_initUP() currGb = ' + str(currGb))
    # print('fhUSDM_initUP() in % cnfg.firstInPrcUP[0] = ' + str(cnfg.firstInPrcUP[0]))
    # print('fhUSDM_initUP() in $ cnfg.costsUP[0] = ' + str(cnfg.costsUP[0]))
    lblPriceInUP_.set(cnfg.costsUP[0])  # view first in $ first cost

    #------------------------ 1th trading -------------------------
    ####### SHORT
    ratio = float(round(1/int(cnfg.CTrades[1]),2)) #Ratio for two trades
    print('\nfhUSDM_initUP() ratio  = ' + str(ratio))
    cnfg.positShUp[0] = truncate(cnfg.balancesShU[1] * ratio / cnfg.costsUP[0], qtyStep) #calculate count in first position
    #cnfg.balanceShRatU[0] = cnf.balancesSh[1]*ratio #balance on first trade Short

    print('fhUSDM_initUP() cnfg.balancesShU[1]  = ' + str(cnfg.balancesShU[1]))
    cnfg.balanceShRatU[0] = round(cnfg.positShUp[0] * cnfg.costsUP[0], 2)  # REWRITE balance after truncate quontity !!!!!!
    print('fhUSDM_initUP()  Qty(short)  cnfg.positShUp[0]  = ' + str(cnfg.positShUp[0]))
    cnfg.costTP_ShortU[0] = round(cnfg.costsUP[0]*(1-float(cnfg.shTPfirst[0])/100),cnfg.pricePrc) #cost first TP
    cnfg.costSL_ShortU[0]=round(cnfg.costsUP[0]*(1+float(cnfg.shSLfirst[0])/100),cnfg.pricePrc) #cost first SL
    fee1 = round(cnfg.balanceShRatU[0] * float(feeMarket),4) # fee on market trade, buy and sell
    cnfg.profitsShU[0]=round(cnfg.balanceShRatU[0] - cnfg.positShUp[0] * cnfg.costTP_ShortU[0], 2) #first profit
    cnfg.lossesShU[0]=round(cnfg.positShUp[0] * cnfg.costSL_ShortU[0] - cnfg.balanceShRatU[0], 2) #first loss

def fhUSDM_initDOWN(lblPriceInDn_):
    feeMarket, feeLimit = getFee(cnfg.pair)
    currGb=lastPrice() #get current price
    qprecision, priceScale, tickSize = quantityPrecision(cnfg.pair)
    qtyStep = int(str(qprecision)[::-1].find('.'))
    cnfg.pricePrc = priceScale

    cnfg.costsDn[0]=round(currGb*(1-cnfg.firstInPrcDn[0]/100),priceScale)# cost for short then UP 1th in ($)
    lblPriceInDn_.set(cnfg.costsDn[0])  # view first in $ first cost
    
    #------------------------ 1th trading -------------------------
    ####### LONG
    ratio = float(round(1/int(cnfg.CTrades[0]),2)) #Ratio for two trades
    print('\nfhUSDM_initDOWN() ratio  = ' + str(ratio))
    cnfg.positLngDn[0] = truncate(cnfg.balancesLngDn[1] * ratio / cnfg.costsDn[0], qtyStep)  # calculate count in first position - truncate quantity because of restrictions at futures rules
    print('\nfhUSDM_initDOWN() cnfg.balancesLngDn[1] = ' + str(round(cnfg.balancesLngDn[1],2)))

    #print('initDown Qty(long)  cnfg.positLngDn[0] = ' + str(cnfg.balancesLngDn[1] / cnfg.costsDn[0]))
    print('fhUSDM_initDOWN() Qty(long)  cnfg.positLngDn[0] = ' + str(cnfg.positLngDn[0]))
    cnfg.balanceLngRatDn[0] = round(cnfg.positLngDn[0] * cnfg.costsDn[0], 2)  # REWRITE balance after truncate quontity !!!!!!
    cnfg.costTP_LongDn[0] = round(cnfg.costsDn[0] * (1 + float(cnfg.lngTPfirstDn[0]) / 100), cnfg.pricePrc) #cost first TP
    cnfg.costSL_LongDn[0]=round(cnfg.costsDn[0] * (1 - float(cnfg.lngSLfirstDn[0]) / 100), cnfg.pricePrc) #cost first SL !!!!!!!!!!!! TRIGER IN OCO !!!!!!
    fee11 = round(cnfg.balanceLngRatDn[0] * float(feeMarket) * float(feeMarket),4) # fee on market trade, buy and sell
    cnfg.profitsLngDn[0]=round(cnfg.positLngDn[0] * cnfg.costTP_LongDn[0] - cnfg.balanceLngRatDn[0],2) #first profit
    cnfg.lossesLngDn[0]=round(cnfg.balanceLngRatDn[0] - cnfg.positLngDn[0] * cnfg.costSL_LongDn[0],2) #first loss

def initCurrent(): #init with second trade and more
    currGb = lastPrice()  # get current price
    feeMarket, feeLimit = getFee(cnfg.pair)
    qprecision, priceScale, tickSize = quantityPrecision(cnfg.pair)
    qtyStep = int(str(qprecision)[::-1].find('.'))
    cnfg.pricePrc = priceScale
    walletBalTotal = calculateBalance()

    currGb_ = round(currGb, priceScale)  # cost for short then UP 1th in ($)
    print('initCurrent()  wallet_balance_total: ' + str(walletBalTotal))

    #------ Init for Short
    cnfg.positSh[cnfg.loopItems] = truncate(walletBalTotal * cnfg.levUP / currGb_, qtyStep)  # calculate count for position
    print('initCurrent()  cnfg.positSh[cnfg.loopItems] : ' + str(cnfg.positSh[cnfg.loopItems] ))
    cnfg.costTP_Short[cnfg.loopItems] = round(currGb_ * (1 - float(cnfg.shTPfirst[cnfg.loopItems]) / 100), cnfg.pricePrc) # calculate TP
    cnfg.costSL_Short[cnfg.loopItems] = round(currGb_ * (1 + float(cnfg.shSLfirst[cnfg.loopItems]) / 100), cnfg.pricePrc)  # calculate SL

    #------ Init for Long
    fee1 = round(walletBalTotal * float(feeMarket), 4)  # fee on market trade, buy and sell
    cnfg.positLng[cnfg.loopItems] = truncate(walletBalTotal * cnfg.levUP / currGb_, qtyStep)  # calculate count for position
    print('initCurrent()  cnfg.positLng[cnfg.loopItems] : ' + str(cnfg.positLng[cnfg.loopItems] ))
    cnfg.costTP_Long[cnfg.loopItems] = round(currGb_ * (1 + float(cnfg.lngTPfirst[cnfg.loopItems]) / 100), cnfg.pricePrc) # calculate TP
    cnfg.costSL_Long[cnfg.loopItems] = round(currGb_ * (1 - float(cnfg.lngSLfirst[cnfg.loopItems]) / 100), cnfg.pricePrc)  # calculate SL

def fhUSDM_Calculate(CurRt_, TBal_, balUPt_,balDnT_):
    try:
        cnfg.session.switch_position_mode(category="linear", symbol=cnfg.pair, mode=0)# mode=3) #Switch Position Mode
        #print('fhUSDM_Calculate() switchPM:  ' + str(switchPM))
    except Exception as e:
        print("fhUSDM_Calculate() Exception!!!!!!!!!!!!!!!!!!!!!!!!!!! {}".format(e))
    try:
        setLeverage = cnfg.session.set_leverage(category="linear",symbol=cnfg.pair, buyLeverage=str(cnfg.levUP),sellLeverage=str(cnfg.levDn))
        print('fhUSDM_Calculate() setLeverage:  ' + str(setLeverage))
    except Exception as e:
        print("fhUSDM_Calculate() Exception!!!!!!!!!!!!!!!!!!!!!!!!!!! {}".format(e))
    quantityPrecision(cnfg.pair)
    lstPrice = lastPrice()
    CurRt_.set(lstPrice)
    totalBalance = calculateBalance()

    TBal_.set(totalBalance)

    balUPt = round(totalBalance * cnfg.levUP, 2)
    print('fhUSDM_Calculate() total balance UP = ' + str(balUPt))
    cnfg.balancesShU[0] = totalBalance  # initialisation long & short balance for UP
    balUPt_.set(balUPt)
    cnfg.balancesShU[1] = balUPt  # initialisation long & short balance * leverage for UP

    balDnt = round(totalBalance * cnfg.levDn, 1)
    print('fhUSDM_Calculate() total balance Down = ' + str(balDnt))
    cnfg.balancesLngDn[0] = totalBalance
    balDnT_.set(balDnt)
    cnfg.balancesLngDn[1] = balDnt

    #shBalT=round(balanceSh*float(cnfg.LevS[0]),2)
def calculateBalance():
    quantityPrecision(cnfg.pair)
    get_wallet_balance = cnfg.session.get_wallet_balance(accountType="UNIFIED", coin="USDT")
    wallet_balance1 = get_wallet_balance['result']['list']
    wallet_balance2 = wallet_balance1[0]['coin']
    wallet_balance_total1 = truncate(float(wallet_balance2[0]['availableToWithdraw']),2)
    wallet_balance_total = round(wallet_balance_total1 ,2)
    print('Wallet_balance_total = ' + str(wallet_balance_total1))

    return wallet_balance_total

@thread
def test(exept_):
    cnfg.orderID_sell, cnfg.retMsg_sell = createOrder('Sell', cnfg.levUP,cnfg.costsUP[0], cnfg.costTP_ShortU[0], cnfg.costSL_ShortU[0],cnfg.positShUp[0], exept_,'LIMIT', 0)
    cnfg.orderID_buy, cnfg.retMsg_buy = createOrder('Buy', cnfg.levDn, cnfg.costsDn[0], cnfg.costTP_LongDn[0], cnfg.costSL_LongDn[0],cnfg.positLngDn[0], exept_,'LIMIT', 0)

    # ordersInfo = cnfg.session.get_open_orders(category="linear", symbol=cnfg.pair, openOnly=0, limit=2)
    # ordersInfo2 = ordersInfo["result"]["list"]
    # print('ordersInfo2: ' + str(ordersInfo2))
    # print('Sell ID: ' + str(ordersInfo2[0]['orderId']))
    # print('Buy ID: ' + str(ordersInfo2[1]['orderId']))
    # delOrder = cnfg.session.cancel_order(category="linear", symbol=cnfg.pair, orderId=cnfg.ID_buyDn)
    # print('ordersInfo delOrder: ' + str(delOrder))
@thread
def mainLoop(pb00_, scrMain_, exept_):
    global Pnl_, lmt_
    Pnl_ = 0.0
    lmt_ = 4
    cnfg.orderID_sell, cnfg.retMsg_sell = createOrder('Sell', cnfg.levUP,cnfg.costsUP[0], cnfg.costTP_ShortU[0], cnfg.costSL_ShortU[0],cnfg.positShUp[0], exept_,'LIMIT', 0)
    cnfg.orderID_buy, cnfg.retMsg_buy = createOrder('Buy', cnfg.levDn, cnfg.costsDn[0], cnfg.costTP_LongDn[0], cnfg.costSL_LongDn[0],cnfg.positLngDn[0], exept_,'LIMIT', 0)
    #cnfg.loopItems += 1
    # ordersInfo = cnfg.session.get_open_orders(category="linear", symbol=cnfg.pair, openOnly=0, limit=2)
    # ordersInfo2 = ordersInfo["result"]["list"]
    scrMain_.insert(tk.END, '\nSell ID: ' + str(cnfg.orderID_sell) + '; Buy ID:: ' + str(cnfg.orderID_buy))
    # print('ordersInfo2: ' + str(ordersInfo2))
    # print('Sell ID: ' + str(ordersInfo2[0]['orderId']))
    # print('Buy ID: ' + str(ordersInfo2[1]['orderId']))
    while cnfg.loopItems <= cnfg.trades:
        try:
            mlastPrice = lastPrice()
            scrMain_.insert(tk.END,'\nPrice: ' + str(mlastPrice) + '; PnL: ' + str(Pnl_) + '; Total PnL: ' + str(cnfg.pnlTotal) + '; Current loop: ' + str(cnfg.loopItems) + '; ' + str(dt.now().strftime('%H:%M:%S')))

            ordersInfo = cnfg.session.get_open_orders(category="linear", symbol=cnfg.pair, openOnly=0, limit=lmt_)
            print('ml ordersInfo: ' + str(ordersInfo))
            ordersInfo2 = ordersInfo["result"]["list"]
            ordInfoLen = len(ordersInfo2)
            firstSellOrder = searchOrder(ordersInfo2, ordInfoLen, cnfg.orderID_sell)
            if not firstSellOrder and not cnfg.isDown: # What trend?
                cnfg.trades = cnfg.CTrades[1]
                cnfg.isUp = True
            print('ml firstSellOrder: ' + str(firstSellOrder))
            firstBuyOrder = searchOrder(ordersInfo2, ordInfoLen, cnfg.orderID_buy)
            if not firstBuyOrder and not cnfg.isUp: # What trend?
                cnfg.trades = cnfg.CTrades[0]
                cnfg.isDown = True

            print('ml firstBuyOrder: ' + str(firstBuyOrder))

            Pnl_ = 0.0
            positionInfo = cnfg.session.get_positions(category="linear", symbol=cnfg.pair)
            print('ml positionInfo: ' + str(positionInfo))
            got_positions = positionInfo["result"]["list"]
            if got_positions[0]['unrealisedPnl']:
                print('ml Position Info -> Pnl: ' + str(got_positions[0]['unrealisedPnl']))
                Pnl_ += round(float(got_positions[0]['unrealisedPnl']), 3)

            positionValue = got_positions[0]['positionValue']
            print('ml got_positions[positionValue]: ' + str(positionValue))
            if not positionValue and (cnfg.loopItems < cnfg.trades): #if position close and need make new order
                cnfg.loopItems += 1
                initCurrent()  # Initialisation data
                print('ml if position over!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! ')
                if cnfg.isUp:
                    cnfg.pnlTotal += Pnl_
                    cnfg.orderID_sell, cnfg.retMsg_sell = createOrder('Sell', cnfg.levUP, cnfg.costsUP[0], cnfg.costTP_ShortU[0], cnfg.costSL_ShortU[0],cnfg.positShUp[0], exept_, 'MARKET', 0)
                    print('ml next trade!  cnfg.orderID_sell: ' + str(cnfg.orderID_sell))
                    scrMain_.insert(tk.END, '\ncreate Order Sell; sell ID: ' + str(cnfg.orderID_sell) + '; ' + str(dt.now().strftime('%H:%M:%S')))
                    scrMain_.insert(tk.END, '\nTotal Pnl: ' + str(cnfg.pnlTotal))
                if cnfg.isDown:
                    cnfg.pnlTotal += Pnl_
                    cnfg.orderID_buy, cnfg.retMsg_buy = createOrder('Buy', cnfg.levDn, cnfg.costsDn[0], cnfg.costTP_LongDn[0], cnfg.costSL_LongDn[0], cnfg.positLngDn[0], exept_, 'MARKET', 0)
                    print('ml next trade!  cnfg.orderID_buy: ' + str(cnfg.orderID_buy))
                    scrMain_.insert(tk.END, '\ncreate Order Buy; buy ID: ' + str(cnfg.orderID_buy) + '; ' + str(dt.now().strftime('%H:%M:%S')))
                    scrMain_.insert(tk.END, '\nTotal Pnl: ' + str(cnfg.pnlTotal))
            if not firstSellOrder and positionInfo and not cnfg.orderSStatus: #if sell(short)
                delBuyOrder = cnfg.session.cancel_order(category="linear", symbol=cnfg.pair, orderId=cnfg.orderID_buy)
                cnfg.orderSStatus = True
                cnfg.orderBStatus = True
                print('ordersInfo delBuyOrder: ' + str(delBuyOrder))
            if not firstBuyOrder and positionInfo and not cnfg.orderBStatus: #if buy(long)
                delSellOrder = cnfg.session.cancel_order(category="linear", symbol=cnfg.pair, orderId=cnfg.orderID_sell)
                cnfg.orderBStatus = True
                cnfg.orderSStatus = True
                print('ordersInfo delSellOrder: ' + str(delSellOrder))

            thread = threading.Thread(target=run_progressbar(pb00_, cnfg.chVarDelay_GL))
            thread.start()
        except Exception as e:
            exept_.set(str(dt.now().strftime('%H:%M:%S')) +'; mainLoop() Exception! -> '+str(e))
            print("mainLoop() Exception!!!!!!!!!!!!!!!!!!!!!!!!!!! {}".format(e))
            # cnf.log.info("mainLoop(Exception)-> {ex}".format(ex=e))
            time.sleep(3)
            continue

def createOrder(side_, lev_, prc_, tp_, sl_, qty_, exept_,type_, posIdx_):
    try:
        print('create Order() side_: ' + str(side_) + '; prc_: ' + str(prc_) +'; tp_: ' + str(tp_) + '; sl_: ' + str(sl_) + '; qty_: ' + str(qty_) + '; ' + str(dt.now().strftime('%H:%M:%S')))
        if type_ == 'LIMIT':
            responce = cnfg.session.place_order(
                category="linear",
                symbol=str(cnfg.pair),
                side=side_,
                orderType="Limit",
                price=prc_,
                qty=str(qty_),
                timeInForce="PostOnly",
                isLeverage=lev_,
                orderFilter="Order",
                takeProfit=str(tp_),
                stopLoss=str(sl_),
                tpslMode='Partial',
                positionIdx=posIdx_,  # hedge-mode if 2 - sell, if 1 - Buy side, 0: one-way mode
            )
            return responce["result"]["orderId"], responce["retMsg"]
        if type_ == 'MARKET':
            responce = cnfg.session.place_order(
                category="linear",
                symbol=str(cnfg.pair),
                side=side_,
                orderType="Market",
                price=prc_,
                qty=str(qty_),
                timeInForce="PostOnly",
                isLeverage=lev_,
                orderFilter="Order",
                takeProfit=str(tp_),
                stopLoss=str(sl_),
                positionIdx=posIdx_,  # hedge-mode if 2 - sell, if 1 - Buy side, 0: one-way mode
            )
            return responce["result"]["orderId"], responce["retMsg"]

    except Exception as e:
        exept_.set(str(dt.now().strftime('%H:%M:%S')) +'; createOrder() Exception! -> '+str(e))
        #cnf.log.info("\ncreateOrder(Exception)-> {ex}".format(ex=e))
        print("createOrder() Exception! {}".format(e))

def lastPrice():
    currPrice = cnfg.session.get_tickers(category="inverse", symbol=cnfg.pair)  # get current price
    currPrice2 = currPrice['result']['list']
    lastPrice = float(currPrice2[0]['lastPrice'])
    return lastPrice

def quantityPrecision(pair_):
    prcsn,qrcsn, tsize = 0,0,0
    info = cnfg.session.get_instruments_info(category="linear", symbol=pair_)
    info2 = info["result"]["list"]
    #print('instruments_info2: ' + str(info2))
    priceScale = int(info2[0]['priceScale'])
    #print('priceScale: ' + str(priceScale))
    priceFilter = info2[0]['priceFilter']
    tsize = priceFilter['tickSize']
    lotSizeFilter = info2[0]['lotSizeFilter']
    qrcsn = lotSizeFilter['qtyStep']
    #print('tickSize: ' + str(tickSize))

    # for x in info['symbols']:
    #     if x['symbol'] == pair_:
    #         qrcsn = int(x['quantityPrecision'])
    #         prcsn = int(x['pricePrecision'])
    #         for f in x['filters']:
    #             if f['filterType'] == 'PRICE_FILTER':
    #                 tsize = float(f['tickSize'])
    return qrcsn, priceScale, tsize

def getTicker(pair_):
    get_tickers = cnfg.session.get_tickers(category="inverse",symbol=pair_)
    result = get_tickers['result']['list']
    fundingRate = result[0]['fundingRate']
    print('Ticker(result): ' +str(result))
    print('Ticker(fundingRate): ' +str(fundingRate))

def getFee(pair_):
    get_fee = cnfg.session.get_fee_rates(symbol=pair_)
    result = get_fee['result']['list']
    feeMarket = result[0]["takerFeeRate"]
    feeLimit = result[0]["makerFeeRate"]
    #print('feeMarket: ' +str(feeMarket))
    #print('feeLimit: ' +str(feeLimit))
    return feeMarket, feeLimit

def truncate(n, decimals=0):
    multiplier = 10 ** decimals
    return int(n * multiplier) / multiplier

def searchOrder(ordersInfo_, lmt_, order_):
    #print('searchOrder(): order_ = ' + str(order_))
    forder = ''
    for i in range(0, lmt_):
        if ordersInfo_[i]['orderId'] == order_:
            forder = ordersInfo_[i]['orderId']
        #     print('searchOrder(): i = ' + str(i) + '; ' + str(forder))
        # print('searchOrder(): i = ' + str(i) + '; lmt_ = ' + str(lmt_)+ '; forder = ' + str(forder))
    return forder