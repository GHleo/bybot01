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
    # cnfg.positShUp[0] = truncate(cnfg.balanceShOnLev / cnfg.costsSh[0], qtyStep) #calculate count in first position
    cnfg.positShUp[0] = round_up(cnfg.balanceShOnLev / cnfg.costsSh[0], qtyStep)  # calculate count in first position

    # cnfg.balanceShRatU[0] = round(cnfg.positShUp[0] * cnfg.costsSh[0], 2)  # REWRITE balance after truncate quontity !!!!!!
    print('fhUSDM_initUP()  Qty(short)  cnfg.positShUp[0]  = ' + str(cnfg.positShUp[0]))
    cnfg.costTP_Short[0] = round(cnfg.costsSh[0] * (1 - float(cnfg.shTPfirst[0]) / 100), cnfg.pricePrc)  # cost first TP
    cnfg.costSL_Short[0] = round(cnfg.costsSh[0] * (1 + float(cnfg.shSLfirst[0]) / 100), cnfg.pricePrc)  # cost first SL
    # fee1 = round(cnfg.balanceShRatU[0] * float(feeMarket),4) # fee on market trade, buy and sell
    # cnfg.profitsShU[0]=round(cnfg.balanceShRatU[0] - cnfg.positShUp[0] * cnfg.costTP_Short[0], 2) #first profit
    # cnfg.lossesShU[0]=round(cnfg.positShUp[0] * cnfg.costSL_Short[0] - cnfg.balanceShRatU[0], 2) #first loss


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
    # cnfg.positLngDn[0] = truncate(cnfg.balanceLnOnLev / cnfg.costsLn[0], qtyStep)  # calculate count in first position - truncate quantity because of restrictions at futures rules
    cnfg.positLngDn[0] = round_up(cnfg.balanceLnOnLev / cnfg.costsLn[0],qtyStep)  # calculate count in first position - truncate quantity because of restrictions at futures rules
    print('fhUSDM_initDOWN() Qty(long) cnfg.balanceLnOnLev / cnfg.costsLn[0]: ' + str(cnfg.balanceLnOnLev / cnfg.costsLn[0]) + '; cnfg.positLngDn[0] = ' + str(cnfg.positLngDn[0]))
    cnfg.balanceLngRatDn[0] = round(cnfg.positLngDn[0] * cnfg.costsLn[0],2)  # REWRITE balance after truncate quontity !!!!!!
    cnfg.costTP_Long[0] = round(cnfg.costsLn[0] * (1 + float(cnfg.lngTPfirstDn[0]) / 100),cnfg.pricePrc)  # cost first TP
    cnfg.costSL_Long[0] = round(cnfg.costsLn[0] * (1 - float(cnfg.lngSLfirstDn[0]) / 100),cnfg.pricePrc)  # cost first SL !!!!!!!!!!!! TRIGER IN OCO !!!!!!
    fee11 = round(cnfg.balanceLngRatDn[0] * float(feeMarket) * float(feeMarket), 4)  # fee on market trade, buy and sell
    cnfg.profitsLngDn[0] = round(cnfg.positLngDn[0] * cnfg.costTP_Long[0] - cnfg.balanceLngRatDn[0], 2)  # first profit
    cnfg.lossesLngDn[0] = round(cnfg.balanceLngRatDn[0] - cnfg.positLngDn[0] * cnfg.costSL_Long[0], 2)  # first loss


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
    cnfg.positSh[cnfg.loopItems] = round_up(BalOnLevUpxRatio / currGb_, qtyStep)  # calculate count for position
    cnfg.costTP_Short[cnfg.loopItems] = round(currGb_ * (1 - float(cnfg.shTPfirst[cnfg.loopItems]) / 100), cnfg.pricePrc)  # calculate TP
    cnfg.costSL_Short[cnfg.loopItems] = round(currGb_ * (1 + float(cnfg.shSLfirst[cnfg.loopItems]) / 100), cnfg.pricePrc)  # calculate SL
    print('initCurrent()  cnfg.costTP_Short: ' + str(cnfg.costTP_Short) + '; cnfg.costSL_Short: ' + str(cnfg.costSL_Short) + '; cnfg.positSh: ' + str(cnfg.positSh))

    # ------ Init for Long
    ratioLngCrr = cnfg.ratioLn * (cnfg.loopItems + 1)  # initial rate multiply on currnt step
    BalOnLevUpxRatio = round(walletBalance * cnfg.levUP * ratioLngCrr, 2)
    print('initCurrent() Long  BalOnLevUpxRatio: ' + str(BalOnLevUpxRatio) + '; ratioLngCrr: ' + str(ratioLngCrr))
    print('initCurrent()  cnfg.positLng(row): ' + str(BalOnLevUpxRatio / currGb_))
    cnfg.positLng[cnfg.loopItems] = round_up(BalOnLevUpxRatio / currGb_, qtyStep)  # calculate count for position
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
    wallet_balance_total = round(float(wallet_balance2[0]['availableToWithdraw']), 2)
    #wallet_balance_total = round(wallet_balance_total1, 2)
    #print('calculateBalance() wallet_balance_total1(truncate) = ' + str(wallet_balance_total1) + '; Wallet_balance_total(round) = ' + str(wallet_balance_total1))
    return wallet_balance_total


def mainLoop(pb00_, scrMain_, exept_):
    global Pnl_, lmt_
    Pnl_ = 0.00
    lmt_ = 4
    firstSellOrder, firstBuyOrder = '', ''
    cnfg.orderID_sell, cnfg.retMsg_sell = createOrder('Sell', cnfg.levUP, cnfg.costsSh[0], cnfg.costTP_Short[0],cnfg.costSL_Short[0], cnfg.positShUp[0], exept_, 'LIMIT', 0)
    cnfg.orderID_buy, cnfg.retMsg_buy = createOrder('Buy', cnfg.levDn, cnfg.costsLn[0], cnfg.costTP_Long[0],cnfg.costSL_Long[0], cnfg.positLngDn[0], exept_, 'LIMIT', 0)
    cnfg.loopItems += 1
    scrMain_.insert(tk.END, '\nSell ID: ' + str(cnfg.orderID_sell) + '; Buy ID:: ' + str(cnfg.orderID_buy))
    while cnfg.loopItems <= cnfg.trades:
        try:
            mlastPrice = lastPrice()
            scrMain_.insert(tk.END, '\nPrice: ' + str(mlastPrice) + '; PnL: ' + str(Pnl_) + '; Total PnL: ' + str(
                cnfg.pnlTotal) + '; Current loop: ' + str(cnfg.loopItems) + '; ' + str(dt.now().strftime('%H:%M:%S')))
            ordersInfo = cnfg.session.get_open_orders(category="linear", symbol=cnfg.pair, openOnly=0, limit=lmt_)
            print('ml ordersInfo: ' + str(ordersInfo))
            print('Total PnL: ' + str(cnfg.pnlTotal))
            ordersInfo2 = ordersInfo["result"]["list"]
            ordInfoLen = len(ordersInfo2)
            if cnfg.retMsg_sell or cnfg.retMsg_buy:
                firstSellOrder = searchOrder(ordersInfo2, ordInfoLen, cnfg.orderID_sell)
                firstBuyOrder = searchOrder(ordersInfo2, ordInfoLen, cnfg.orderID_buy)
                print('ml firstBuyOrder: ' + str(firstBuyOrder) + '; ml firstSellOrder: ' + str(firstSellOrder))

            # If order was triggered - Deleting other order
            ###############################################
            if not firstSellOrder and cnfg.retMsg_sell and cnfg.isDown:  # if sell(short) delete Buy order
                time.sleep(5)
                print(
                    '!!!!!!!!!firstSellOrder: ' + str(firstSellOrder) + '; cnfg.retMsg_sell: ' + str(cnfg.retMsg_sell))
                cnfg.retMsg_sell, cnfg.retMsg_buy = '', ''
                delBuyOrder = cnfg.session.cancel_order(category="linear", symbol=cnfg.pair, orderId=cnfg.orderID_buy)
                print('ordersInfo delBuyOrder: ' + str(delBuyOrder) + '; cnfg.retMsg_sell: ' + str(cnfg.retMsg_sell))
                cnfg.log.info("delBuyOrder; responce: {dl};".format(dl=delBuyOrder))
                cnfg.trades = cnfg.CTrades[1]
                cnfg.isUp = False
                print('ml !!!!!!!!ordersInfo: ' + str(ordersInfo))
            if not firstBuyOrder and cnfg.retMsg_buy and cnfg.isUp:  # if buy(long) delete Sell order
                print('!!!!!!!!!firstBuyOrder: ' + str(firstBuyOrder) + '; cnfg.retMsg_buy: ' + str(cnfg.retMsg_buy))
                cnfg.retMsg_buy, cnfg.retMsg_sell = '', ''
                delSellOrder = cnfg.session.cancel_order(category="linear", symbol=cnfg.pair, orderId=cnfg.orderID_sell)
                print('ordersInfo delSellOrder: ' + str(delSellOrder) + '; cnfg.retMsg_buy: ' + str(cnfg.retMsg_buy))
                cnfg.log.info("delSellOrder; responce: {dl};".format(dl=delSellOrder))
                cnfg.trades = cnfg.CTrades[0]
                cnfg.isDown = False
                print('ml !!!!!!!!!ordersInfo: ' + str(ordersInfo))

            got_list, posValue = getPosInfolist()
            positionValue = got_list[0]['positionValue']
            print('ml got_positions[positionValue]: ' + str(positionValue) + '; posValue: ' + str(posValue))
            # if enter to position
            ######################
            if (positionValue != '0') and (positionValue != ''):
                print('ml Position Info -> Pnl: ' + str(got_list[0]['unrealisedPnl']))
                Pnl_ = 0.0
                if got_list[0]['unrealisedPnl'] != '':
                    # print('$$$$$$$$$$$$$$$$$$$$$$$$$ Position Info -> Pnl_: ' + str(Pnl_))
                    Pnl_ += round(float(got_list[0]['unrealisedPnl']), 3)
                    # print('$$$$$$$$$$$$$$$$$$$$$$$$$ Position Info -> got_positions[0]: ' + str(got_positions[0]['unrealisedPnl']) + '; Pnl_ += : ' + str(Pnl_))
                if cnfg.isUp:  # if Long
                    tpLongFirst = cnfg.lngTPfirstDn[cnfg.loopItems - 1]  # in %
                    getExecOrder = cnfg.session.get_executions(category="linear", orderId=cnfg.orderID_buy, limit=1, )
                    getExecOrderList = getExecOrder["result"]["list"]
                    print('isUp diff Long -> ' + ' Original price: ' + str(cnfg.costsLn[cnfg.loopItems - 1]) + ' Current price: ' + str(mlastPrice) + ' Diff: ' + str(round(mlastPrice - cnfg.costsLn[cnfg.loopItems], 2)) + '$' + ' Diff: ' + str(diffPercLn) + '%')
                    print('isUp Value in% for TP Long (cnfg.lngTPfirstDn); Set: ' + str(tpLongFirst) + ' Now: ' + str(diffPercLn) + '%')
                    print('isUp Value in% for SL Long (cnfg.lngSLfirstDn); Set: ' + str(cnfg.lngSLfirstDn[cnfg.loopItems]) + ' Now: ' + str(diffPercDn) + '%')
                    print('isUp -> get_execution Buy Order Opened - execFee: ' + str(getExecOrderList[0]['execFee']))
                    diffPercLn = round((mlastPrice - cnfg.costsLn[cnfg.loopItems - 1]) / cnfg.costsLn[cnfg.loopItems - 1] * 100,2)  # difference of first IN and Current cost for Long
                    if (diffPercLn >= tpLongFirst / 2) and (diffPercLn > 0):  # if a half of TP more then difference of first IN and Current cost
                        # print('ml edit Order -> ')
                        lnNextPrice = round(mlastPrice * (1 + tpLongFirst / 2 / 100), 2)
                        slLongFirst = cnfg.lngSLfirstDn[cnfg.loopItems - 1]  # in %
                        print('ml edit Long -> mlastPrice: ' + str(mlastPrice) + '; tpLongFirst/2: ' + str(tpLongFirst / 2) + '; lnNextPrice: ' + str(lnNextPrice))
                        lnNextTP = round(cnfg.costTP_Long[cnfg.loopItems - 1] * (1 + (tpLongFirst / 2 / 100)),cnfg.pricePrc)
                        lnNextSL = round(cnfg.costSL_Long[cnfg.loopItems - 1] * (1 + (slLongFirst / 2 / 100)),cnfg.pricePrc)
                        print('ml edit Long -> cnfg.lngTPfirstDn: ' + str(cnfg.lngTPfirstDn) + '; tpLongFirst/2: ' + str(tpLongFirst / 2) + '; cnfg.costTP_Long: ' + str( cnfg.costTP_Long) + '; lnNextTP: ' + str(lnNextTP))
                        print('ml edit Long -> cnfg.lngSLfirstDn: ' + str(cnfg.lngSLfirstDn) + '; slLongFirst/2: ' + str(cnfg.lngSLfirstDn[cnfg.loopItems - 1] / 2) + '; cnfg.costSL_Long: ' + str(cnfg.costSL_Long) + '; lnNextSL: ' + str(lnNextSL))
                        # cnfg.orderID_buy, cnfg.retMsg_buy = editOrder(lnNextTP,lnNextSL, exept_,0)
                        # print('ml EDIT Long -> cnfg.orderID_buy: ' + str(cnfg.orderID_buy) + '; cnfg.retMsg_buy: ' + str(cnfg.retMsg_buy))
                        # print('ml edit Order -> cnfg.retMsg_buy: ', cnfg.retMsg_buy)
                        # cnfg.iTimesTS += 1
                if cnfg.isDown:
                    tpShortFirst = cnfg.shTPfirstDn[cnfg.loopItems - 1]  # in %
                    print('ml diff Short ->' + ' Original price: ' + str(cnfg.costsSh[cnfg.loopItems - 1]) + ' Current price: ' + str(mlastPrice) + ' Diff: ' + str(round(cnfg.costsSh[cnfg.loopItems - 1] - mlastPrice, 2)) + '$' + ' Diff: ' + str(diffPercDn) + '%')
                    print('isUp -> get_execution Sell Order: ' + str(cnfg.session.get_executions(category="linear", orderId=cnfg.orderID_sell, limit=1, )))
                    diffPercDn = round((cnfg.costsSh[cnfg.loopItems - 1] - mlastPrice) / mlastPrice * 100, 4)  # difference of first IN and Current cost for Short
                    if (diffPercDn >= tpShortFirst / 2) and (diffPercDn > 0):
                        # print('ml edit Order -> ')
                        shNextPrice = round(mlastPrice * (1 + tpShortFirst / 2 / 100), 2)
                        print('ml edit Short -> mlastPrice: ' + str(mlastPrice) + '; tpShortFirst/2: ' + str(tpShortFirst / 2) + '; shNextPrice: ' + str(shNextPrice))
                        shNextTP = round(cnfg.costTP_Short[cnfg.loopItems - 1] * (1 + (tpShortFirst / 2 / 100)), 2)
                        print('ml edit Short -> cnfg.costTP_Short: ' + str(cnfg.costTP_Short) + '; tpShortFirst/2: ' + str(tpShortFirst / 2) + '; shNextTP: ' + str( shNextTP))

                # print('ml Percentage difference for Short: ' + str(diffPercDn) +' %')

            # New order !!!!!!!!!!!!!!!!!!!!!
            #################################
            if not positionValue and (cnfg.loopItems < cnfg.trades) and (Pnl_ < 0):  # if position close and need make new order
                time.sleep(5)
                initCurrent()  # Initialisation data
                cnfg.loopItems += 1
                print('ml if position over!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! ')
                if cnfg.isDown:
                    cnfg.pnlTotal += Pnl_
                    cnfg.orderID_sell, cnfg.retMsg_sell = createOrder('Sell', cnfg.levUP, '0', cnfg.costTP_Short[cnfg.loopItems - 1], cnfg.costSL_Short[cnfg.loopItems - 1], cnfg.positSh[cnfg.loopItems - 1], exept_,'MARKET', 0)
                    cnfg.costsSh[cnfg.loopItems - 1] = lastPrice()  # cost of order
                    print('ml next trade!  cnfg.orderID_sell: ' + str(cnfg.orderID_sell) + '; cnfg.retMsg_sell: ' + str(cnfg.retMsg_sell))
                    print('ml next trade!  cnfg.loopItems: ' + str(cnfg.loopItems) + '; cnfg.costTP_Short: ' + str(cnfg.costTP_Short) + '; cnfg.costSL_Short: ' + str(cnfg.costSL_Short))
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
                    print('ml next trade!  cnfg.orderID_buy: ' + str(cnfg.orderID_buy) + '; cnfg.retMsg_buy: ' + str(
                        cnfg.retMsg_buy))
                    print('ml next trade!  cnfg.loopItems: ' + str(cnfg.loopItems) + '; cnfg.costTP_Long: ' + str(
                        cnfg.costTP_Long) + '; cnfg.costSL_Long: ' + str(cnfg.costSL_Long))
                    scrMain_.insert(tk.END, '\ncreate Order Buy; buy ID: ' + str(cnfg.orderID_buy) + '; ' + str(
                        dt.now().strftime('%H:%M:%S')))
                    scrMain_.insert(tk.END, '\nTotal Pnl: ' + str(cnfg.pnlTotal))

            print('Cost of in for Short & Long - cnfg.costsSh: ' + str(cnfg.costsSh) + '; cnfg.costsLn: ' + str(
                cnfg.costsLn) + '\n')
            # print('Get open orders ' + str(cnfg.session.get_open_orders(category="linear",symbol=cnfg.pair,openOnly=0,limit=1,))+ '\n')

            if positionValue == '' or positionValue == '0':
                print('cnfg.iOrder: ', cnfg.iOrder)
            # got_list = getPosInfolist()
            # positionValue = got_list[0]['positionValue']
            # print('positionValue ', positionValue)
            # if positionValue == '' and not cnfg.evExeption:
            #     cnfg.trades = 0
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
    print('searchOrder(): order_ = ' + str(order_))
    forder = ''
    for i in range(0, lmt_):
        if ordersInfo_[i]['orderId'] == order_:
            forder = ordersInfo_[i]['orderId']
        #     print('searchOrder(): i = ' + str(i) + '; ' + str(forder))
        # print('searchOrder(): i = ' + str(i) + '; lmt_ = ' + str(lmt_)+ '; forder = ' + str(forder))
    # cnfg.log.info("searchOrder; order_: {ord}".format(ord=order_))
    return forder


def round_up(n, decimals=0):
    multiplier = 10 ** decimals
    return math.ceil(n * multiplier) / multiplier


def editOrder(tp_, sl_, exept_, posIdx_):
    try:
        print(
            'edit Order(): ' + '; tp_: ' + str(tp_) + '; sl_: ' + str(sl_) + '; ' + str(dt.now().strftime('%H:%M:%S')))
        responce = cnfg.session.set_trading_stop(
            category="linear",
            symbol=str(cnfg.pair),
            takeProfit=str(tp_),
            stopLoss=str(sl_),
            tpslMode='Full',
            positionIdx=posIdx_,  # hedge-mode if 2 - sell, if 1 - Buy side, 0: one-way mode
        )
        cnfg.log.info("edit Order() LIMIT; responce: {tp}; {sl}".format(tp=tp_, sl=sl_))
        return responce["result"]["orderId"], responce["retMsg"]

    except Exception as e:
        exept_.set(str(dt.now().strftime('%H:%M:%S')) + '; editOrder() Exception! -> ' + str(e))
        cnfg.log.info("\neditOrder(Exception)-> {ex}".format(ex=e))
        print("editOrder() Exception! {}".format(e))


def delAllOrders(except_):
    # print('delOrder() ---- ' +str(dt.now().strftime('%H:%M:%S')))
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
