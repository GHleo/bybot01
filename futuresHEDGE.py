import tkinter as tk
#from tkinter import messagebox as msg
from datetime import datetime as dt
import threading
import time
import config as cnfg
#import math
import pybit as pb

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
    #print('Qty(short)  cnfg.positSh[0] = ' + str(cnfg.balancesShU[1]/cnfg.costsUP[0]))
    cnfg.positShUp[0] = truncate(cnfg.balancesShU[1] / cnfg.costsUP[0], qtyStep) #calculate count in first position
    print('Qty(short trancate)  cnfg.positSh[0] = ' + str(cnfg.positShUp[0]))
    cnfg.balanceShRatU[0] = round(cnfg.positShUp[0] * cnfg.costsUP[0], 2)  # REWRITE balance after truncate quontity !!!!!!
    cnfg.costTP_ShortU[0] = round(cnfg.costsUP[0]*(1-float(cnfg.shTPfirst[0])/100),cnfg.pricePrc) #cost first TP
    cnfg.costSL_ShortU[0]=round(cnfg.costsUP[0]*(1+float(cnfg.shSLfirst[0])/100),cnfg.pricePrc) #cost first SL
    fee1 = round(cnfg.balanceShRatU[0] * float(feeMarket),4) # fee on market trade, buy and sell
    cnfg.profitsShU[0]=round(cnfg.balanceShRatU[0] - cnfg.positShUp[0] * cnfg.costTP_ShortU[0], 2) #first profit
    cnfg.lossesShU[0]=round(cnfg.positShUp[0] * cnfg.costSL_ShortU[0] - cnfg.balanceShRatU[0], 2) #first loss
    ####### LONG
    #print('cnfg.balancesLngU[1] = ' + str(cnfg.balancesLngU[1]))
    cnfg.balancesLngU[1] = round(cnfg.balancesLngU[1] - fee1 - fee1,2)
    print('cnfg.balancesLngU[1] RW = ' + str(round(cnfg.balancesLngU[1],1)))
    cnfg.positLngUp[0] = truncate(cnfg.balancesLngU[1] / cnfg.costsUP[0], qtyStep)  # calculate count in first position - truncate quantity because of restrictions at futures rules
    #print('Qty(long)  cnfg.positLng[0] = ' + str(cnfg.balancesLngU[1] / cnfg.costsUP[0]))
    print('Qty(long trancate)  cnfg.positLng[0] = ' + str(cnfg.positLngUp[0]))
    cnfg.balanceLngRatU[0] = round(cnfg.positLngUp[0] * cnfg.costsUP[0], 2)  # REWRITE balance after truncate quontity !!!!!!
    cnfg.costTP_LongU[0]=round(cnfg.costsUP[0] * (1 + float(cnfg.lngTPfirst[0]) / 100), cnfg.pricePrc) #cost first TP
    cnfg.costSL_LongU[0]=round(cnfg.costsUP[0] * (1 - float(cnfg.lngSLfirst[0]) / 100), cnfg.pricePrc) #cost first SL !!!!!!!!!!!! TRIGER IN OCO !!!!!!
    fee11 = round(cnfg.balanceLngRatU[0] * float(feeMarket) * float(feeMarket),4) # fee on market trade, buy and sell
    cnfg.profitsLngU[0]=round(cnfg.positLngUp[0] * cnfg.costTP_LongU[0] - cnfg.balanceLngRatU[0], 2) #first profit
    cnfg.lossesLngU[0]=round(cnfg.balanceLngRatU[0] - cnfg.positLngUp[0] * cnfg.costSL_LongU[0], 2) #first loss

def fhUSDM_initDOWN(lblPriceInDn_):
    feeMarket, feeLimit = getFee(cnfg.pair)
    currGb=lastPrice() #get current price
    qprecision, priceScale, tickSize = quantityPrecision(cnfg.pair)
    qtyStep = int(str(qprecision)[::-1].find('.'))
    cnfg.pricePrc = priceScale

    cnfg.costsDn[0]=round(currGb*(1-cnfg.firstInPrcDn[0]/100),priceScale)# cost for short then UP 1th in ($)
    lblPriceInDn_.set(cnfg.costsDn[0])  # view first in $ first cost
    
    #------------------------ 1th trading -------------------------
    ####### SHORT
    cnfg.positShDn[0]=truncate(cnfg.balancesShDn[1]/cnfg.costsDn[0],qtyStep) #calculate count in first position
    cnfg.balanceShRatDn[0] = round(cnfg.positShDn[0] * cnfg.costsDn[0], 2)  # REWRITE balance after truncate quontity !!!!!!
    cnfg.costTP_ShortDn[0]=round(cnfg.costsDn[0]*(1-float(cnfg.shTPfirstDn[0])/100),cnfg.pricePrc) #cost first TP
    cnfg.costSL_ShortDn[0]=round(cnfg.costsDn[0]*(1+float(cnfg.shSLfirstDn[0])/100),cnfg.pricePrc) #cost first SL
    fee1 = round(cnfg.balanceShRatDn[0] * float(feeMarket),4) # fee on market trade, sell
    cnfg.profitsShDn[0]=round(cnfg.balanceShRatDn[0]-cnfg.positShDn[0]*cnfg.costTP_ShortDn[0],2) #first profit
    cnfg.lossesShDn[0]=round(cnfg.positShDn[0]*cnfg.costSL_ShortDn[0] - cnfg.balanceShRatDn[0],2) #first loss
    ####### LONG
    #print('initDown cnfg.balancesLngDn[1] = ' + str(cnfg.balancesLngDn[1]))
    cnfg.balancesLngDn[1] = cnfg.balancesLngDn[1] - fee1
    print('initDown cnfg.balancesLngDn[1] RW = ' + str(round(cnfg.balancesLngDn[1],2)))
    cnfg.positLngDn[0] = truncate(cnfg.balancesLngDn[1] / cnfg.costsDn[0], qtyStep)  # calculate count in first position - truncate quantity because of restrictions at futures rules
    #print('initDown Qty(long)  cnfg.positLngDn[0] = ' + str(cnfg.balancesLngDn[1] / cnfg.costsDn[0]))
    print('initDown Qty(long trancate)  cnfg.positLngDn[0] = ' + str(cnfg.positLngDn[0]))
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
    wallet_balance_total, balanceShort, balanceLong = calculateBalance()

    currGb_ = round(currGb, priceScale)  # cost for short then UP 1th in ($)
    print('initCurrent()  balanceShort: ' + str(balanceShort))
    print('initCurrent()  balanceLong: ' + str(balanceLong))

    #------ Init for Short
    cnfg.positSh[cnfg.loopItems] = truncate(balanceShort * cnfg.levUP / currGb_, qtyStep)  # calculate count for position
    print('initCurrent()  cnfg.positSh[cnfg.loopItems] : ' + str(cnfg.positSh[cnfg.loopItems] ))
    cnfg.costTP_Short[cnfg.loopItems] = round(currGb_ * (1 - float(cnfg.shTPfirst[cnfg.loopItems]) / 100), cnfg.pricePrc) # calculate TP
    cnfg.costSL_Short[cnfg.loopItems] = round(currGb_ * (1 + float(cnfg.shSLfirst[cnfg.loopItems]) / 100), cnfg.pricePrc)  # calculate SL

    #------ Init for Long
    fee1 = round(balanceShort * float(feeMarket), 4)  # fee on market trade, buy and sell
    cnfg.positLng[cnfg.loopItems] = truncate(balanceLong * cnfg.levUP / currGb_, qtyStep)  # calculate count for position
    cnfg.costTP_Long[cnfg.loopItems] = round(currGb_ * (1 + float(cnfg.lngTPfirst[cnfg.loopItems]) / 100), cnfg.pricePrc) # calculate TP
    cnfg.costSL_Long[cnfg.loopItems] = round(currGb_ * (1 - float(cnfg.lngSLfirst[cnfg.loopItems]) / 100), cnfg.pricePrc)  # calculate SL

def fhUSDM_Calculate(CurRt_, TBal_, balUP_, balDn_,balUPt_,balDnT_):
    try:
        switchPM = cnfg.session.switch_position_mode(category="linear", symbol=cnfg.pair, mode=3) #Switch Position Mode
        print('fhUSDM_Calculate() switchPM:  ' + str(switchPM))
    except Exception as e:
        print("fhUSDM_Calculate() Exception!!!!!!!!!!!!!!!!!!!!!!!!!!! {}".format(e))
    try:
        setLeverage = cnfg.session.set_leverage(category="linear",symbol=cnfg.pair, buyLeverage=str(cnfg.levUP),sellLeverage=str(cnfg.levDn))
        print('fhUSDM_Calculate() setLeverage:  ' + str(setLeverage))
    except Exception as e:
        print("fhUSDM_Calculate() Exception!!!!!!!!!!!!!!!!!!!!!!!!!!! {}".format(e))
    quantityPrecision(cnfg.pair)
    lstPrice = lastPrice()
    #print(lstPrice)
    CurRt_.set(lstPrice)
    # get_wallet_balance = cnfg.session.get_wallet_balance(accountType="UNIFIED", coin="USDT")
    # wallet_balance1 = get_wallet_balance['result']['list']
    # wallet_balance2 = wallet_balance1[0]['coin']
    # wallet_balance_total = truncate(float(wallet_balance2[0]['availableToWithdraw']),1)
    # wallet_balance_total = float(wallet_balance[0]['totalWalletBalance'])
    # print('fhUSDM_Calculate: wallet_balance = ' + str(wallet_balance))
    # print('fhUSDM_Calculate: wallet_balance = ' + str(wallet_balance3))
    totalBalance, balanceShort, balanceLong = calculateBalance()

    TBal_.set(totalBalance)

    balUP = round(totalBalance / 2, 1)
    print('fhUSDM_Calculate: balance UP = ' + str(balUP))
    balUP_.set(balUP)
    balUPt = round(balUP * cnfg.levUP, 2)
    print('fhUSDM_Calculate: total balance UP = ' + str(balUPt))
    cnfg.balancesShU[0], cnfg.balancesLngU[0] = balUP,balUP  # initialisation long & short balance for UP
    balUPt_.set(balUPt)
    cnfg.balancesShU[1], cnfg.balancesLngU[1] = balUPt,balUPt  # initialisation long & short balance * leverage for UP

    balDn = round(totalBalance - balUP,1)
    balDnt = round(balDn * cnfg.levDn, 1)
    print('fhUSDM_Calculate: total balance Down = ' + str(balDnt))
    balDn_.set(balDn)      # initialisation balance for DOWN
    cnfg.balancesShDn[0], cnfg.balancesLngDn[0] = balDn, balDn
    balDnT_.set(balDnt)
    cnfg.balancesShDn[1], cnfg.balancesLngDn[1] = balDnt, balDnt

    #shBalT=round(balanceSh*float(cnfg.LevS[0]),2)
def calculateBalance():
    quantityPrecision(cnfg.pair)
    print('' + str(pb.generate_timestamp))
    print('CalculateBalance() volatility: ' + str(cnfg.session.get_historical_volatility(category="option",baseCoin=cnfg.getQuote,period=30)))
    get_wallet_balance = cnfg.session.get_wallet_balance(accountType="UNIFIED", coin="USDT")
    wallet_balance1 = get_wallet_balance['result']['list']
    wallet_balance2 = wallet_balance1[0]['coin']
    wallet_balance_total1 = truncate(float(wallet_balance2[0]['availableToWithdraw']),2)
    print('initDown wallet_balance_total1= ' + str(wallet_balance_total1))
    wallet_balance_total = round(wallet_balance_total1 * (1 - 0.03),2)
    print('initDown wallet_balance_total= ' + str(wallet_balance_total))
    balSh = round(wallet_balance_total / 2, 1)
    balLng = wallet_balance_total - balSh

    return wallet_balance_total, balSh, balLng
@thread
def mainLoop(pb00_, scrMain_, exept_):
    global Pnl_
    while (cnfg.loopItems <= cnfg.trades):
        try:
            mlastPrice = lastPrice()
            #currTrade_.set(cnfg.loopItems)
            #scrMain_.delete(0.1, tk.END)
            scrMain_.insert(tk.END,'\nlast Price: ' + str(mlastPrice) + '; Total PnL: ' + str(cnfg.pnlTotal) + '; Current loop: ' + str(cnfg.loopItems) + '; ' + str(dt.now().strftime('%H:%M:%S')))

            ordersInfo = cnfg.session.get_open_orders(category="linear",symbol=cnfg.pair,openOnly=0,limit=1,)
            ordInfo = ordersInfo["result"]["list"]

            print('ml ordersInfo: ' + str(ordInfo))
            positionInfo = cnfg.session.get_positions(category="linear", symbol=cnfg.pair)

            got_positions = positionInfo["result"]["list"]
            print('ml got_positions: ' + str(got_positions))

            if ordInfo: #if there is pocition set ID for global cnfg.posInfoOrderID
                Pnl_ = 0.0
                positionInfo = cnfg.session.get_positions(category="linear", symbol=cnfg.pair)
                posInfo = positionInfo["result"]["list"]
                print('ml positionInfo in (if ordInfo:): ' + str(positionInfo))
                cnfg.posInfoOrderID = ordInfo[0]['orderId']
                print('ml Position Info -> orderId:  ' + str(ordInfo[0]['orderId']))
                #createdTime = dt.fromtimestamp(int(posInfo[0]['createdTime']) / 1000)
                if posInfo[0]['unrealisedPnl']:
                    print('ml Position Info -> side:  ' + str(posInfo[0]['side']) + '; Pnl: ' + str(posInfo[0]['unrealisedPnl']))
                    Pnl_ += round(float(posInfo[0]['unrealisedPnl']), 3)

                if posInfo[1]['unrealisedPnl']:
                    print('ml Position Info -> side:  ' + str(posInfo[1]['side']) + '; Pnl: ' + str(posInfo[1]['unrealisedPnl']))
                    #scrMain_.insert(tk.END,'\nside: ' + str(posInfo[1]['side']))
                    Pnl_ += round(float(posInfo[1]['unrealisedPnl']), 3)
                scrMain_.insert(tk.END, '\nside 1:  ' + str(posInfo[0]['side']) + '; side 2: ' + str(posInfo[1]['side']))
                scrMain_.insert(tk.END, '\nPnl: ' + str(Pnl_) + '; Total Pnl: ' + str(cnfg.pnlTotal))
            if not ordInfo and cnfg.tradeOpened and (cnfg.loopItems < cnfg.trades): #cnfg.posInfoOrderID:
                initCurrent()  # Initialisation data
                ID_sell, retMsg_sell = createOrder('Sell', cnfg.levUP, cnfg.costTP_Short[cnfg.loopItems], cnfg.costSL_Short[cnfg.loopItems], cnfg.positSh[cnfg.loopItems], exept_)
                print('ml After first trade!!! Pnl_: ' + str(Pnl_))
                print('ml After first trade!!! createOrder(Short) sell ID: ' + str(ID_sell) + '; ' + str(dt.now().strftime('%H:%M:%S')))
                scrMain_.insert(tk.END, '\ncreate Order Short; sell ID: ' + str(ID_sell) + '; ' + str(dt.now().strftime('%H:%M:%S')))
                if retMsg_sell == "OK":
                    ID_buy, retMsg_buy = createOrder('Buy', cnfg.levUP, cnfg.costTP_Long[cnfg.loopItems], cnfg.costSL_Long[cnfg.loopItems], cnfg.positLng[cnfg.loopItems], exept_)
                    print('ml After first trade!!! Pnl_: ' + str(Pnl_))
                    cnfg.pnlTotal += Pnl_
                    print('ml After first trade!!! createOrder(Long) buy ID: ' + str(ID_buy) + '; ' + str(dt.now().strftime('%H:%M:%S')))
                    scrMain_.insert(tk.END, '\ncreate Order Long; buy ID: ' + str(ID_sell) + '; ' + str(dt.now().strftime('%H:%M:%S')))
                    scrMain_.insert(tk.END, '\nTotal Pnl: ' + str(cnfg.pnlTotal))
                    cnfg.UpTrand, cnfg.DnTrand = True, True
                    cnfg.tradeOpened = True
                    cnfg.loopItems += 1
                else:
                    delOrder = cnfg.session.cancel_order(category="linear",symbol=cnfg.pair, orderId=ID_sell)
                    print('!!!!!!!!!!! ml delete order: second trade and more! ')

            #----------- if trend Up
            if (mlastPrice >= cnfg.costsUP[0]) and not cnfg.UpTrand:
                print('ml create order then cost UP!!!!!! ')
                #print('ml create order then cost UP!!!!!! SELL cnfg.positSh[0] = ' + str(cnfg.positShUp[0]))
                ID_sell, retMsg_sell = createOrder('Sell', cnfg.levUP, cnfg.costTP_ShortU[0], cnfg.costSL_ShortU[0], cnfg.positShUp[0], exept_)
                print('ml First trade!!! createOrder(Short) sell ID: ' + str(ID_sell) + '; ' + str(dt.now().strftime('%H:%M:%S')))
                scrMain_.insert(tk.END, '\ncreate Order Short(UP); sell ID: ' + str(ID_sell) + '; ' + str(dt.now().strftime('%H:%M:%S')))
                if retMsg_sell == "OK":
                    #print('ml create order then cost UP!!!!!! BUY cnfg.positLng[0] = ' + str(cnfg.positLngUp[0]))
                    ID_buy, retMsg_buy = createOrder('Buy', cnfg.levUP, cnfg.costTP_LongU[0], cnfg.costSL_LongU[0], cnfg.positLngUp[0], exept_)
                    print('ml First trade!!! createOrder(Long) buy ID: ' + str(ID_buy) + '; ' + str(dt.now().strftime('%H:%M:%S')))
                    scrMain_.insert(tk.END, '\ncreate Order Long(UP); buy ID: ' + str(ID_sell) + '; ' + str(dt.now().strftime('%H:%M:%S')))
                    cnfg.UpTrand, cnfg.DnTrand = True, True
                    cnfg.tradeOpened = True
                    cnfg.loopItems += 1
                else:
                    delOrder = cnfg.session.cancel_order(category="linear",symbol=cnfg.pair, orderId=ID_sell)
                    print('!!!!!!!!!!! ml delete order: if trend Up ')
            # ----------- if trend Down
            if (mlastPrice <= cnfg.costsDn[0] ) and not cnfg.DnTrand:
                print('ml create order then cost Down!!!!!! ')
                #print('ml create order then cost Down!!!!!! BUY cnfg.positShDn[0] = ' + str(cnfg.positShDn[0]))
                ID_sellDn, retMsg_sellDn  = createOrder('Sell', cnfg.levDn, cnfg.costTP_ShortDn[0], cnfg.costSL_ShortDn[0], cnfg.positShDn[0], exept_)
                print('ml First trade!!! create Order(Short) sell ID: ' + str(ID_sellDn) + '; ' + str(dt.now().strftime('%H:%M:%S')))
                scrMain_.insert(tk.END, '\ncreate Order Short(DOWN); sell ID: ' + str(ID_sellDn) + '; ' + str(dt.now().strftime('%H:%M:%S')))
                if retMsg_sellDn == "OK":
                    #print('ml create order then cost Down!!!!!! SELL cnfg.positLngDn[0] = ' + str(cnfg.positLngDn[0]))
                    ID_buyDn, retMsg_buyDn  = createOrder('Buy', cnfg.levDn, cnfg.costTP_LongDn[0], cnfg.costSL_LongDn[0], cnfg.positLngDn[0], exept_)
                    print('ml First trade!!! create Order(Long) buy ID: ' + str(ID_buyDn) + '; ' + str(dt.now().strftime('%H:%M:%S')))
                    scrMain_.insert(tk.END, '\ncreate Order Long(DOWN); buy ID: ' + str(ID_buyDn) + '; ' + str(dt.now().strftime('%H:%M:%S')))
                    cnfg.DnTrand, cnfg.UpTrand = True, True
                    cnfg.tradeOpened = True
                    cnfg.loopItems += 1
                else:
                    delOrder = cnfg.session.cancel_order(category="linear",symbol=cnfg.pair, orderId=ID_sellDn)
                    print('!!!!!!!!!!! ml delete order: if trend Down ')

            thread = threading.Thread(target=run_progressbar(pb00_, cnfg.chVarDelay_GL))
            thread.start()
        except Exception as e:
            exept_.set(str(dt.now().strftime('%H:%M:%S')) +'; mainLoop() Exception! -> '+str(e))
            print("mainLoop() Exception!!!!!!!!!!!!!!!!!!!!!!!!!!! {}".format(e))
            # cnf.log.info("mainLoop(Exception)-> {ex}".format(ex=e))
            time.sleep(3)
            continue

def createOrder(side_, lev_, tp_, sl_, qty_, exept_):
    try:
        print('create Order() side_: ' + str(side_) + '; tp_: ' + str(tp_) + '; sl_: ' + str(sl_) + '; qty_: ' + str(qty_) + '; ' + str(dt.now().strftime('%H:%M:%S')))
        #wBalTot,shBal, shBalT, lngBal, lngBalT, shQty, lngQty = balQty(lPrice_)
        if side_ == 'Sell':
            posIdx = 2
        else:
            posIdx = 1
        responce = cnfg.session.place_order(
            category="linear",
            symbol=str(cnfg.pair),
            side=side_,
            orderType="Market",
            qty=str(qty_),
            #price=str(lPrice_),
            timeInForce="PostOnly",
            isLeverage=lev_,
            # orderFilter="Order",
            takeProfit=str(tp_),
            stopLoss=str(sl_),
            positionIdx=posIdx,  # hedge-mode if 2 - sell, if 1 - Buy side
        )
        return responce["result"]["orderId"], responce["retMsg"]
        # print('BUY Order!!! ', str(responce["retMsg"]))
        # if responce["retMsg"] == "OK":
        #     print('BUY Order is OK? ',responce["result"]["orderId"])
        #     ######## Sell Limit #########
        #     responce2 = cnfg.session.place_order(
        #         category="linear",
        #         symbol="BTCUSDT",
        #         side="Sell",
        #         orderType="Market",
        #         qty="0.002",
        #         timeInForce="GTC",
        #         isLeverage=cnfg.LevS[0],
        #         takeProfit=str(tp_),
        #         stopLoss=str(sl_),
        #         positionIdx=2,  # hedge-mode Sell side
        #     )
        #     print('SELL Order ', responce2["result"]["orderId"])

    except Exception as e:
        exept_.set(str(dt.now().strftime('%H:%M:%S')) +'; createOrder() Exception! -> '+str(e))
        #cnf.log.info("\ncreateOrder(Exception)-> {ex}".format(ex=e))
        print("createOrder() Exception! {}".format(e))

def lastPrice():
    currPrice = cnfg.session.get_tickers(category="inverse", symbol=cnfg.pair)  # get current price
    currPrice2 = currPrice['result']['list']
    lastPrice = float(currPrice2[0]['lastPrice'])
    return lastPrice

# def balQty(lstPrice_): #calculate balance and quntyty for short and long
#     get_wallet_balance = cnfg.session.get_wallet_balance(accountType="UNIFIED", coin="USDT")
#     wallet_balance = get_wallet_balance['result']['list']
#     wallet_balance_total = round(float(wallet_balance[0]['totalWalletBalance']),2)
#     balanceSh = round(wallet_balance_total/2,2)
#     shBalT = round(balanceSh * float(cnfg.LevS[0]), 2) #balance for short * leverage
#     balanceLng = wallet_balance_total - balanceSh
#     lngBalT = round(balanceLng * float(cnfg.LevS[1]), 2) #balance for long * leverage
#     shQty = round(shBalT / float(lstPrice_), 3)
#     lngQty = round(lngBalT / float(lstPrice_), 3)
#
#     return wallet_balance_total,balanceSh, shBalT,balanceLng, lngBalT, shQty, lngQty

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