import tkinter as tk
# from tkinter import messagebox as msg
from datetime import datetime as dt
import threading
import time
import config as cnfg
import math


# from decimal import Decimal

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


def fhUSDM_initUP(lblPriceInUP_):  # SHORT
    # global balanceSh3, balanceSh3Lev, fee3, mc3
    # feeMarket, feeLimit = getFee(cnfg.pair)
    currGb = lastPrice()  # get current pricel
    # wBalTotal, shBal, shBalT, lngBal, lngBalT, shQty, lngQty = balQty(currGb)
    qprecision, priceScale, tickSize = quantityPrecision(cnfg.pair)
    qtyStep: int = int(str(qprecision)[::-1].find('.'))
    cnfg.pricePrc = priceScale

    # ------------------------ First block in TRADING -------------------------
    cnfg.costsSh[0] = round(currGb * (1 + cnfg.firstInPrcUP[0] / 100), priceScale)  # cost for short then UP 1th in ($)
    # print('fhUSDM_initUP() currGb = ' + str(currGb))
    # print('fhUSDM_initUP() in % cnfg.firstInPrcUP[0] = ' + str(cnfg.firstInPrcUP[0]))
    # print('fhUSDM_initUP() in $ cnfg.costsSh[0] = ' + str(cnfg.costsSh[0]))
    lblPriceInUP_.set(cnfg.costsSh[0])  # view first in $ first cost

    # ------------------------ 1th trading -------------------------
    ####### SHORT
    cnfg.ratioSh = float(round(1 / int(cnfg.CTrades[1]), 2))  # Ratio for first
    print('\nfhUSDM_initUP() Short ratioSh: ' + str(cnfg.ratioSh) + '; cnfg.loopItems: ' + str(cnfg.loopItems))
    cnfg.balanceShOnLev = cnfg.balanceShOnLev * cnfg.ratioSh
    print('fhUSDM_initUP() Short cnfg.balanceShOnLev] * ratio  = ' + str(cnfg.balanceShOnLev))
    cnfg.positSh[0] = truncate(cnfg.balanceShOnLev / cnfg.costsSh[0], qtyStep) #calculate count in first position
    #cnfg.positSh[0] = round_up(cnfg.balanceShOnLev / cnfg.costsSh[0], qtyStep)  # calculate count in first position

    # cnfg.balanceShRatU[0] = round(cnfg.positSh[0] * cnfg.costsSh[0], 2)  # REWRITE balance after truncate quontity !!!!!!
    print('fhUSDM_initUP()  Qty(short)  cnfg.positSh[0]  = ' + str(cnfg.positSh[0]))
    cnfg.costTP_Short[0] = round(cnfg.costsSh[0] * (1 - float(cnfg.shTPfirst[0]) / 100), cnfg.pricePrc)  # cost first TP
    cnfg.costSL_Short[0] = round(cnfg.costsSh[0] * (1 + float(cnfg.shSLfirst[0]) / 100), cnfg.pricePrc)  # cost first SL
    # fee1 = round(cnfg.balanceShRatU[0] * float(feeMarket),4) # fee on market trade, buy and sell
    # cnfg.profitsShU[0]=round(cnfg.balanceShRatU[0] - cnfg.positSh[0] * cnfg.costTP_Short[0], 2) #first profit
    # cnfg.lossesShU[0]=round(cnfg.positSh[0] * cnfg.costSL_Short[0] - cnfg.balanceShRatU[0], 2) #first loss


def fhUSDM_initDOWN(lblPriceInDn_):
    feeMarket, feeLimit = getFee(cnfg.pair)
    currGb = lastPrice()  # get current price
    qprecision, priceScale, tickSize = quantityPrecision(cnfg.pair)
    qtyStep = int(str(qprecision)[::-1].find('.'))
    cnfg.pricePrc = priceScale

    cnfg.costsLn[0] = round(currGb * (1 - cnfg.firstInPrcDn[0] / 100), priceScale)  # cost for long then UP 1th in ($)
    lblPriceInDn_.set(cnfg.costsLn[0])  # view first in $ first cost

    # ------------------------ 1th trading -------------------------
    ####### LONG
    cnfg.ratioLn = float(round(1 / int(cnfg.CTrades[0]), 2))  # Ratio for first
    print('\nfhUSDM_initDOWN Long ratioLng: ' + str(cnfg.ratioLn) + '; cnfg.loopItems: ' + str(cnfg.loopItems) + '; cnfg.balanceLnOnLev: ' + str(cnfg.balanceLnOnLev))
    cnfg.balanceLnOnLev = round(cnfg.balanceLnOnLev * cnfg.ratioLn, 2)
    print('fhUSDM_initDOWN() Long cnfg.balanceLnOnLev = ' + str(cnfg.balanceLnOnLev))
    cnfg.positLng[0] = truncate(cnfg.balanceLnOnLev / cnfg.costsLn[0], qtyStep)  # calculate count in first position - truncate quantity because of restrictions at futures rules
    #cnfg.positLng[0] = round_up(cnfg.balanceLnOnLev / cnfg.costsLn[0],qtyStep)  # calculate count in first position - truncate quantity because of restrictions at futures rules
    print('fhUSDM_initDOWN() Qty(long) cnfg.balanceLnOnLev / cnfg.costsLn[0]: ' + str(cnfg.balanceLnOnLev / cnfg.costsLn[0]) + '; cnfg.positLng[0] = ' + str(cnfg.positLng[0]))
    cnfg.balanceLngRatDn[0] = round(cnfg.positLng[0] * cnfg.costsLn[0],2)  # REWRITE balance after truncate quontity !!!!!!
    cnfg.costTP_Long[0] = round(cnfg.costsLn[0] * (1 + float(cnfg.lngTPfirstDn[0]) / 100),cnfg.pricePrc)  # cost first TP
    cnfg.costSL_Long[0] = round(cnfg.costsLn[0] * (1 - float(cnfg.lngSLfirstDn[0]) / 100),cnfg.pricePrc)  # cost first SL !!!!!!!!!!!! TRIGER IN OCO !!!!!!
    fee11 = round(cnfg.balanceLngRatDn[0] * float(feeMarket) * float(feeMarket), 4)  # fee on market trade, buy and sell
    cnfg.profitsLngDn[0] = round(cnfg.positLng[0] * cnfg.costTP_Long[0] - cnfg.balanceLngRatDn[0], 2)  # first profit
    cnfg.lossesLngDn[0] = round(cnfg.balanceLngRatDn[0] - cnfg.positLng[0] * cnfg.costSL_Long[0], 2)  # first loss


def initCurrent():  # init with second trade and more
    currGb = lastPrice()  # get current price
    feeMarket, feeLimit = getFee(cnfg.pair)
    qprecision, priceScale, tickSize = quantityPrecision(cnfg.pair)
    qtyStep = int(str(qprecision)[::-1].find('.'))
    #print('initCurrent()  qprecision ' + str(qprecision) + '; qtyStep: ' + str(qtyStep))
    cnfg.pricePrc = priceScale
    walletBalance = calculateBalance()
    #walletBalTotal = round(walletBalTotal1 * (1 - 0.01), 2)

    currGb_ = round(currGb, priceScale)  # cost for short then UP 1th in ($)
    print('\ninitCurrent() wallet_balance_total: ' + str(walletBalance))

    # ------ Init for Short
    ratioShCrr = cnfg.ratioSh * (cnfg.loopItems + 1)  # initial rate multiply on currnt step
    BalOnLevUpxRatio = round(walletBalance * cnfg.levUP * ratioShCrr, 2)
    print('initCurrent() Short  BalOnLevUpxRatio: ' + str(BalOnLevUpxRatio) + '; ratioShCrr: ' + str(ratioShCrr))
    print('initCurrent()  cnfg.positSh(row): ' + str(BalOnLevUpxRatio / currGb_))
    cnfg.positSh[cnfg.loopItems] = truncate(BalOnLevUpxRatio / currGb_, qtyStep)  # calculate count for position
    cnfg.costTP_Short[cnfg.loopItems] = round(currGb_ * (1 - float(cnfg.shTPfirst[cnfg.loopItems]) / 100), cnfg.pricePrc)  # calculate TP
    cnfg.costSL_Short[cnfg.loopItems] = round(currGb_ * (1 + float(cnfg.shSLfirst[cnfg.loopItems]) / 100), cnfg.pricePrc)  # calculate SL
    print('initCurrent()  cnfg.costTP_Short: ' + str(cnfg.costTP_Short) + '; cnfg.costSL_Short: ' + str(cnfg.costSL_Short) + '; cnfg.positSh: ' + str(cnfg.positSh))

    # ------ Init for Long
    ratioLngCrr = cnfg.ratioLn * (cnfg.loopItems + 1)  # initial rate multiply on currnt step
    BalOnLevUpxRatio = round(walletBalance * cnfg.levUP * ratioLngCrr, 2)
    print('initCurrent() Long  BalOnLevUpxRatio: ' + str(BalOnLevUpxRatio) + '; ratioLngCrr: ' + str(ratioLngCrr))
    print('initCurrent()  cnfg.positLng(row): ' + str(BalOnLevUpxRatio / currGb_))
    cnfg.positLng[cnfg.loopItems] = truncate(BalOnLevUpxRatio / currGb_, qtyStep)  # calculate count for position
    cnfg.costTP_Long[cnfg.loopItems] = round(currGb_ * (1 + float(cnfg.lngTPfirstDn[cnfg.loopItems]) / 100), cnfg.pricePrc)  # calculate TP
    cnfg.costSL_Long[cnfg.loopItems] = round(currGb_ * (1 - float(cnfg.lngSLfirstDn[cnfg.loopItems]) / 100), cnfg.pricePrc)  # calculate SL
    print('initCurrent()  cnfg.costTP_Long: ' + str(cnfg.costTP_Long) + '; cnfg.costSL_Long: ' + str(cnfg.costSL_Long) + '; cnfg.positLng: ' + str(cnfg.positLng) + '\n')


def fhUSDM_Calculate(CurRt_, TBal_, balUPt_, balDnT_):  # First init
    try:
        cnfg.session.switch_position_mode(category="linear", symbol=cnfg.pair, mode=0)  # mode=3) #Switch Position Mode
        # print('fhUSDM_Calculate() switchPM:  ' + str(switchPM))
    except Exception as e:
        print("fhUSDM_Calculate() Exception!!!!!!!!!!!!!!!!!!!!!!!!!!! {}".format(e))
    try:
        setLeverage = cnfg.session.set_leverage(category="linear", symbol=cnfg.pair, buyLeverage=str(cnfg.levUP),
                                                sellLeverage=str(cnfg.levDn))
        print('fhUSDM_Calculate() setLeverage:  ' + str(setLeverage))
    except Exception as e:
        print("fhUSDM_Calculate() Exception!!!!!!!!!!!!!!!!!!!!!!!!!!! {}".format(e))
    quantityPrecision(cnfg.pair)
    lstPrice = lastPrice()
    CurRt_.set(lstPrice)
    totalBalance = calculateBalance()

    TBal_.set(totalBalance)

    cnfg.balanceShOnLev = round(totalBalance * cnfg.levUP, 1)
    balUPt_.set(cnfg.balanceShOnLev)
    cnfg.balanceLnOnLev = round(totalBalance * cnfg.levDn, 1)
    balDnT_.set(cnfg.balanceLnOnLev)


def calculateBalance():
    quantityPrecision(cnfg.pair)
    get_wallet_balance = cnfg.session.get_wallet_balance(accountType="UNIFIED", coin="USDT")
    wallet_balance1 = get_wallet_balance['result']['list']
    wallet_balance2 = wallet_balance1[0]['coin']
    walletBalance = round(float(wallet_balance2[0]['walletBalance']), 2)
    totalPositionIM = round(float(wallet_balance2[0]['totalPositionIM']), 2)
    forwithdrawal = round(walletBalance - totalPositionIM, 2)
    print('BBBBBBalance for withdrawal: ' + str(forwithdrawal))
    wallet_balance_total = forwithdrawal #round(float(wallet_balance2[0]['walletBalance']), 2)

    #wallet_balance_total = round(wallet_balance_total1, 2)
    #print('calculateBalance() wallet_balance_total1(truncate) = ' + str(wallet_balance_total1) + '; Wallet_balance_total(round) = ' + str(wallet_balance_total1))
    return wallet_balance_total

@thread
def mainLoop(pb00_, scrMain_, exept_):
    global Pnl_, lmt_
    Pnl_ = 0.0
    lmt_ = 4
    ordersListCnt = 0
    orderId1 = ''
    execFeeBuy, execFeeSell = 0.0, 0.0
    #cnfg.orderID_sell, firstBuyOrder = '', ''
    cnfg.orderID_sell, cnfg.retMsg_sell = createOrder('Sell', cnfg.levUP, cnfg.costsSh[0], cnfg.costTP_Short[0],cnfg.costSL_Short[0], cnfg.positSh[0], exept_, 'LIMIT', 0)
    cnfg.orderID_buy, cnfg.retMsg_buy = createOrder('Buy', cnfg.levDn, cnfg.costsLn[0], cnfg.costTP_Long[0],cnfg.costSL_Long[0], cnfg.positLng[0], exept_, 'LIMIT', 0)
    print('ml cnfg.orderID_sell: ' + str(cnfg.orderID_sell) + '; cnfg.orderID_buy: ' + str(cnfg.orderID_buy))
    cnfg.loopItems += 1
    scrMain_.insert(tk.END, '\ncnfg.orderID_sell: ' + str(cnfg.orderID_sell) + '; cnfg.orderID_buy: ' + str(cnfg.orderID_buy))
    while cnfg.loopItems <= cnfg.trades:
        try:
            mlastPrice = lastPrice()
            got_list, positionValue = getPosInfolist()
            posQty = got_list[0]['size']
            #print('ml got_positions[positionValue]: ' + str(positionValue) + '; posQty: ' + str(posQty))
            #print('ml get_execution Buy Order Opened - execFeeBuy: ' + str(execFeeBuy)) 555

            scrMain_.insert(tk.END, '\nPrice: ' + str(mlastPrice) + '; position Qty: ' + str(posQty) + '; PnL: ' + str(round(Pnl_ + cnfg.pnlTotal - float(execFeeBuy),3))  + '; Current loop: ' + str(cnfg.loopItems) + '; ' + str(dt.now().strftime('%H:%M:%S')))
            ordersInfo = cnfg.session.get_open_orders(category="linear", symbol=cnfg.pair, openOnly=0, limit=lmt_)
            #print('ml ordersInfo: ' + str(ordersInfo))
            ordersList = ordersInfo["result"]["list"]
            #print('ml ordersList: ' + str(ordersList))
            ordInfoLen = len(ordersList)
            #print('ml positionsInfo List: ' + str(got_list))
            print('mlastPrice: ' + str(mlastPrice) +'; Total PnL: ' + str(cnfg.pnlTotal))
            if cnfg.orderID_sell or cnfg.orderID_buy and not cnfg.firstOrderEnd:
                cnfg.orderID_sell = searchOrder(ordersList, ordInfoLen, cnfg.orderID_sell)
                cnfg.orderID_buy = searchOrder(ordersList, ordInfoLen, cnfg.orderID_buy)
                print('ml SEARCH cnfg.orderID_buy: ' + str(cnfg.orderID_buy) + '; cnfg.orderID_sell: ' + str(cnfg.orderID_sell))

            #print('ml cnfg.orderID_buy: ' + str(cnfg.orderID_buy) + '; cnfg.orderID_sell: ' + str(cnfg.orderID_sell))

            # If order was triggered - Deleting other order
            ###############################################
            if not cnfg.orderID_sell and not cnfg.firstOrderEnd and cnfg.isDown:  # if sell(short) delete Buy order
                #time.sleep(55)
                #print('!!!!!!!!!cnfg.orderID_sell: ' + str(cnfg.orderID_buy) + '; cnfg.retMsg_sell: ' + str(cnfg.retMsg_sell))
                #cnfg.retMsg_sell, cnfg.retMsg_buy = '', ''
                delBuyOrder = cnfg.session.cancel_order(category="linear", symbol=cnfg.pair, orderId = cnfg.orderID_buy)
                print('ordersInfo delBuyOrder: ' + str(delBuyOrder) + ';  cnfg.orderID_buy: ' + str(cnfg.orderID_buy))
                cnfg.log.info("delBuyOrder; responce: {dl};".format(dl=delBuyOrder))
                cnfg.trades = cnfg.CTrades[1]
                cnfg.isUp = False
                cnfg.firstOrderEnd = True
                #print('ml !!!!!!!!ordersInfo: ' + str(ordersInfo))
            if not cnfg.orderID_buy and not cnfg.firstOrderEnd and cnfg.isUp:  # if buy(long) delete Sell order
                #time.sleep(55)
                print('!!!!!!!!!cnfg.orderID_buy: ' + str(cnfg.orderID_buy) + '; cnfg.retMsg_buy: ' + str(cnfg.retMsg_buy))
                #cnfg.retMsg_buy, cnfg.retMsg_sell = '', ''
                delSellOrder = cnfg.session.cancel_order(category="linear", symbol=cnfg.pair, orderId=cnfg.orderID_sell)
                print('ordersInfo delSellOrder: ' + str(delSellOrder) + '; cnfg.orderID_sell: ' + str(cnfg.orderID_sell))
                cnfg.log.info("delSellOrder; responce: {dl};".format(dl=delSellOrder))
                cnfg.trades = cnfg.CTrades[0]
                cnfg.isDown = False
                cnfg.firstOrderEnd = True
                print('ml !!!!!!!!!ordersInfo: ' + str(ordersInfo))


            # IF ENTER TO POSITION!!!!!!!!!!!!!!!!
            ######################
            if (positionValue != '0') and (positionValue != ''):
                #time.sleep(1)
                print(str(dt.now().strftime('%H:%M:%S')) + '; if Position!!!! IPosition Info -> Pnl: ' + str(got_list[0]['unrealisedPnl']))

                listID, listOT = getOrders(ordersList, ordInfoLen)

                if got_list[0]['unrealisedPnl'] != '':
                    Pnl_ = round(float(got_list[0]['unrealisedPnl']), 3)
                if cnfg.isUp:  # ID LONG
                    #print('if Position!!!! isUp')
                    diffPercLn = round((mlastPrice - cnfg.costsLn[cnfg.loopItems - 1]) / cnfg.costsLn[cnfg.loopItems - 1] * 100,2)  # difference of first IN and Current cost for Long
                    tpLongCurr = cnfg.lngTPfirstDn[cnfg.loopItems - 1]  # in %
                    slLongCurr = cnfg.lngSLfirstDn[cnfg.loopItems - 1]  # in %
                    #getExecOrderList = getExecutionOrd(cnfg.orderID_buy)
                    #getExecOrder = cnfg.session.get_executions(category="linear", orderId=cnfg.orderID_buy, limit=1, )
                    #execFeeBuy = getExecOrderList[0]['execFee']
                    #print('isUp diff Long -> ' + ' Original price: ' + str(cnfg.costsLn[cnfg.loopItems - 1]) + ' Current price: ' + str(mlastPrice) + ' Diff: ' + str(round(mlastPrice - cnfg.costsLn[cnfg.loopItems], 2)) + '$' + ' Diff: ' + str(diffPercLn) + '%')
                    #print('isUp Value in% for TP Long (cnfg.lngTPfirstDn); Set: ' + str(tpLongFirst) + ' Now: ' + str(diffPercLn) + '%')
                    loop = cnfg.loopItems - 1 #??????
                    if cnfg.trailingCountLng >= 1:
                        loop = cnfg.loopItems
                    print('isUp Current price = ' + str(mlastPrice) + '; for TP Long = ' + str(cnfg.costTP_Long) + '; for SL Long =  ' + str(cnfg.costSL_Long))
                    print('isUp Value for TP Long = ' + str(cnfg.costTP_Long[cnfg.loopItems - 1]) + '; for SL Long =  ' + str(cnfg.costSL_Long[cnfg.loopItems - 1]) + '; loop =  ' + str(loop))
                    print('isUp -> diffPercLn: ' + str(diffPercLn) + '; tpLongCurr: ' + str(tpLongCurr) + '; cnfg.loopItems: ' + str(cnfg.loopItems))

                    if (diffPercLn >= tpLongCurr / 2) and (diffPercLn > 0) and (cnfg.trailingCountLng <= 3):  # if a half of TP more then difference of first IN and Current cost
                        delSLTP = cnfg.session.cancel_order(category="linear", symbol=cnfg.pair, orderId=listID[0])
                        print('if Position LONG!!!! Position Delete order listID[0]:' + str(delSLTP))
                        if delSLTP['retMsg'] == 'OK':

                            #lnNextPrice = round(mlastPrice * (1 + tpLongCurr / 2 / 100), 2) # For test ??????
                            #slLongCurr = cnfg.lngSLfirstDn[cnfg.loopItems - 1]  # in %
                            #print('isUp edit Long -> mlastPrice: ' + str(mlastPrice) + '; tpLongCurr/2: ' + str(tpLongCurr / 2) + '; lnNextPrice: ' + str(lnNextPrice))
                            lnNextTP = round(cnfg.costTP_Long[cnfg.loopItems - 1] * (1 + (tpLongCurr / 2 / 100)), cnfg.pricePrc)
                            lnNextSL = round(cnfg.costSL_Long[cnfg.loopItems - 1] * (1 + (slLongCurr / 2 / 100)),cnfg.pricePrc)
                            print('isUp edit Long TP -> cnfg.lngTPfirstDn(%): ' + str(cnfg.lngTPfirstDn) + '; cnfg.costTP_Long($): ' + str(cnfg.costTP_Long) + '; lnNextTP($): ' + str(lnNextTP))
                            print('isUp edit Long SL -> cnfg.lngSLfirstDn(%): ' + str(cnfg.lngSLfirstDn) + '; cnfg.costSL_Long($): ' + str(cnfg.costSL_Long) + '; lnNextSL($): ' + str(lnNextSL))
                            print('isUp edit Long Quantity -> cnfg.positLng: ' + str(cnfg.positLng) + '; cnfg.loopItems: ' + str(cnfg.loopItems) + '; cnfg.trailingCountLng: ' + str(cnfg.trailingCountLng))
                            response = set_trading_stop(lnNextTP,lnNextSL, cnfg.positLng[cnfg.loopItems - 1], exept_,0)
                            if response:
                                cnfg.trailingCountLng += 1
                                cnfg.costSL_Long[cnfg.loopItems] = lnNextSL  # rewrite SL
                                if cnfg.trailingCountLng >= 3: # Rewrite TP on 1/3 instead of 1/2 in this condition
                                    lnNextTP2 = round(cnfg.costTP_Long[cnfg.loopItems - 1] * (1 + (tpLongCurr / 3 / 100)),cnfg.pricePrc) # on second step take profit increase on 1/3
                                    cnfg.costTP_Long[cnfg.loopItems] = round(lnNextTP2,cnfg.pricePrc) #rewrite TP
                                    print('isUp edit THIRD Step Long -> costTP_Long: ' + str(cnfg.costTP_Long) + '; lnNextTP2 (TP increase on 1/3): ' + str(lnNextTP2) + '; tpLongCurr/3): ' + str(tpLongCurr/3))
                                else:
                                    cnfg.costTP_Long[cnfg.loopItems] = lnNextTP #rewrite TP
                                    print('isUp edit UP to THIRD Step Long -> costTP_Long: ' + str(cnfg.costTP_Long) + '; lnNextTP: ' + str(lnNextTP))
                            #print('isUp EDIT Long -> response: ' + str(response))

                        # cnfg.iTimesTS += 1
                if cnfg.isDown: # IF SHORT
                    #print('if Position!!!! isDown')
                    diffPercDn = round((cnfg.costsSh[cnfg.loopItems - 1] - mlastPrice) / mlastPrice * 100,2)  # difference of first IN and Current cost for Short
                    tpShortCurr = cnfg.shTPfirstDn[cnfg.loopItems - 1]  # in %
                    slShortCurr = cnfg.shSLfirstDn[cnfg.loopItems - 1]  # in %
                    #getExecOrderList = getExecutionOrd(cnfg.orderID_sell)
                    #execFeeSell = getExecOrderList[0]['execFee']
                    # print('isDown diff Short ->' + ' Original price: ' + str(cnfg.costsSh[cnfg.loopItems - 1]) + ' Current price: ' + str(mlastPrice) + ' Diff: ' + str(round(cnfg.costsSh[cnfg.loopItems - 1] - mlastPrice, 2)) + '$' + ' Diff: ' + str(diffPercDn) + '%')
                    # print('isDown -> get_execution Sell Order: ' + str(cnfg.session.get_executions(category="linear", orderId=cnfg.orderID_sell, limit=1, )))
                    # print('isDown -> get_execution Sell Order Opened - execFeeSell: ' + str(execFeeSell))
                    loop = cnfg.loopItems - 1 #??????
                    if cnfg.trailingCountSh >= 1:
                        loopSh = cnfg.loopItems
                    print('isDown Current price = ' + str(mlastPrice) + '; for TP Short = ' + str(cnfg.costTP_Short) + '; for SL Short =  ' + str(cnfg.costSL_Short))
                    print('isDown Value for TP short = ' + str(cnfg.costTP_Short[cnfg.loopItems - 1]) + '; for SL Short =  ' + str(cnfg.costSL_Short[cnfg.loopItems - 1]) + '; loop =  ' + str(loop))
                    print('isDown -> diffPercSh: ' + str(diffPercDn) + '; tpShCurr: ' + str(tpShortCurr))

                    if (diffPercDn >= tpShortCurr / 2) and (diffPercDn > 0) and (cnfg.trailingCountSh <= 2):  # if a half of TP more then difference of first IN and Current cost
                        delSLTP = cnfg.session.cancel_order(category="linear", symbol=cnfg.pair, orderId=listID[0])
                        print('if Position SHORT!!!! Position Delete order listID[0]:' + str(delSLTP))
                        if delSLTP['retMsg'] == 'OK':
                            #shNextPrice = round(mlastPrice * (1 - tpShortCurr / 2 / 100), 2) # For test ??????
                            #print('isDown edit short -> mlastPrice: ' + str(mlastPrice) + '; tpShortCurr/2: ' + str(tpShortCurr / 2) + '; shNextPrice: ' + str(shNextPrice))
                            shNextTP = round(cnfg.costTP_Short[cnfg.loopItems - 1] * (1 - (tpShortCurr / 2 / 100)),cnfg.pricePrc)
                            shNextSL = round(cnfg.costSL_Short[cnfg.loopItems - 1] * (1 - (slShortCurr / 2 / 100)),cnfg.pricePrc)
                            print('isDown edit Short TP -> cnfg.shTPfirstDn(%): ' + str(cnfg.shTPfirstDn) + '; cnfg.costTP_Short($): ' + str( cnfg.costTP_Short) + '; shNextTP($): ' + str(shNextTP))
                            print('isDown edit Short SL -> cnfg.shSLfirstDn(%): ' + str(cnfg.shSLfirstDn) + '; cnfg.costSL_Short($): ' + str(cnfg.costSL_Short)  + '; shNextSL: ' + str(shNextSL))
                            print('isDown edit Short Quantity -> cnfg.positSh: ' + str(cnfg.positSh) + '; cnfg.loopItems: ' + str(cnfg.loopItems) + '; cnfg.trailingCountSh: ' + str(cnfg.trailingCountSh))
                            response = set_trading_stop(shNextTP,shNextSL, cnfg.positSh[cnfg.loopItems - 1], exept_,0)
                            if response:
                                cnfg.trailingCountSh += 1
                                if cnfg.trailingCountSh >= 3:
                                    shNextTP2 = round(cnfg.costTP_Short[cnfg.loopItems - 1] * (1 + (tpShortCurr / 3 / 100)),cnfg.pricePrc)  # on second step take profit increase on 1/3
                                    cnfg.costTP_Short[cnfg.loopItems - 1] = round(shNextTP2,cnfg.pricePrc) #rewrite TP
                                    print('isDown edit SECOND item Short -> costTP_Short: ' + str(cnfg.costTP_Short[cnfg.loopItems - 1])+ '; shNextTP2 (TP increase on 1/3): ' + str(shNextTP2) )
                                else:
                                    cnfg.costSL_Short[cnfg.loopItems] = shNextSL  # rewrite TP
                                    print('isDn edit UP to THIRD Step Short -> costTP_Short: ' + str(cnfg.costTP_Short) + '; shNextTP2: ' + str(shNextTP2))


            # New order !!!!!!!!!!!!!!!!!!!!!
            #################################
            if not positionValue and (cnfg.loopItems < cnfg.trades) and (Pnl_ < 0):  # if position close and need make new order
                time.sleep(2)
                initCurrent()  # Initialisation data
                cnfg.loopItems += 1
                print('Stop Loss if position over!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! ')
                if cnfg.isDown:
                    cnfg.pnlTotal += Pnl_
                    cnfg.orderID_sell, cnfg.retMsg_sell = createOrder('Sell', cnfg.levUP, '0', cnfg.costTP_Short[cnfg.loopItems - 1], cnfg.costSL_Short[cnfg.loopItems - 1], cnfg.positSh[cnfg.loopItems - 1], exept_,'MARKET', 0)
                    cnfg.costsSh[cnfg.loopItems - 1] = lastPrice()  # cost of order
                    print('isDown next trade!  cnfg.orderID_sell: ' + str(cnfg.orderID_sell) + '; cnfg.retMsg_sell: ' + str(cnfg.retMsg_sell))
                    print('isDown next trade!  cnfg.loopItems: ' + str(cnfg.loopItems) + '; cnfg.costTP_Short: ' + str(cnfg.costTP_Short) + '; cnfg.costSL_Short: ' + str(cnfg.costSL_Short))
                    scrMain_.insert(tk.END, '\ncreate Order Sell; sell ID: ' + str(cnfg.orderID_sell) + '; ' + str(dt.now().strftime('%H:%M:%S')))
                    scrMain_.insert(tk.END, '\nTotal Pnl: ' + str(cnfg.pnlTotal))
                if cnfg.isUp:
                    cnfg.pnlTotal += Pnl_
                    getExecOrder = cnfg.session.get_executions(category="linear", orderId=cnfg.orderID_buy, limit=1)
                    getExecOrderList = getExecOrder["result"]["list"]
                    print('isUp -> get_execution Buy Order Closed - execFee: ' + str(getExecOrderList[0]['execFee']))
                    cnfg.orderID_buy, cnfg.retMsg_buy = createOrder('Buy', cnfg.levDn, '0', cnfg.costTP_Long[cnfg.loopItems - 1], cnfg.costSL_Long[cnfg.loopItems - 1], cnfg.positLng[cnfg.loopItems - 1], exept_, 'MARKET',0)
                    # cnfg.costsLn = cnfg.costsLn[cnfg.loopItems]
                    cnfg.costsLn[cnfg.loopItems - 1] = lastPrice()  # cost of order
                    print('isUp next trade!  cnfg.orderID_buy: ' + str(cnfg.orderID_buy) + '; cnfg.retMsg_buy: ' + str(cnfg.retMsg_buy))
                    print('isUp next trade!  cnfg.loopItems: ' + str(cnfg.loopItems) + '; cnfg.costTP_Long: ' + str(cnfg.costTP_Long) + '; cnfg.costSL_Long: ' + str(cnfg.costSL_Long))
                    scrMain_.insert(tk.END, '\ncreate Order Buy; buy ID: ' + str(cnfg.orderID_buy) + '; ' + str(dt.now().strftime('%H:%M:%S')))
                    scrMain_.insert(tk.END, '\nTotal Pnl: ' + str(cnfg.pnlTotal))

            if positionValue == '' and not cnfg.evExeption and not ordersList:
                ordersListCnt += 1
                if ordersListCnt > 3: # if 3 min there not orders end of loop
                    cnfg.trades = 0

            thread = threading.Thread(target=run_progressbar(pb00_, cnfg.chVarDelay_GL))
            thread.start()
        except Exception as e:
            exept_.set(str(dt.now().strftime('%H:%M:%S')) + '; mainLoop() Exception! -> ' + str(e))
            print("mainLoop() Exception!!!!!!!!!!!!!!!!!!!!!!!!!!! {}".format(e))
            cnfg.evExeption = True
            # cnf.log.info("mainLoop(Exception)-> {ex}".format(ex=e))
            time.sleep(3)
            continue


def createOrder(side_, lev_, prc_, tp_, sl_, qty_, exept_, type_, posIdx_):
    try:
        print('create Order() side_: ' + str(side_) + '; prc_: ' + str(prc_) + '; tp_: ' + str(tp_) + '; sl_: ' + str(sl_) + '; qty_: ' + str(qty_) + '; ' + str(dt.now().strftime('%H:%M:%S')))
        if type_ == 'LIMIT':
            responce = cnfg.session.place_order(
                category="linear",
                symbol=str(cnfg.pair),
                side=side_,
                orderType="Limit",
                price=prc_,
                qty=str(qty_),
                timeInForce="GTC",
                isLeverage=lev_,
                orderFilter="Order",
                takeProfit=str(tp_),
                stopLoss=str(sl_),
                tpslMode='Partial',
                #tpslMode='Partial',
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
                # price=prc_,
                qty=str(qty_),
                timeInForce="GTC",
                isLeverage=lev_,
                orderFilter="Order",
                takeProfit=str(tp_),
                stopLoss=str(sl_),
                positionIdx=posIdx_,  # hedge-mode if 2 - sell, if 1 - Buy side, 0: one-way mode
            )
            cnfg.log.info("create Order() MARKET; responce: {side}; {price}".format(side=side_, price=prc_))
            return responce["result"]["orderId"], responce["retMsg"]
        cnfg.iOrder += 1

    except Exception as e:
        exept_.set(str(dt.now().strftime('%H:%M:%S')) + '; createOrder() Exception! -> ' + str(e))
        cnfg.log.info("\ncreateOrder(Exception)-> {ex}".format(ex=e))
        print("createOrder() Exception! {}".format(e))


def lastPrice():
    currPrice = cnfg.session.get_tickers(category="inverse", symbol=cnfg.pair)  # get current price
    currPrice2 = currPrice['result']['list']
    lastPrice = float(currPrice2[0]['lastPrice'])
    return lastPrice


def quantityPrecision(pair_):
    prcsn, qrcsn, tsize = 0, 0, 0
    info = cnfg.session.get_instruments_info(category="linear", symbol=pair_)
    info2 = info["result"]["list"]
    # print('instruments_info2: ' + str(info2))
    priceScale = int(info2[0]['priceScale'])
    # print('priceScale: ' + str(priceScale))
    priceFilter = info2[0]['priceFilter']
    tsize = priceFilter['tickSize']
    lotSizeFilter = info2[0]['lotSizeFilter']
    qrcsn = lotSizeFilter['qtyStep']
    # print('tickSize: ' + str(tickSize))

    # for x in info['symbols']:
    #     if x['symbol'] == pair_:
    #         qrcsn = int(x['quantityPrecision'])
    #         prcsn = int(x['pricePrecision'])
    #         for f in x['filters']:
    #             if f['filterType'] == 'PRICE_FILTER':
    #                 tsize = float(f['tickSize'])
    return qrcsn, priceScale, tsize


def getTicker(pair_):
    get_tickers = cnfg.session.get_tickers(category="inverse", symbol=pair_)
    result = get_tickers['result']['list']
    fundingRate = result[0]['fundingRate']
    print('Ticker(result): ' + str(result))
    print('Ticker(fundingRate): ' + str(fundingRate))


def getFee(pair_):
    get_fee = cnfg.session.get_fee_rates(symbol=pair_)
    result = get_fee['result']['list']
    feeMarket = result[0]["takerFeeRate"]
    feeLimit = result[0]["makerFeeRate"]
    # print('feeMarket: ' +str(feeMarket))
    # print('feeLimit: ' +str(feeLimit))
    return feeMarket, feeLimit


def truncate(n, decimals=0):
    multiplier = 10 ** decimals
    return int(n * multiplier) / multiplier


def searchOrder(ordersInfo_, lmt_, order_):
    #print('searchOrder(): order_ = ' + str(order_))
    forderID = ''
    for i in range(0, lmt_):
        if ordersInfo_[i]['orderId'] == order_:
            forderID = ordersInfo_[i]['orderId']
        #     print('searchOrder(): i = ' + str(i) + '; ' + str(forder))
        # print('searchOrder(): i = ' + str(i) + '; lmt_ = ' + str(lmt_)+ '; forder = ' + str(forder))
    # cnfg.log.info("searchOrder; order_: {ord}".format(ord=order_))
    return forderID


def getOrders(ordersList_, lmt_):
    ListID = ['','','','']
    ListOT = ['', '', '', '']
    for i in range(0, lmt_):
        ListID[i] = ordersList_[i]['orderId']
        ListOT[i] = ordersList_[i]['stopOrderType']
    return ListID, ListOT

def round_up(n, decimals=0):
    multiplier = 10 ** decimals
    return math.ceil(n * multiplier) / multiplier


def set_trading_stop(tp_, sl_, qty_, exept_, posIdx_):
    try:
        print('edit Order(): ' + 'tp_: ' + str(tp_) + '; sl_: ' + str(sl_) + '; ' + '; qty_: ' + str(qty_) +'; date: ' + str(dt.now().strftime('%H:%M:%S')))
        responce = cnfg.session.set_trading_stop(
            category="linear",
            symbol=str(cnfg.pair),
            tpslMode="Full",
            positionIdx=posIdx_,
            takeProfit=str(tp_),
            stopLoss=str(sl_),
            #tpSize=qty_,
            #slSize=qty_

        )
        cnfg.log.info("edit Order() LIMIT; responce: {tp}; {sl}".format(tp=tp_, sl=sl_))
        return responce

    except Exception as e:
        exept_.set(str(dt.now().strftime('%H:%M:%S')) + '; set_trading_stop() Exception! -> ' + str(e))
        cnfg.log.info("\nset_trading_stop(Exception)-> {ex}".format(ex=e))
        print("set_trading_stop() Exception! {}".format(e))


def editOrde2(tp_, sl_, exept_, posIdx_):
    try:
        print('edit Order(): ' + '; tp_: ' + str(tp_) + '; sl_: ' + str(sl_) + '; ' + str(dt.now().strftime('%H:%M:%S')))
        responce = cnfg.session.set_trading_stop(
            category="linear",
            symbol=str(cnfg.pair),
            takeProfit=str(tp_),
            stopLoss=str(sl_),
            tpslMode='Full',
            positionIdx=posIdx_,  # hedge-mode if 2 - sell, if 1 - Buy side, 0: one-way mode
        )
        cnfg.log.info("edit Order() LIMIT; responce: {tp}; {sl}".format(tp=tp_, sl=sl_))
        return responce

    except Exception as e:
        exept_.set(str(dt.now().strftime('%H:%M:%S')) + '; set_trading_stop() Exception! -> ' + str(e))
        cnfg.log.info("\nset_trading_stop(Exception)-> {ex}".format(ex=e))
        print("set_trading_stop() Exception! {}".format(e))

def delAllOrders(except_):
    # print('delOrder() ---- ' +str(dt.now().strftime('%H:%M:%S'))) #
    if cnfg.pair:
        # deleteOrders = cnf.client.futures_cancel_all_open_orders(symbol=cnf.pair, timestamp=dt.now())  # Delete all open orders
        deleteOrders = cnfg.session.cancel_all_orders(category="linear", settleCoin="USDT", )
        # print(cndf.session.cancel_all_orders(category="linear", settleCoin="USDT",))
        print('delAllOrdesr() !!!!!!!!!!!!!!!!!!!!!!!! status: ' + str(deleteOrders))
        cnfg.trades = 0
        except_.set('All orders cancel!')


def getPosInfolist():
    positionInfo = cnfg.session.get_positions(category="linear", symbol=cnfg.pair)
    got_list = positionInfo["result"]["list"]
    posValue = got_list[0]['positionValue']
    return got_list, posValue

def getExecutionOrd(orderID):
    result_ = cnfg.session.get_executions(category="linear", orderId=orderID, limit=1)
    list_ = result_["result"]["list"]
    return list_