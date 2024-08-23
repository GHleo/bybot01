import tkinter as tk
#from tkinter import messagebox as msg
from datetime import datetime as dt
import threading
import time
import config as cnfg
import math

#from decimal import Decimal

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
    #feeMarket, feeLimit = getFee(cnfg.pair)

    currGb=lastPrice() #get current pricel
    #wBalTotal, shBal, shBalT, lngBal, lngBalT, shQty, lngQty = balQty(currGb)
    qprecision, priceScale, tickSize = quantityPrecision(cnfg.pair)
    qtyStep: int = int(str(qprecision)[::-1].find('.'))
    cnfg.pricePrc = priceScale

    #------------------------ First block in TRADING -------------------------
    cnfg.costsUP[0]=round(currGb*(1+cnfg.firstInPrcUP[0]/100),priceScale)# cost for short then UP 1th in ($)
    # print('fhUSDM_initUP() currGb = ' + str(currGb))
    # print('fhUSDM_initUP() in % cnfg.firstInPrcUP[0] = ' + str(cnfg.firstInPrcUP[0]))
    # print('fhUSDM_initUP() in $ cnfg.costsUP[0] = ' + str(cnfg.costsUP[0]))
    lblPriceInUP_.set(cnfg.costsUP[0])  # view first in $ first cost

    #------------------------ 1th trading -------------------------
    ####### SHORT
    cnfg.ratioSh = float(round(1/int(cnfg.CTrades[1]),2)) #Ratio for first
    print('\nfhUSDM_initUP() Short ratioSh: ' + str(cnfg.ratioSh)+ '; cnfg.loopItems: ' + str(cnfg.loopItems))
    cnfg.balanceShOnLev = cnfg.balanceShOnLev * cnfg.ratioSh
    print('fhUSDM_initUP() Short cnfg.balanceShOnLev] * ratio  = ' + str(cnfg.balanceShOnLev))
    cnfg.positShUp[0] = truncate(cnfg.balanceShOnLev / cnfg.costsUP[0], qtyStep) #calculate count in first position
    #cnfg.positShUp[0] = round_up(cnfg.balanceShOnLev / cnfg.costsUP[0], qtyStep) # calculate count in first position

    #cnfg.balanceShRatU[0] = cnf.balancesSh[1]*ratio #balance on first trade Short

    #cnfg.balanceShRatU[0] = round(cnfg.positShUp[0] * cnfg.costsUP[0], 2)  # REWRITE balance after truncate quontity !!!!!!
    print('fhUSDM_initUP()  Qty(short)  cnfg.positShUp[0]  = ' + str(cnfg.positShUp[0]))
    cnfg.costTP_ShortU[0] = round(cnfg.costsUP[0]*(1-float(cnfg.shTPfirst[0])/100),cnfg.pricePrc) #cost first TP
    cnfg.costSL_ShortU[0]=round(cnfg.costsUP[0]*(1+float(cnfg.shSLfirst[0])/100),cnfg.pricePrc) #cost first SL
    # fee1 = round(cnfg.balanceShRatU[0] * float(feeMarket),4) # fee on market trade, buy and sell
    # cnfg.profitsShU[0]=round(cnfg.balanceShRatU[0] - cnfg.positShUp[0] * cnfg.costTP_ShortU[0], 2) #first profit
    # cnfg.lossesShU[0]=round(cnfg.positShUp[0] * cnfg.costSL_ShortU[0] - cnfg.balanceShRatU[0], 2) #first loss

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
    cnfg.ratioLn = float(round(1/int(cnfg.CTrades[0]),2)) #Ratio for first
    print('\nfhUSDM_initDOWN Long ratioLng: ' + str(cnfg.ratioLn)+ '; cnfg.loopItems: ' + str(cnfg.loopItems))
    cnfg.balanceLnOnLev = round(cnfg.balanceLnOnLev * cnfg.ratioLn,2)
    print('fhUSDM_initDOWN() Long cnfg.balanceLnOnLev] * ratio = ' + str(cnfg.balanceLnOnLev))
    cnfg.positLngDn[0] = truncate(cnfg.balanceLnOnLev / cnfg.costsDn[0], qtyStep)  # calculate count in first position - truncate quantity because of restrictions at futures rules
    #cnfg.positLngDn[0] = round_up(cnfg.balanceLnOnLev / cnfg.costsDn[0],qtyStep)  # calculate count in first position - truncate quantity because of restrictions at futures rules
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
    walletBalTotal1 = calculateBalance()
    walletBalTotal = round(walletBalTotal1 * (1 - 0.01),2)

    currGb_ = round(currGb, priceScale)  # cost for short then UP 1th in ($)
    print('initCurrent()  wallet_balance_total1: ' + str(walletBalTotal1) + '; wallet_balance_total: ' + str(walletBalTotal))

    #------ Init for Short
    ratioShCrr = cnfg.ratioSh * cnfg.loopItems #initial rate multiply on currnt step
    # if cnfg.CTrades[1] != cnfg.loopItems: #exclude division by zero
    #     ratioShCrr = float(round(1/int(cnfg.CTrades[1]-cnfg.loopItems),2)) #Ratio for current
    walletBalTotal = round(walletBalTotal * ratioShCrr,2)
    print('initCurrent() Short ratioShCrr: ' + str(ratioShCrr) + '; cnfg.loopItems: ' + str(cnfg.loopItems))
    print('initCurrent() Short wallet_balance_total * ratio: ' + str(walletBalTotal))
    #cnfg.positSh[cnfg.loopItems] = round_up(walletBalTotal * cnfg.levUP / currGb_, qtyStep)  # calculate count for position
    cnfg.positSh[cnfg.loopItems] = truncate(walletBalTotal * cnfg.levUP / currGb_,qtyStep)  # calculate count for position
    positSh = walletBalTotal * cnfg.levUP / currGb_
    print('initCurrent()  positLng: ' + str(positSh) + '; qtyStep: ' + str(qtyStep))
    print('initCurrent()  cnfg.positSh[cnfg.loopItems] : ' + str(cnfg.positSh[cnfg.loopItems] ))
    cnfg.costTP_Short[cnfg.loopItems] = round(currGb_ * (1 - float(cnfg.shTPfirst[cnfg.loopItems]) / 100), cnfg.pricePrc) # calculate TP
    cnfg.costSL_Short[cnfg.loopItems] = round(currGb_ * (1 + float(cnfg.shSLfirst[cnfg.loopItems]) / 100), cnfg.pricePrc)  # calculate SL

    #------ Init for Long
    ratioLngCrr = cnfg.ratioLn * cnfg.loopItems #initial rate multiply on currnt step
    # if cnfg.CTrades[0] != cnfg.loopItems: #exclude division by zero
    #     ratioLngCrr = float(round(1/int(cnfg.CTrades[0]-cnfg.loopItems),2)) #Ratio for current
    walletBalTotal = round(walletBalTotal * ratioLngCrr,2)
    print('initCurrent() Long ratioLngCrr: ' + str(ratioLngCrr) + '; cnfg.loopItems: ' + str(cnfg.loopItems))
    print('initCurrent() Long  wallet_balance_total * ratio: ' + str(walletBalTotal))
    fee1 = round(walletBalTotal * float(feeMarket), 4)  # fee on market trade, buy and sell
    cnfg.positLng[cnfg.loopItems] = truncate(walletBalTotal * cnfg.levUP / currGb_, qtyStep)  # calculate count for position
    positLng = walletBalTotal * cnfg.levUP  / currGb_ # calculate count for position
    print('initCurrent()  positLng: ' + str(positLng) + '; qtyStep: ' + str(qtyStep))
    print('initCurrent()  cnfg.positLng[cnfg.loopItems] : ' + str(cnfg.positLng[cnfg.loopItems]))
    cnfg.costTP_Long[cnfg.loopItems] = round(currGb_ * (1 + float(cnfg.lngTPfirstDn[cnfg.loopItems]) / 100), cnfg.pricePrc) # calculate TP
    cnfg.costSL_Long[cnfg.loopItems] = round(currGb_ * (1 - float(cnfg.lngSLfirstDn[cnfg.loopItems]) / 100), cnfg.pricePrc)  # calculate SL

def fhUSDM_Calculate(CurRt_, TBal_, balUPt_,balDnT_): # First init
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

    cnfg.balanceShOnLev = round(totalBalance * cnfg.levUP, 1)
    balUPt_.set(cnfg.balanceShOnLev )
    cnfg.balanceLnOnLev = round(totalBalance * cnfg.levDn, 1)
    balDnT_.set(cnfg.balanceLnOnLev)

def calculateBalance():
    quantityPrecision(cnfg.pair)
    get_wallet_balance = cnfg.session.get_wallet_balance(accountType="UNIFIED", coin="USDT")
    wallet_balance1 = get_wallet_balance['result']['list']
    wallet_balance2 = wallet_balance1[0]['coin']
    wallet_balance_total1 = truncate(float(wallet_balance2[0]['availableToWithdraw']),1)
    wallet_balance_total = round(wallet_balance_total1 ,1)
    print('calculateBalance() Wallet_balance_total = ' + str(wallet_balance_total1))

    return wallet_balance_total

def mainLoop(pb00_, scrMain_, exept_):
    global Pnl_, lmt_
    Pnl_ = 0.00
    lmt_ = 4
    cnfg.orderID_sell, cnfg.retMsg_sell = createOrder('Sell', cnfg.levUP,cnfg.costsUP[0], cnfg.costTP_ShortU[0], cnfg.costSL_ShortU[0],cnfg.positShUp[0], exept_,'LIMIT', 0)
    cnfg.orderCostDn = cnfg.costsUP[0]
    cnfg.orderID_buy, cnfg.retMsg_buy = createOrder('Buy', cnfg.levDn, cnfg.costsDn[0], cnfg.costTP_LongDn[0], cnfg.costSL_LongDn[0],cnfg.positLngDn[0], exept_,'LIMIT', 0)
    cnfg.orderCostLn = cnfg.costsDn[0]
    cnfg.loopItems += 1
    # ordersInfo = cnfg.session.get_open_orders(category="linear", symbol=cnfg.pair, openOnly=0, limit=2)
    # ordersInfo2 = ordersInfo["result"]["list"]
    scrMain_.insert(tk.END, '\nSell ID: ' + str(cnfg.orderID_sell) + '; Buy ID:: ' + str(cnfg.orderID_buy))
    # print('Sell ID: ' + str(ordersInfo2[0]['orderId']))
    # print('Buy ID: ' + str(ordersInfo2[1]['orderId']))
    while cnfg.loopItems <= cnfg.trades:
        try:
            mlastPrice = lastPrice()
            scrMain_.insert(tk.END,'\nPrice: ' + str(mlastPrice) + '; PnL: ' + str(Pnl_) + '; Total PnL: ' + str(cnfg.pnlTotal) + '; Current loop: ' + str(cnfg.loopItems) + '; ' + str(dt.now().strftime('%H:%M:%S')))

            ordersInfo = cnfg.session.get_open_orders(category="linear", symbol=cnfg.pair, openOnly=0, limit=lmt_)
            print('ml ordersInfo: ' + str(ordersInfo))
            print('Total PnL: ' + str(cnfg.pnlTotal))
            ordersInfo2 = ordersInfo["result"]["list"]
            ordInfoLen = len(ordersInfo2)
            firstSellOrder = searchOrder(ordersInfo2, ordInfoLen, cnfg.orderID_sell)
            # if not firstSellOrder and cnfg.isDown: # What trend - Short?
            #     cnfg.trades = cnfg.CTrades[1]
            #     cnfg.isUp = False
            #     print('ml IN firstSellOrder: ' + str(firstSellOrder))
            firstBuyOrder = searchOrder(ordersInfo2, ordInfoLen, cnfg.orderID_buy)
            # if not firstBuyOrder and cnfg.isUp: # What trend - Buy?
            #     cnfg.trades = cnfg.CTrades[0]
            #     cnfg.isDown = False
            #     print('ml IN firstBuyOrder: ' + str(firstBuyOrder))

            print('ml firstBuyOrder: ' + str(firstBuyOrder) + '; ml firstSellOrder: ' + str(firstSellOrder))

            positionInfo = cnfg.session.get_positions(category="linear", symbol=cnfg.pair)
            print('ml positionInfo: ' + str(positionInfo))

            # If order waw triggered - Deleting other order
            if not firstSellOrder and positionInfo and cnfg.retMsg_sell and cnfg.isDown: #if sell(short) delete Buy order
                print('!!!!!!!!!firstSellOrder: ' + str(firstSellOrder) + '; cnfg.retMsg_sell: ' + str(cnfg.retMsg_sell))
                cnfg.retMsg_sell, cnfg.retMsg_buy = '', ''
                delBuyOrder = cnfg.session.cancel_order(category="linear", symbol=cnfg.pair, orderId=cnfg.orderID_buy)
                print('ordersInfo delBuyOrder: ' + str(delBuyOrder) + '; cnfg.retMsg_sell: ' + str(cnfg.retMsg_sell))
                cnfg.log.info("delBuyOrder; responce: {dl};".format(dl=delBuyOrder))
                cnfg.trades = cnfg.CTrades[1]
                cnfg.isUp = False
            if not firstBuyOrder and positionInfo and cnfg.retMsg_buy and cnfg.isUp:  #if buy(long) delete Sell order
                print('!!!!!!!!!firstBuyOrder: ' + str(firstBuyOrder) + '; cnfg.retMsg_buy: ' + str(cnfg.retMsg_buy))
                cnfg.retMsg_buy, cnfg.retMsg_sell = '', ''
                delSellOrder = cnfg.session.cancel_order(category="linear", symbol=cnfg.pair, orderId=cnfg.orderID_sell)
                print('ordersInfo delSellOrder: ' + str(delSellOrder)+ '; cnfg.retMsg_buy: ' + str(cnfg.retMsg_buy))
                cnfg.log.info("delSellOrder; responce: {dl};".format(dl=delSellOrder))
                cnfg.trades = cnfg.CTrades[0]
                cnfg.isDown = False

            got_positions = positionInfo["result"]["list"]
            positionValue = got_positions[0]['positionValue']
            print('ml got_positions[positionValue]: ' + str(positionValue))
            if (positionValue != '0') and (positionValue != ''): #if enter to position
                print('ml Position Info -> Pnl: ' + str(got_positions[0]['unrealisedPnl']))
                Pnl_ = 0.0
                if got_positions[0]['unrealisedPnl'] != '':
                    Pnl_ += round(float(got_positions[0]['unrealisedPnl']), 3)
                diffPercLn = round((mlastPrice - cnfg.orderCostLn) / cnfg.orderCostLn * 100, 2)
                diffPercDn = round((cnfg.orderCostDn - mlastPrice ) / mlastPrice * 100, 2)
                if cnfg.isUp:
                    tpLongFirst = cnfg.lngTPfirstDn[cnfg.loopItems-1]
                    print('ml diff Long -> ' + ' Original price: ' + str(cnfg.orderCostLn) + ' Current price: ' + str(mlastPrice) + ' Diff: ' + str(round(mlastPrice - cnfg.orderCostLn,2)) +' $'+ ' Diff: ' + str(diffPercLn) +' %' )
                    print('ml Value in% for TP Long (cnfg.lngTPfirstDn); Set: ' + str(tpLongFirst) + ' Now: ' + str(diffPercLn) +' %')
                    print('ml Value in% for SL Long (cnfg.lngSLfirstDn); Set: ' + str(cnfg.lngSLfirstDn[cnfg.loopItems-1]) + ' Now: ' + str(diffPercDn) +' %')
                    if (tpLongFirst/2 >= diffPercLn) and (diffPercLn > 0):
                        #print('ml edit Order -> ')
                        lnNextPrice = mlastPrice * (1 + tpLongFirst/2 )
                        print('ml edit Long -> mlastPrice: ' + str(mlastPrice) + '; tpLongFirst/2: ' + str(tpLongFirst/2) + '; lnNextPrice: ' + str(lnNextPrice))
                        lnNextTP = cnfg.costTP_Long[cnfg.loopItems] * (1 + tpLongFirst/2 )
                        print('ml edit Long -> cnfg.costTP_Long[cnfg.loopItems]: ' + str(cnfg.costTP_Long[cnfg.loopItems]) + '; tpLongFirst/2: ' + str(tpLongFirst/2) + '; lnNextTP: ' + str(lnNextTP))
                        #cnfg.orderID_buy, cnfg.retMsg_buy = editOrder(cnfg.costTP_Long[cnfg.loopItems],cnfg.costSL_Long[cnfg.loopItems], exept_,0)
                        #print('ml edit Order -> cnfg.retMsg_buy: ', cnfg.retMsg_buy)
                if cnfg.isDown:
                    tpShortFirst = cnfg.shTPfirstDn[cnfg.loopItems - 1]
                    print('ml diff Short ->' + ' Original price: ' + str(cnfg.orderCostDn) + ' Current price: ' + str(mlastPrice) + ' Diff: ' + str(round(cnfg.orderCostDn - mlastPrice,2)) +' $'+ ' Diff: ' + str(diffPercDn) + ' %')
                    if (tpShortFirst/2 >= diffPercDn) and (diffPercDn > 0):
                        #print('ml edit Order -> ')
                        shNextPrice = mlastPrice * (1 + tpShortFirst/2 )
                        print('ml edit Short -> mlastPrice: ' + str(mlastPrice) + '; tpShortFirst/2: ' + str(tpShortFirst/2) + '; shNextPrice: ' + str(shNextPrice))

                #print('ml Percentage difference for Short: ' + str(diffPercDn) +' %')

            # New order !!!!!!!!!!!!!!!!!!!!!
            if not positionValue and (cnfg.loopItems < cnfg.trades) and (Pnl_ < 0): #if position close and need make new order
                cnfg.loopItems += 1
                initCurrent()  # Initialisation data
                print('ml if position over!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! ')
                if cnfg.isDown:
                    cnfg.pnlTotal += Pnl_
                    cnfg.orderID_sell, cnfg.retMsg_sell = createOrder('Sell', cnfg.levUP, cnfg.costsUP[0], cnfg.costTP_Short[cnfg.loopItems], cnfg.costSL_Short[cnfg.loopItems],cnfg.positSh[cnfg.loopItems], exept_, 'MARKET', 0)
                    cnfg.orderCostDn = cnfg.costsUP[cnfg.loopItems]
                    print('ml next trade!  cnfg.orderID_sell: ' + str(cnfg.orderID_sell) + '; cnfg.retMsg_sell: ' + str(cnfg.retMsg_sell))
                    scrMain_.insert(tk.END, '\ncreate Order Sell; sell ID: ' + str(cnfg.orderID_sell) + '; ' + str(dt.now().strftime('%H:%M:%S')))
                    scrMain_.insert(tk.END, '\nTotal Pnl: ' + str(cnfg.pnlTotal))
                if cnfg.isUp:
                    cnfg.pnlTotal += Pnl_
                    cnfg.orderID_buy, cnfg.retMsg_buy = createOrder('Buy', cnfg.levDn, cnfg.costsDn[0], cnfg.costTP_Long[cnfg.loopItems], cnfg.costSL_Long[cnfg.loopItems], cnfg.positLng[cnfg.loopItems], exept_, 'MARKET', 0)
                    cnfg.orderCostLn = cnfg.costsDn[cnfg.loopItems]
                    print('ml next trade!  cnfg.orderID_buy: ' + str(cnfg.orderID_buy)+ '; cnfg.retMsg_buy: ' + str(cnfg.retMsg_buy))
                    scrMain_.insert(tk.END, '\ncreate Order Buy; buy ID: ' + str(cnfg.orderID_buy) + '; ' + str(dt.now().strftime('%H:%M:%S')))
                    scrMain_.insert(tk.END, '\nTotal Pnl: ' + str(cnfg.pnlTotal))

            print('Cost of in for Short & Long - cnfg.orderCostDn: ' + str(cnfg.orderCostDn) + '; cnfg.orderCostLn: ' + str(cnfg.orderCostLn) + '\n')
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
            cnfg.log.info("create Order() LIMIT; responce: {side}; {price}".format(side=side_, price=prc_))
            return responce["result"]["orderId"], responce["retMsg"]
        if type_ == 'MARKET':
            responce = cnfg.session.place_order(
                category="linear",
                symbol=str(cnfg.pair),
                side=side_,
                orderType="Market",
                #price=prc_,
                qty=str(qty_),
                timeInForce="PostOnly",
                isLeverage=lev_,
                orderFilter="Order",
                takeProfit=str(tp_),
                stopLoss=str(sl_),
                positionIdx=posIdx_,  # hedge-mode if 2 - sell, if 1 - Buy side, 0: one-way mode
            )
            cnfg.log.info("create Order() MARKET; responce: {side}; {price}".format(side=side_, price=prc_))
            return responce["result"]["orderId"], responce["retMsg"]

    except Exception as e:
        exept_.set(str(dt.now().strftime('%H:%M:%S')) +'; createOrder() Exception! -> '+str(e))
        cnfg.log.info("\ncreateOrder(Exception)-> {ex}".format(ex=e))
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
def round_up(n, decimals=0):
    multiplier = 10**decimals
    return math.ceil(n * multiplier) / multiplier
def editOrder(tp_, sl_, exept_, posIdx_):
    try:
        print('edit Order(): ' +'; tp_: ' + str(tp_) + '; sl_: ' + str(sl_) + '; ' + str(dt.now().strftime('%H:%M:%S')))
        responce = cnfg.session.set_trading_stop(
            category="linear",
            symbol=str(cnfg.pair),
            takeProfit=str(tp_),
            stopLoss=str(sl_),
            tpslMode='Partial',
            positionIdx=posIdx_,  # hedge-mode if 2 - sell, if 1 - Buy side, 0: one-way mode
        )
        cnfg.log.info("edit Order() LIMIT; responce: {tp}; {sl}".format(tp=tp_, sl=sl_))
        return responce["result"]["orderId"], responce["retMsg"]

    except Exception as e:
        exept_.set(str(dt.now().strftime('%H:%M:%S')) +'; editOrder() Exception! -> '+str(e))
        cnfg.log.info("\neditOrder(Exception)-> {ex}".format(ex=e))
        print("editOrder() Exception! {}".format(e))
