import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as msg
from tkinter import scrolledtext
from datetime import datetime as dt
#import pandas as pd
#import futuresHEDGE as fHedge
import futuresHEDGE2 as fHedge2

import config as cnfg

class OOP:

    def __init__(self):  # Initializer method!
        self.nbr = 3
        # Create instance
        self.win = tk.Tk()
        self.win.title("Python bot for Bybit")

        self.tabControl = ttk.Notebook(self.win)  # Create Tab Control
        # self.tab0 = ttk.Frame(self.tabControl)  # Create a tab
        # self.tabControl.add(self.tab0, text='Settings')  # Add the tab
        self.tab2 = ttk.Frame(self.tabControl)  # Add a second tab
        self.tabControl.add(self.tab2, text='USDT Perpetual')  # Make second tab visible
        # self.tab3 = ttk.Frame(self.tabControl)  # Create a tab
        # self.tabControl.add(self.tab3, text='Margin')  # Add the tab
        self.tabControl.pack(expand=True, fill="both")  # Pack to make visible

        #t1Frame1St = ttk.Style()
        #t1Frame1St.configure('Red.TLabelframe.Label', background='blue')

        # self.t1Frame1 = tk.LabelFrame(self.tab0, bg="white", text=' ------------ General settings ---------------------------------  ')# style = "Font.TLabelframe")
        # self.t1Frame1.grid(column=0, row=0, padx=4, pady=4, sticky='N')
        # self.t1Frame11 = tk.LabelFrame(self.tab0, bg="white", text=' ----------- Current Info --------------------  ')
        # self.t1Frame11.grid(column=1, row=0, padx=4, pady=4, sticky='N')

        self.panel00 = ttk.LabelFrame(self.tab2)
        self.panel00.grid(column=0, row=0, padx=5, sticky='W')

        self.panel0 = ttk.LabelFrame(self.panel00, text='Balance ')
        self.panel0.grid(column=0, row=0, padx=5, sticky='N')

        self.panel1 = ttk.LabelFrame(self.panel00, text=' Set parameters for HEDGE mode trading  ')
        self.panel1.grid(column=1, row=0, sticky='E')

        self.panel2 = ttk.LabelFrame(self.tab2, text=' ----- TRADING ----- ')
        self.panel2.grid(column=0, row=1, padx=8, sticky='N')
        self.panel3 = ttk.LabelFrame(self.tab2)
        self.panel3.grid(column=0, row=2, sticky='W')

        self.panel2s = ttk.LabelFrame(self.panel2, text=' Set values for UP')
        self.panel2s.grid(column=0, row=2, padx=1, pady=2, sticky='N')
        self.panel2l = ttk.LabelFrame(self.panel2, text=' Set values for DOWN')
        self.panel2l.grid(column=0, row=2, padx=1, pady=2, sticky='S')

        # self.panel21 = ttk.LabelFrame(self.panel2, text='<- Current values')
        # self.panel21.grid(column=6, row=2, padx=2, pady=2)
        # self.panel22 = ttk.LabelFrame(self.panel2, text='<- Current values')
        # self.panel22.grid(column=6, row=3, padx=2, pady=2)
        #
        # self.panel211 = ttk.LabelFrame(self.panel2, text='<- Current values')
        # self.panel211.grid(column=8, row=2, padx=2, pady=2)
        # self.panel222 = ttk.LabelFrame(self.panel2, text='<- Current values')
        # self.panel222.grid(column=8, row=3, padx=2, pady=2)
        #
        # self.panel24 = ttk.LabelFrame(self.panel2, text='<- Current values')
        # self.panel24.grid(column=10, row=2, padx=2, pady=2)
        # self.panel25 = ttk.LabelFrame(self.panel2, text='<- Current values')
        # self.panel25.grid(column=10, row=3, padx=2, pady=2)

# //////////////////// tab #0 Panel ////////////////////////////////////////////////////
#         lblAcces_0 = ttk.Label(self.t1Frame1, text='Select Account')
#         lblAcces_0.grid(column=0, row=0, sticky='W', padx=8, pady=4)
#         self.cmb_Acc_00 = ttk.Combobox(self.t1Frame1, values=cnfg.Accounts, width=12)
#         self.cmb_Acc_00.current(0)
#         self.cmb_Acc_00.grid(column=0, row=1, sticky='W', padx=8, pady=4)
#         #self.cmb_Acc_00.bind("<<ComboboxSelected>>", self.initAccounts)
#         self.txtAccounts = tk.StringVar()
#         lblAcces_00 = ttk.Label(self.t1Frame1, textvariable=self.txtAccounts)
#         lblAcces_00.grid(column=1, row=1, sticky='E')

# Tab Control Futures USDs-M ---------We are creating a container frame to hold all other widgets------------------------------------------------------------
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

#---------------------- panel 1 -------------------------------------------

        # self.lblBal = ttk.Label(self.panel2s, text='Balance:')
        # self.lblBal.grid(column=0, row=0)
        self.vBal = tk.StringVar()
        self.vBal.set(0.00)
        self.lblBal = ttk.Label(self.panel0, textvariable=self.vBal) #Output balance
        self.lblBal.grid(column=0, row=0)
        btnBal0 = ttk.Button(self.panel0, text='Calculate', command=self.calc)
        btnBal0.grid(column=0, row=1)

        label_00 = ttk.Label(self.panel1, text="Base:")
        label_00.grid(column=0, row=0, sticky='E')
        self.cmbFtr01 = ttk.Combobox(self.panel1, values=cnfg.base, width=6)
        self.cmbFtr01.current(0)
        self.cmbFtr01.grid(column=1, row=0)
        label00 = ttk.Label(self.panel1, text="Quote:")
        label00.grid(column=0, row=1, sticky='E')
        self.cmbFtrP1_01 = ttk.Combobox(self.panel1, values=cnfg.quote, width=6)
        self.cmbFtrP1_01.current(0)
        self.cmbFtrP1_01.grid(column=1, padx=6,row=1)
        #self.cmbFtrP1_01.bind("<<ComboboxSelected>>", self.getQuote)

        btnFtr01 = ttk.Button(self.panel1, text='Init', command=self.usdmInit)
        btnFtr01.grid(column=1, row=2, pady=4, sticky='W')

# ------- for UP
#         self.varCB1 = tk.IntVar()
#         self.cb_sh = tk.Checkbutton(self.panel1, text="UPShort -> set Trades", variable=self.varCB1, onvalue=1) #tcheck box for short, variable=self.varCB1, onvalue=1)
#         self.cb_sh.select()
#         self.cb_sh.grid(column=4, row=0, padx=3)
        label_01 = ttk.Label(self.panel1, text="UPShort -> set Trades:")
        label_01.grid(column=4, row=0, padx=3)

        self.cmbFtrP1_02 = ttk.Combobox(self.panel1, values=cnfg.cntTrades, width=4)# set count trades for Short then UP
        self.cmbFtrP1_02.current(1)
        self.cmbFtrP1_02.grid(column=7, row=0)

        # label_02 = ttk.Label(self.panel1, text="UPLong")
        # label_02.grid(column=4, row=1, padx=3, sticky='W')

# ------- for Down
#         label_03 = ttk.Label(self.panel1, text="DnShort")
#         label_03.grid(column=4, row=2, padx=3, sticky='W')

        label_04 = ttk.Label(self.panel1, text="DnLong -> set Trades:")
        label_04.grid(column=4, row=1, padx=3, sticky='W')

        self.cmbFtrP1_11 = ttk.Combobox(self.panel1, values=cnfg.cntTrades, width=4)# set count trades for Long then Dn
        self.cmbFtrP1_11.current(1)
        self.cmbFtrP1_11.grid(column=7, row=1)

# 1------- for Up
        self.lblFtr05 = ttk.Label(self.panel1, text='1trd - TP/SL(%):')
        self.lblFtr05.grid(column=8, row=0, padx=3)
        self.cmbFtrUpTP_Sh1 = ttk.Combobox(self.panel1, values=cnfg.firstIn, width=4) # Set profit (%) for Short 1
        self.cmbFtrUpTP_Sh1.current(9)
        self.cmbFtrUpTP_Sh1.grid(column=9, row=0)
        self.cmbFtrUpSl_Sh1 = ttk.Combobox(self.panel1, values=cnfg.firstIn, width=4)  # Set stop loss (%) for Short 1
        self.cmbFtrUpSl_Sh1.current(7)
        self.cmbFtrUpSl_Sh1.grid(column=10, row=0)

        # self.lblFtrP1_05 = ttk.Label(self.panel1, text='1trd - TP/SL(%):')
        # self.lblFtrP1_05.grid(column=8, row=1, padx=3)
        # self.cmbFtrUpTP_Lng1 = ttk.Combobox(self.panel1, values=cnfg.firstIn, width=4) # Set profit (%) for Long 1
        # self.cmbFtrUpTP_Lng1.current(12)
        # self.cmbFtrUpTP_Lng1.grid(column=9, row=1)
        # self.cmbFtrUpSl_Lng1 = ttk.Combobox(self.panel1, values=cnfg.firstIn, width=4) # Set stop loss (%) for Long 1
        # self.cmbFtrUpSl_Lng1.current(8)
        # self.cmbFtrUpSl_Lng1.grid(column=10, row=1)
#------- for Down
        # self.lblFtr0551 = ttk.Label(self.panel1, text='1trd - TP/SL(%):')
        # self.lblFtr0551.grid(column=8, row=2, padx=3)
        # self.cmbFtrDnTP_Sh1 = ttk.Combobox(self.panel1, values=cnfg.firstIn, width=4)  # Set profit (%) Down for Short 1
        # self.cmbFtrDnTP_Sh1.current(12)
        # self.cmbFtrDnTP_Sh1.grid(column=9, row=2)
        # self.cmbFtrDnSl_Sh1 = ttk.Combobox(self.panel1, values=cnfg.firstIn, width=4)  # Set stop loss (%) Down for Short 1
        # self.cmbFtrDnSl_Sh1.current(8)
        # self.cmbFtrDnSl_Sh1.grid(column=10, row=2)

        self.lblFtrP1_055 = ttk.Label(self.panel1, text='1trd - TP/SL(%):')
        self.lblFtrP1_055.grid(column=8, row=1, padx=3)
        self.cmbFtrDnTP_Lng1 = ttk.Combobox(self.panel1, values=cnfg.firstIn, width=4)  # Set profit (%) Down for Long 1
        self.cmbFtrDnTP_Lng1.current(9)
        self.cmbFtrDnTP_Lng1.grid(column=9, row=1)
        self.cmbFtrDnSl_Lng1 = ttk.Combobox(self.panel1, values=cnfg.firstIn, width=4)  # Set stop loss (%) Down for Long 1
        self.cmbFtrDnSl_Lng1.current(7)
        self.cmbFtrDnSl_Lng1.grid(column=10, row=1)

# 2------- for UP
        self.lblFtr05 = ttk.Label(self.panel1, text='2trd - TP/SL(%):')
        self.lblFtr05.grid(column=11, row=0, padx=3)
        self.cmbFtrUpTP_Sh2 = ttk.Combobox(self.panel1, values=cnfg.firstIn, width=4) # Set profit (%) for Short 2
        self.cmbFtrUpTP_Sh2.current(9)
        self.cmbFtrUpTP_Sh2.grid(column=12, row=0)
        self.cmbFtrUpSl_Sh2 = ttk.Combobox(self.panel1, values=cnfg.firstIn, width=4)  # Set stop loss (%) for Short 2
        self.cmbFtrUpSl_Sh2.current(5)
        #self.cmbFtr11.bind("<<ComboboxSelected>>", self.getTP_SL_percent)
        self.cmbFtrUpSl_Sh2.grid(column=13, row=0,  sticky='E')

        # self.lblFtrP1_06 = ttk.Label(self.panel1, text='2trd - TP/SL(%):')
        # self.lblFtrP1_06.grid(column=11, row=1, padx=3)
        # self.cmbFtrUpTP_Lng2 = ttk.Combobox(self.panel1, values=cnfg.firstIn, width=4) # Set profit (%) for Long 2
        # self.cmbFtrUpTP_Lng2.current(9)
        # #self.cmbFtr12.bind("<<ComboboxSelected>>", self.getTP_SL_percent)
        # self.cmbFtrUpTP_Lng2.grid(column=12, row=1)
        # self.cmbFtrUpSl_Lng2 = ttk.Combobox(self.panel1, values=cnfg.firstIn, width=4) # Set stop loss (%) for Long 2
        # self.cmbFtrUpSl_Lng2.current(5)
        # #self.cmbFtr13.bind("<<ComboboxSelected>>", self.getTP_SL_percent)
        # self.cmbFtrUpSl_Lng2.grid(column=13, row=1)

# 2------- for Down
#         self.lblFtr066 = ttk.Label(self.panel1, text='2trd - TP/SL(%):')
#         self.lblFtr066.grid(column=11, row=2, padx=3)
#         self.cmbFtrDnTP_Sh2 = ttk.Combobox(self.panel1, values=cnfg.firstIn, width=4) # Set profit (%) Down for Short 2
#         self.cmbFtrDnTP_Sh2.current(9)
#         self.cmbFtrDnTP_Sh2.grid(column=12, row=2)
#         self.cmbFtrDnSl_Sh2 = ttk.Combobox(self.panel1, values=cnfg.firstIn, width=4)  # Set stop loss (%) for Short 2
#         self.cmbFtrDnSl_Sh2.current(5)
#         self.cmbFtrDnSl_Sh2.grid(column=13, row=2,  sticky='E')

        self.lblFtrP1_077 = ttk.Label(self.panel1, text='2trd - TP/SL(%):')
        self.lblFtrP1_077.grid(column=11, row=1, padx=3)
        self.cmbFtrDnTP_Lng2 = ttk.Combobox(self.panel1, values=cnfg.firstIn, width=4) # Set profit (%) Down for Long 2
        self.cmbFtrDnTP_Lng2.current(9)
        self.cmbFtrDnTP_Lng2.grid(column=12, row=1)
        self.cmbFtrDnSl_Lng2 = ttk.Combobox(self.panel1, values=cnfg.firstIn, width=4) # Set stop loss (%) Down for Long 2
        self.cmbFtrDnSl_Lng2.current(5)
        self.cmbFtrDnSl_Lng2.grid(column=13, row=1)

# 3------- for UP
        self.lblFtr11 = ttk.Label(self.panel1, text='3trd - TP/SL(%):')
        self.lblFtr11.grid(column=14, row=0, padx=3)
        self.cmbFtrUpTP_Sh3 = ttk.Combobox(self.panel1, values=cnfg.firstIn, width=4) # Set profit (%) for Short 3
        self.cmbFtrUpTP_Sh3.current(3)
        self.cmbFtrUpTP_Sh3.grid(column=15, row=0)
        self.cmbFtrUpSl_Sh3 = ttk.Combobox(self.panel1, values=cnfg.firstIn, width=4)  # Set stop loss (%) for Short 3
        self.cmbFtrUpSl_Sh3.current(2)
        self.cmbFtrUpSl_Sh3.grid(column=16, row=0,  sticky='E')

        # self.lblFtrP1_07 = ttk.Label(self.panel1, text='3trd - TP/SL(%):')
        # self.lblFtrP1_07.grid(column=14, row=1, padx=3)
        # self.cmbFtrUpTP_Lng3 = ttk.Combobox(self.panel1, values=cnfg.firstIn, width=4) # Set profit (%) for Long 3
        # self.cmbFtrUpTP_Lng3.current(3)
        # self.cmbFtrUpTP_Lng3.grid(column=15, row=1)
        # self.cmbFtrUpSl_Lng3 = ttk.Combobox(self.panel1, values=cnfg.firstIn, width=4) # Set stop loss (%) for Long 3
        # self.cmbFtrUpSl_Lng3.current(2)
        # self.cmbFtrUpSl_Lng3.grid(column=16, row=1)

# 3------- for Down
#         self.lblFtr067 = ttk.Label(self.panel1, text='3trd - TP/SL(%):')
#         self.lblFtr067.grid(column=14, row=2, padx=3)
#         self.cmbFtrDnTP_Sh3 = ttk.Combobox(self.panel1, values=cnfg.firstIn, width=4)  # Set profit (%) Down for Short 3
#         self.cmbFtrDnTP_Sh3.current(3)
#         self.cmbFtrDnTP_Sh3.grid(column=15, row=2)
#         self.cmbFtrDnSl_Sh3 = ttk.Combobox(self.panel1, values=cnfg.firstIn, width=4)  # Set stop loss (%) for Short 3
#         self.cmbFtrDnSl_Sh3.current(2)
#         self.cmbFtrDnSl_Sh3.grid(column=16, row=2, sticky='E')

        self.lblFtrP1_078 = ttk.Label(self.panel1, text='3trd - TP/SL(%):')
        self.lblFtrP1_078.grid(column=14, row=1, padx=3)
        self.cmbFtrDnTP_Lng3 = ttk.Combobox(self.panel1, values=cnfg.firstIn, width=4)  # Set profit (%) Down for Long 3
        self.cmbFtrDnTP_Lng3.current(3)
        self.cmbFtrDnTP_Lng3.grid(column=15, row=1)
        self.cmbFtrDnSl_Lng3 = ttk.Combobox(self.panel1, values=cnfg.firstIn, width=4)  # Set stop loss (%) Down for Long 3
        self.cmbFtrDnSl_Lng3.current(2)
        self.cmbFtrDnSl_Lng3.grid(column=16, row=1)

# 4------- for UP
        self.lblFtr12 = ttk.Label(self.panel1, text='4trd - TP/SL(%):')
        self.lblFtr12.grid(column=17, row=0, padx=3)
        self.cmbFtrUpTP_Sh4 = ttk.Combobox(self.panel1, values=cnfg.firstIn, width=4) # Set profit (%) for Short 4
        self.cmbFtrUpTP_Sh4.current(3)
        self.cmbFtrUpTP_Sh4.grid(column=18, row=0)
        self.cmbFtrUpSl_Sh4 = ttk.Combobox(self.panel1, values=cnfg.firstIn, width=4)  # Set stop loss (%) for Short 4
        self.cmbFtrUpSl_Sh4.current(2)
        self.cmbFtrUpSl_Sh4.grid(column=19, row=0,  sticky='E')

        # self.lblFtrP13 = ttk.Label(self.panel1, text='4trd - TP/SL(%):')
        # self.lblFtrP13.grid(column=17, row=1, padx=3)
        # self.cmbFtrUpTP_Lng4 = ttk.Combobox(self.panel1, values=cnfg.firstIn, width=4) # Set profit (%) for Long 4
        # self.cmbFtrUpTP_Lng4.current(3)
        # self.cmbFtrUpTP_Lng4.grid(column=18, row=1)
        # self.cmbFtrUpSl_Lng4 = ttk.Combobox(self.panel1, values=cnfg.firstIn, width=4) # Set stop loss (%) for Long 4
        # self.cmbFtrUpSl_Lng4.current(2)
        # self.cmbFtrUpSl_Lng4.grid(column=19, row=1)

# 4------- for Down
#         self.lblFtr133 = ttk.Label(self.panel1, text='4trd - TP/SL(%):')
#         self.lblFtr133.grid(column=17, row=2, padx=3)
#         self.cmbFtrDnTP_Sh4 = ttk.Combobox(self.panel1, values=cnfg.firstIn, width=4) # Set profit (%) for Short 4
#         self.cmbFtrDnTP_Sh4.current(3)
#         self.cmbFtrDnTP_Sh4.grid(column=18, row=2)
#         self.cmbFtrDnSl_Sh4 = ttk.Combobox(self.panel1, values=cnfg.firstIn, width=4)  # Set stop loss (%) for Short 4
#         self.cmbFtrDnSl_Sh4.current(2)
#         self.cmbFtrDnSl_Sh4.grid(column=19, row=2,  sticky='E')

        self.lblFtr134 = ttk.Label(self.panel1, text='4trd - TP/SL(%):')
        self.lblFtr134.grid(column=17, row=1, padx=3)
        self.cmbFtrDnTP_Lng4 = ttk.Combobox(self.panel1, values=cnfg.firstIn, width=4) # Set profit (%) for long 4
        self.cmbFtrDnTP_Lng4.current(3)
        self.cmbFtrDnTP_Lng4.grid(column=18, row=1)
        self.cmbFtrDnSl_Lng4 = ttk.Combobox(self.panel1, values=cnfg.firstIn, width=4)  # Set stop loss (%) for Short 4
        self.cmbFtrDnSl_Lng4.current(2)
        self.cmbFtrDnSl_Lng4.grid(column=19, row=1,  sticky='E')

# ---------------------- panel 2 -------------------------------------------
        self.lblFtr01 = ttk.Label(self.panel2s, text='Current rate:')
        self.lblFtr01.grid(column=0, row=0, padx=2, sticky='E')
        self.vPrice = tk.StringVar()
        self.vPrice.set(0.00)
        self.lblFtr03 = ttk.Label(self.panel2s, textvariable=self.vPrice) # Current rate for UP
        self.lblFtr03.grid(column=1, row=0, sticky='W')

        self.lblFtrP2_01 = ttk.Label(self.panel2s, text='First in(%):')
        self.lblFtrP2_01.grid(column=0, row=1, padx=2, sticky='E')
        self.cmbFtr03 = ttk.Combobox(self.panel2s, values=cnfg.firstIn, width=4)    # First in (%) for Short
        self.cmbFtr03.current(9)
        self.cmbFtr03.grid(column=1, row=1, sticky='W')

        self.lblFtr02 = ttk.Label(self.panel2s, text='First in($):')
        self.lblFtr02.grid(column=0, row=2, padx=2, sticky='E')
        self.vPrice2 = tk.StringVar()
        self.vPrice2.set(0.00)
        self.lblFtr04 = ttk.Label(self.panel2s, textvariable=self.vPrice2) # First in ($) for UP
        self.lblFtr04.grid(column=1, row=2, sticky='W')

        # self.lblFtrP2_02 = ttk.Label(self.panel2s, text='Balance(1/2):')
        # self.lblFtrP2_02.grid(column=0, row=3, padx=2, sticky='E')
        # self.entFtrVar01 = tk.StringVar()
        # self.entFtrVar01.set(0.00)
        # self.entFtr01 = tk.Entry(self.panel2s, textvariable=self.entFtrVar01, width=4)# Balance for Short then UP
        # self.entFtr01.grid(column=1, row=3, sticky='W')

        self.lblFtr06 = ttk.Label(self.panel2s, text='Leverage:')
        self.lblFtr06.grid(column=0, row=4, padx=2, sticky='E')
        self.cmbFtr04 = ttk.Combobox(self.panel2s, values=cnfg.lev, width=4) # Leverage for Short
        self.cmbFtr04.current(9)
        self.cmbFtr04.grid(column=1, row=4, sticky='W')

        self.lblFtrP2_03 = ttk.Label(self.panel2s, text='TBalance:') # Balance * Leverage for Short
        self.lblFtrP2_03.grid(column=0, row=5, padx=2, sticky='E')
        self.vTBsh = tk.StringVar()
        self.vTBsh.set(0.00)
        self.lblFtr022 = ttk.Label(self.panel2s, textvariable=self.vTBsh)
        self.lblFtr022.grid(column=1, row=5, sticky='W')


        self.lblFtr01l = ttk.Label(self.panel2l, text='Current rate:')
        self.lblFtr01l.grid(column=0, row=0, padx=2, sticky='E')
        self.lblFtr08l = ttk.Label(self.panel2l, textvariable=self.vPrice) # Current rate for DOWN
        self.lblFtr08l.grid(column=1, row=0, sticky='W')

        self.lblFtrP2_01l = ttk.Label(self.panel2l, text='First in(%):')
        self.lblFtrP2_01l.grid(column=0, row=1, padx=2, sticky='E')
        self.cmbFtr10 = ttk.Combobox(self.panel2l, values=cnfg.firstIn, width=4)    # First in (%) for Long
        self.cmbFtr10.current(9)
        self.cmbFtr10.grid(column=1, row=1, sticky='W')

        self.lblFtr02l = ttk.Label(self.panel2l, text='First in($):')
        self.lblFtr02l.grid(column=0, row=2, padx=2, sticky='E')
        self.vPrice3 = tk.StringVar()
        self.vPrice3.set(0.00)
        self.lblFtr09 = ttk.Label(self.panel2l, textvariable=self.vPrice3) # First in ($) for DOWN
        self.lblFtr09.grid(column=1, row=2, sticky='W')

        # self.lblFtrP2_02l = ttk.Label(self.panel2l, text='Balance(1/2):')
        # self.lblFtrP2_02l.grid(column=0, row=3, padx=2, sticky='E')
        # self.entFtrVar02 = tk.StringVar()
        # self.entFtrVar02.set(0.00)
        # self.entFtr03 = tk.Entry(self.panel2l, textvariable=self.entFtrVar02, width=4) # Balance for Long
        # self.entFtr03.grid(column=1, row=3, sticky='W')

        self.lblFtr06l = ttk.Label(self.panel2l, text='Leverage:')
        self.lblFtr06l.grid(column=0, row=4, padx=2, sticky='E')
        self.cmbFtr09 = ttk.Combobox(self.panel2l, values=cnfg.lev, width=4) # Leverage for Long
        self.cmbFtr09.current(9)
        self.cmbFtr09.grid(column=1, row=4, sticky='W')

        self.lblTBsh = ttk.Label(self.panel2l, text='TBalance:') # Balance * Leverage for Long
        self.lblTBsh.grid(column=0, row=5, padx=2, sticky='E')
        self.vTBlng = tk.StringVar()
        self.vTBlng.set(0.00)
        self.lblTBsh1 = ttk.Label(self.panel2l, textvariable=self.vTBlng)
        self.lblTBsh1.grid(column=1, row=5, sticky='W')


# +++++++++++++++++++++++ for 2-traded ++++++++++++++++++++++++++
#         self.lblFtrP2_07 = ttk.Label(self.panel21, text='Trade:')
#         self.lblFtrP2_07.grid(column=0, row=0, padx=2, sticky='E')
#         self.vPrice6 = tk.StringVar()
#         self.vPrice6.set(0)
#         self.lblFtrP2_08 = ttk.Label(self.panel21, textvariable=self.vPrice6) # Current trade Short
#         self.lblFtrP2_08.grid(column=1, row=0, sticky='W')
#
#         self.lblFtrP2_13 = ttk.Label(self.panel21, text=' PnL:')
#         self.lblFtrP2_13.grid(column=0, row=1, padx=2, sticky='E')
#         self.vPrice9 = tk.StringVar()
#         self.vPrice9.set(0.00)
#         self.lblFtrP2_14 = ttk.Label(self.panel21, textvariable=self.vPrice9) # PnL Short
#         self.lblFtrP2_14.grid(column=1, row=1, sticky='W')
#
#         self.lblFtrP2_27 = ttk.Label(self.panel21, text='Total PnL:')
#         self.lblFtrP2_27.grid(column=0, row=2, padx=2, sticky='E')
#         self.vPrcT2s = tk.StringVar()
#         self.vPrcT2s.set(0.00)
#         self.lblFtrP2_14 = ttk.Label(self.panel21, textvariable=self.vPrcT2s) # Total PnL Short
#         self.lblFtrP2_14.grid(column=1, row=2, sticky='W')
#
#         self.lblFtrP2_32 = ttk.Label(self.panel21, text='liquidation:')
#         self.lblFtrP2_32.grid(column=0, row=3, padx=2, sticky='E')
#         self.vPrcLiqSh2 = tk.StringVar()
#         self.vPrcLiqSh2.set(0.00)
#         self.lblFtrP2_33 = ttk.Label(self.panel21, textvariable=self.vPrcLiqSh2) # liquidationPrice 2 - trade Short
#         self.lblFtrP2_33.grid(column=1, row=3, sticky='W')


        # self.lblFtrP2_09 = ttk.Label(self.panel22, text=' Trade:')
        # self.lblFtrP2_09.grid(column=0, row=0, padx=2, sticky='E')
        # self.vPrice7 = tk.StringVar()
        # self.vPrice7.set(0.00)
        # self.lblFtrP2_10 = ttk.Label(self.panel22, textvariable=self.vPrice7) # Current trade Long
        # self.lblFtrP2_10.grid(column=1, row=0, sticky='W')
        #
        # self.lblFtrP2_11 = ttk.Label(self.panel22, text=' PnL:')
        # self.lblFtrP2_11.grid(column=0, row=1, padx=2, sticky='E')
        # self.vPrice8 = tk.StringVar()
        # self.vPrice8.set(0.00)
        # self.lblFtrP2_12 = ttk.Label(self.panel22, textvariable=self.vPrice8) # Pnl Long
        # self.lblFtrP2_12.grid(column=1, row=1, sticky='W')
        #
        # self.lblFtrP2_24 = ttk.Label(self.panel22, text='Total PnL:')
        # self.lblFtrP2_24.grid(column=0, row=2, padx=2, sticky='E')
        # self.vPrcT2l = tk.StringVar()
        # self.vPrcT2l.set(0.00)
        # self.lblFtrP2_14 = ttk.Label(self.panel22, textvariable=self.vPrcT2l) # Total PnL Long
        # self.lblFtrP2_14.grid(column=1, row=2, sticky='W')
        #
        # self.lblFtrP2_34 = ttk.Label(self.panel22, text='liquidation:')
        # self.lblFtrP2_34.grid(column=0, row=3, padx=2, sticky='E')
        # self.vPrcLiqLng2 = tk.StringVar()
        # self.vPrcLiqLng2.set(0.00)
        # self.lblFtrP2_35 = ttk.Label(self.panel22, textvariable=self.vPrcLiqLng2) # liquidationPrice 2 - trade Long
        # self.lblFtrP2_35.grid(column=1, row=3, sticky='E')

        self.lblFtrRatio2 = ttk.Label(self.panel2, text='Trades log')
        self.lblFtrRatio2.grid(column=5, row=1, padx=4)
        self.scrlFtrMain = scrolledtext.ScrolledText(self.panel2, width=100, height=30, wrap=tk.WORD, bg="#39E22D", fg="black")#tab first trade for Short
        self.scrlFtrMain.grid(column=5, row=2, pady=2, sticky='N')
        # self.scrlFtrDn = scrolledtext.ScrolledText(self.panel2, width=100, height=17, wrap=tk.WORD, bg="#FF7777", fg="white")#tab first trade for Long
        # self.scrlFtrDn.grid(column=5, row=3, pady=2, sticky='S')
#
        self.pbT2S2 = ttk.Progressbar(self.panel2, orient='horizontal', length=810, mode='determinate')#tab Trading Work
        self.pbT2S2.grid(row=4, column=5, pady=10)
#
# # +++++++++++++++++++++++ for 3-traded ++++++++++++++++++++++++++
#         self.lblFtrP2_15 = ttk.Label(self.panel211, text='Trade:')
#         self.lblFtrP2_15.grid(column=0, row=0, padx=2, sticky='E')
#         self.vPrcT3s = tk.StringVar()
#         self.vPrcT3s.set(0.00)
#         self.lblFtrP2_16 = ttk.Label(self.panel211, textvariable=self.vPrcT3s) # Current Trade3 - trade Short
#         self.lblFtrP2_16.grid(column=1, row=0, sticky='W')
#
#         self.lblFtrP2_17 = ttk.Label(self.panel211, text='PnL:')
#         self.lblFtrP2_17.grid(column=0, row=1, padx=2, sticky='E')
#         self.vPrcP3nLs = tk.StringVar()
#         self.vPrcP3nLs.set(0.00)
#         self.lblFtrP2_12 = ttk.Label(self.panel211, textvariable=self.vPrcP3nLs) # Current PnL 3 - trade Short
#         self.lblFtrP2_12.grid(column=1, row=1, sticky='W')
#
#         self.lblFtrP2_25 = ttk.Label(self.panel211, text='Total PnL:')
#         self.lblFtrP2_25.grid(column=0, row=2, padx=2, sticky='E')
#         self.vPrcPnl3s_t = tk.StringVar()
#         self.vPrcPnl3s_t.set(0.00)
#         self.lblFtrP2_26 = ttk.Label(self.panel211, textvariable=self.vPrcPnl3s_t) # Total PnL 3 - trade Short
#         self.lblFtrP2_26.grid(column=1, row=2, sticky='W')
#
#         self.lblFtrP2_28 = ttk.Label(self.panel211, text='liquidation:')
#         self.lblFtrP2_28.grid(column=0, row=3, padx=2, sticky='E')
#         self.vPrcLiqSh3 = tk.StringVar()
#         self.vPrcLiqSh3.set(0.00)
#         self.lblFtrP2_29 = ttk.Label(self.panel211, textvariable=self.vPrcLiqSh3) # liquidationPrice 3 - trade Short
#         self.lblFtrP2_29.grid(column=1, row=3, sticky='W')
#
#
#         self.lblFtrP2_18 = ttk.Label(self.panel222, text='Trade:')
#         self.lblFtrP2_18.grid(column=0, row=0, padx=2, sticky='E')
#         self.vPrcT3l = tk.StringVar()
#         self.vPrcT3l.set(0.00)
#         self.lblFtrP2_19 = ttk.Label(self.panel222, textvariable=self.vPrcT3l) # Current Trade 3 - trade Long
#         self.lblFtrP2_19.grid(column=1, row=0, sticky='W')
#
#         self.lblFtrP2_20 = ttk.Label(self.panel222, text='PnL:')
#         self.lblFtrP2_20.grid(column=0, row=1, padx=2, sticky='E')
#         self.vPrcPnl3l = tk.StringVar()
#         self.vPrcPnl3l.set(0.00)
#         self.lblFtrP2_21 = ttk.Label(self.panel222, textvariable=self.vPrcPnl3l) # Current PnL 3 - trade Long
#         self.lblFtrP2_21.grid(column=1, row=1, sticky='W')
#
#         self.lblFtrP2_23 = ttk.Label(self.panel222, text='Total PnL:')
#         self.lblFtrP2_23.grid(column=0, row=2, padx=2, sticky='E')
#         self.vPrcPnl3l_t = tk.StringVar()
#         self.vPrcPnl3l_t.set(0.00)
#         self.lblFtrP2_21 = ttk.Label(self.panel222, textvariable=self.vPrcPnl3l_t) # Total PnL 3 - trade Long
#         self.lblFtrP2_21.grid(column=1, row=2, sticky='W')
#
#         self.lblFtrP2_30 = ttk.Label(self.panel222, text='liquidation:')
#         self.lblFtrP2_30.grid(column=0, row=3, padx=2, sticky='E')
#         self.vPrcLiqLng3 = tk.StringVar()
#         self.vPrcLiqLng3.set(0.00)
#         self.lblFtrP2_31 = ttk.Label(self.panel222, textvariable=self.vPrcLiqLng3) #liquidationPrice  3 - trade Long
#         self.lblFtrP2_31.grid(column=1, row=3, sticky='W')
#
#         self.lblFtrRatio3 = ttk.Label(self.panel2, text='Ratio: 0.3(balance split on 3 parts)')
#         self.lblFtrRatio3.grid(column=7, row=1, padx=4)
#         self.scrlFtr2Sh = scrolledtext.ScrolledText(self.panel2, width=33, height=17, wrap=tk.WORD, bg="#FF7777", fg="white")#tab first trade for Short
#         self.scrlFtr2Sh.grid(column=7, row=2, pady=2, sticky='N')
#         self.scrlFtr2Lng = scrolledtext.ScrolledText(self.panel2, width=33, height=17, wrap=tk.WORD, bg="#39E22D", fg="white")#tab first trade for Long
#         self.scrlFtr2Lng.grid(column=7, row=3, pady=2, sticky='S')
#
#         self.pbT2S3 = ttk.Progressbar(self.panel2, orient='horizontal', length=265, mode='determinate')#tab Trading Work
#         self.pbT2S3.grid(row=4, column=7, pady=10)

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

        # self.lblFtrP22_11 = ttk.Label(self.panel2, text='  Current Rate:')
        # self.lblFtrP22_11.grid(column=6, row=4, sticky='W')
        # self.vPrice111 = tk.StringVar()
        # self.vPrice111.set(0.00)
        # self.lblFtrP22_22 = ttk.Label(self.panel2, textvariable=self.vPrice111) # Current rate
        # self.lblFtrP22_22.grid(column=6, row=4, padx=4,sticky='E')
        #
        # # +++++++++++++++++++++++ for 4-traded ++++++++++++++++++++++++++
        # self.lblFtrP2_4 = ttk.Label(self.panel24, text='Trade:')
        # self.lblFtrP2_4.grid(column=0, row=0, padx=2, sticky='E')
        # self.vPrcT4s = tk.StringVar()
        # self.vPrcT4s.set(0.00)
        # self.lblFtrP2_41 = ttk.Label(self.panel24, textvariable=self.vPrcT4s)  # Current Trade4 - trade Short
        # self.lblFtrP2_41.grid(column=1, row=0, sticky='W')
        #
        # self.lblFtrP2_5 = ttk.Label(self.panel24, text='PnL:')
        # self.lblFtrP2_5.grid(column=0, row=1, padx=2, sticky='E')
        # self.vPrcP4nLs = tk.StringVar()
        # self.vPrcP4nLs.set(0.00)
        # self.lblFtrP2_6 = ttk.Label(self.panel24, textvariable=self.vPrcP4nLs) # Current PnL 4 - trade Short
        # self.lblFtrP2_6.grid(column=1, row=1, sticky='W')
        #
        # self.lblFtrP2_7 = ttk.Label(self.panel24, text='Total PnL:')
        # self.lblFtrP2_7.grid(column=0, row=2, padx=2, sticky='E')
        # self.vPrcPnl4s_t = tk.StringVar()
        # self.vPrcPnl4s_t.set(0.00)
        # self.lblFtrP2_8 = ttk.Label(self.panel24, textvariable=self.vPrcPnl4s_t) # Total PnL 4 - trade Short
        # self.lblFtrP2_8.grid(column=1, row=2, sticky='W')
        #
        # self.lblFtrP2_9 = ttk.Label(self.panel24, text='liquidation:')
        # self.lblFtrP2_9.grid(column=0, row=3, padx=2, sticky='E')
        # self.vPrcLiqSh4 = tk.StringVar()
        # self.vPrcLiqSh4.set(0.00)
        # self.lblFtrP2_42 = ttk.Label(self.panel24, textvariable=self.vPrcLiqSh4) # liquidationPrice 4 - trade Short
        # self.lblFtrP2_42.grid(column=1, row=3, sticky='W')
        #
        # self.lblFtrP2_43 = ttk.Label(self.panel25, text='Trade:')
        # self.lblFtrP2_43.grid(column=0, row=0, padx=2, sticky='E')
        # self.vPrcT4l = tk.StringVar()
        # self.vPrcT4l.set(0.00)
        # self.lblFtrP2_44 = ttk.Label(self.panel25, textvariable=self.vPrcT4l) # Current Trade 4 - trade Long
        # self.lblFtrP2_44.grid(column=1, row=0, sticky='W')
        #
        # self.lblFtrP2_45 = ttk.Label(self.panel25, text='PnL:')
        # self.lblFtrP2_45.grid(column=0, row=1, padx=2, sticky='E')
        # self.vPrcPnl4l = tk.StringVar()
        # self.vPrcPnl4l.set(0.00)
        # self.lblFtrP2_46 = ttk.Label(self.panel25, textvariable=self.vPrcPnl4l) # Current PnL 4 - trade Long
        # self.lblFtrP2_46.grid(column=1, row=1, sticky='W')
        #
        # self.lblFtrP2_47 = ttk.Label(self.panel25, text='Total PnL:')
        # self.lblFtrP2_47.grid(column=0, row=2, padx=2, sticky='E')
        # self.vPrcPnl4l_t = tk.StringVar()
        # self.vPrcPnl4l_t.set(0.00)
        # self.lblFtrP2_48 = ttk.Label(self.panel25, textvariable=self.vPrcPnl4l_t) # Total PnL 4 - trade Long
        # self.lblFtrP2_48.grid(column=1, row=2, sticky='W')
        #
        # self.lblFtrP2_49 = ttk.Label(self.panel25, text='liquidation:')
        # self.lblFtrP2_49.grid(column=0, row=3, padx=2, sticky='E')
        # self.vPrcLiqLng4 = tk.StringVar()
        # self.vPrcLiqLng4.set(0.00)
        # self.lblFtrP2_50 = ttk.Label(self.panel25, textvariable=self.vPrcLiqLng4) #liquidationPrice  4 - trade Long
        # self.lblFtrP2_50.grid(column=1, row=3, sticky='W')
        #
        # self.lblFtrRatio4 = ttk.Label(self.panel2, text='Ratio: 0.25(balance split on 4 parts)')
        # self.lblFtrRatio4.grid(column=9, row=1, padx=4)
        # self.scrlFtr4Sh = scrolledtext.ScrolledText(self.panel2, width=33, height=17, wrap=tk.WORD, bg="#FF7777", fg="white")#tab first trade for Short
        # self.scrlFtr4Sh.grid(column=9, row=2, pady=2, sticky='N')
        # self.scrlFtr4Lng = scrolledtext.ScrolledText(self.panel2, width=33, height=17, wrap=tk.WORD, bg="#39E22D", fg="white")#tab first trade for Long
        # self.scrlFtr4Lng.grid(column=9, row=3, pady=2, sticky='S')
        #
        # self.pbT2S4 = ttk.Progressbar(self.panel2, orient='horizontal', length=265, mode='determinate')#tab Trading Work
        # self.pbT2S4.grid(row=4, column=9, pady=10)
        #
        self.lblBExept = ttk.Label(self.panel3, text='Exception:', font='times 10 bold')
        self.lblBExept.grid(column=0, row=0, sticky='W')
        self.vBExept = tk.StringVar()
        self.vBExept.set('No exceptions yet!')
        self.lblBExept1 = ttk.Label(self.panel3, textvariable=self.vBExept,
                                    font='times 8 bold')  # output BinanceAPIException
        self.lblBExept1.grid(column=1, row=0, sticky='W')
        #
        #         btnFtr03 = ttk.Button(self.panel2, text='Stop', command=self.delAllOrders)
        #         btnFtr03.grid(column=0, row=4, pady=2, sticky='E')

        self.vCoinM = tk.StringVar()
        self.vCoinM.set("Start")
        btnFtr02 = ttk.Button(self.panel2, textvariable=self.vCoinM, command=self.usdmTrade)
        btnFtr02.grid(column=0, row=4, pady=2, sticky='W')

    def usdmTrade(self):
        if cnfg.init == True:
            fHedge2.mainLoop(self.pbT2S2,self.scrlFtrMain,self.vBExept)
            #fHedge2.test(self.vBExept)
            #fHedge.createOrder(self.vBExept)
        else:
            print("First press Init button!")
            self.vBExept.set("First press Init button!")

    def calc(self): #Calculate button
        cnfg.pair = self.cmbFtrP1_01.get() + self.cmbFtr01.get()  # Pair = Quote + Base
        cnfg.getQuote = self.cmbFtrP1_01.get()
        cnfg.levUP = int(self.cmbFtr04.get())  # initialisation leverage for UP
        cnfg.levDn = int(self.cmbFtr09.get())  # initialisation leverage for Down
        print(cnfg.pair)
        # cnfg.LevS[0] = self.cmbFtr04.get() # Leverage for Short
        # cnfg.LevS[1] = self.cmbFtr09.get() # Leverage for Long
        fHedge2.fhUSDM_Calculate(self.vPrice, self.vBal, self.vTBsh,self.vTBlng)
        #cnfg.init = True #check is press Init?
        cnfg.calculate = True  # check is press Init?
    def usdmInit(self):
        if cnfg.calculate == True:
            cnfg.balancesSh, cnfg.balancesLng = [0,0], [0,0]
            #cnfg.levLng, cnfg.levSh = 0,0

            cnfg.pair = self.cmbFtrP1_01.get() + self.cmbFtr01.get()  # Pair = Quote + Base

            #cnfg.CTrades[0]=self.cmbFtrP1_02.get() #count for long then UP ????????????????????????????
            cnfg.trades = int(self.cmbFtrP1_02.get()) # count of trades
            cnfg.CTrades[0] = int(self.cmbFtrP1_11.get())  # count for long !!!!!!!!!!!!!!!!!!!!!!!
            cnfg.CTrades[1] = int(self.cmbFtrP1_02.get())  # count for short

            cnfg.shTPfirst[0]=float(self.cmbFtrUpTP_Sh1.get()) #get first TP percent Up Short
            cnfg.shTPfirst[1]=float(self.cmbFtrUpTP_Sh2.get()) #get second TP percent Up Short
            cnfg.shTPfirst[2] =float(self.cmbFtrUpTP_Sh3.get()) #get fird TP percent Up Short
            cnfg.shTPfirst[3] =float(self.cmbFtrUpTP_Sh4.get()) #get fourth TP percent Up Short
            #print('usdmInit Up cnfg.shTPfirst ' + str(cnfg.shTPfirst))
            #cnfg.lngTPfirst[0]=float(self.cmbFtrUpTP_Lng1.get()) #get first TP percent Up Long
            #cnfg.lngTPfirst[1]=float(self.cmbFtrUpTP_Lng2.get()) #get second TP percent Up Long
            #cnfg.lngTPfirst[2]=float(self.cmbFtrUpTP_Lng3.get()) #get fird TP percent Up Long
            #cnfg.lngTPfirst[3]=float(self.cmbFtrUpTP_Lng4.get()) #get fourth TP percent Up Long
            #print('usdmInit Up cnfg.lngTPfirst ' + str(cnfg.lngTPfirst))

            cnfg.shSLfirst[0]=float(self.cmbFtrUpSl_Sh1.get()) #get first SL percent Up Short
            cnfg.shSLfirst[1]=float(self.cmbFtrUpSl_Sh2.get()) #get second SL percent Up Short
            cnfg.shSLfirst[2]=float(self.cmbFtrUpSl_Sh3.get()) #get fird SL percent Up Short
            cnfg.shSLfirst[3]=float(self.cmbFtrUpSl_Sh4.get()) #get fourth SL percent Up Short
            #print('usdmInit Up cnfg.shSLfirst ' + str(cnfg.shSLfirst))
            # cnfg.lngSLfirst[0]=float(self.cmbFtrUpSl_Lng1.get()) #get first SL percent Up Long
            # cnfg.lngSLfirst[1]=float(self.cmbFtrUpSl_Lng2.get()) #get second SL percent Up Long
            # cnfg.lngSLfirst[2]=float(self.cmbFtrUpSl_Lng3.get()) #get fird SL percent Up Long
            # cnfg.lngSLfirst[3]=float(self.cmbFtrUpSl_Lng4.get()) #get fourth SL percent Up Long
            #print('usdmInit Up cnfg.lngSLfirst ' + str(cnfg.lngSLfirst))

            ###### for Down
            # cnfg.shTPfirstDn[0] = float(self.cmbFtrDnTP_Sh1.get()) #get first TP percent Down Short
            # cnfg.shTPfirstDn[1] = float(self.cmbFtrDnTP_Sh2.get()) #get second TP percent Down Short
            # cnfg.shTPfirstDn[2] = float(self.cmbFtrDnTP_Sh3.get())  # get second TP percent Down Short
            # cnfg.shTPfirstDn[3] = float(self.cmbFtrDnTP_Sh4.get())  # get second TP percent Down Short
            #print('usdmInit Dn cnfg.shTPfirstDn ' + str( cnfg.shTPfirstDn))
            cnfg.lngTPfirstDn[0] = float(self.cmbFtrDnTP_Lng1.get())  # get first TP percent Long for Down
            cnfg.lngTPfirstDn[1] = float(self.cmbFtrDnTP_Lng2.get())  # get first TP percent Long for Down
            cnfg.lngTPfirstDn[2] = float(self.cmbFtrDnTP_Lng3.get())  # get first TP percent Long for Down
            cnfg.lngTPfirstDn[3] = float(self.cmbFtrDnTP_Lng4.get())  # get first TP percent Long for Down
            #print('usdmInit Dn cnfg.lngTPfirstDn ' + str( cnfg.lngTPfirstDn))

            # cnfg.shSLfirstDn[0] = float(self.cmbFtrDnSl_Sh1.get())  # get first SL percent Short
            # cnfg.shSLfirstDn[1] = float(self.cmbFtrDnSl_Sh2.get())  # get first SL percent Short
            # cnfg.shSLfirstDn[2] = float(self.cmbFtrDnSl_Sh3.get())  # get first SL percent Short
            # cnfg.shSLfirstDn[3] = float(self.cmbFtrDnSl_Sh4.get())  # get first SL percent Short
            #print('usdmInit Dn cnfg.shSLfirstDn ' + str( cnfg.shSLfirstDn))
            cnfg.lngSLfirstDn[0] = float(self.cmbFtrDnSl_Lng1.get())  # get first TP percent Long for Down
            cnfg.lngSLfirstDn[1] = float(self.cmbFtrDnSl_Lng2.get())  # get first SL percent Long for Down
            cnfg.lngSLfirstDn[2] = float(self.cmbFtrDnSl_Lng3.get())  # get first SL percent Long for Down
            cnfg.lngSLfirstDn[3] = float(self.cmbFtrDnSl_Lng4.get())  # get first SL percent Long for Down
            #print('usdmInit Dn cnfg.lngSLfirstDn ' + str(cnfg.lngSLfirstDn))

            cnfg.firstInPrcUP[0] = float(self.cmbFtr03.get())
            cnfg.firstInPrcDn[0] = float(self.cmbFtr10.get())

            fHedge2.fhUSDM_initDOWN(self.vPrice3)
            fHedge2.fhUSDM_initUP(self.vPrice2)

            cnfg.init = True #check is press Init?
            cnfg.calculate = False
        else:
            print("First press Calculate button!!!!!!!!!!")
            #self.vBExept.set("First press Init button!")


    #def getQuote(self,*args):
        #cnf.mbalancesQT = 0