#!/usr/bin/env python
# coding: utf-8
# Importing live data

import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter

import pandas as pd
import yfinance as yf  # Yahoo IPA
#yf.pdr_override()

import smtplib # Email 
import time
from datetime import datetime

import numpy as np


#msft = yf.Ticker("MSFT")
#msft.info
#msft.history(period="max")  definetlymyemail@gmail.com


#Email Shit

sender_email = "notarealemail@gmail.com" #The sender email
rec_email = "arealemail@gmail.com" #The receiver email
password = ("maybearealpassword") #The password to the sender email

# Set messages under conditionals statements


# Building SMA using live Yahoo Data
# Base off every hour for 24 * 20 Day, 50day periods.
# 15 min ints, 60day period
# 20 day MA = 24 * 4 * 20 = 1920 .rolling(windows=1920)
# 50 day MA = 24 * 4 * 50 = 4800 .rolling(windows=4800)

# Trial on smaller Windows of Time 
# 5 hour MA = 20 windows of 15min int
# 10 hour MA = 40 windows of 15min int
# valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
# fetch data by interval (including intraday if period < 60 days)
# valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
# download dataframe # periods can differ from yfinance pages set ints
data = yf.download("ETH-USD", period='1y', interval='1d')
#data.tail(10)




#------------------------------
# Trial 20 and 40 hour MA
#-------------------------------

# Crypto Higher STD, Higher Volatility should trade Longer sets of time.
#Graph the data
#Get the time period 
# 15 minute periods, 4 per hour x 24 = 96 for 1 day. 96 x 24, 2304periods, 50 day = 
#period20MA = 2304
#period50MA = 4800

# 1 day
period20MA = 20
period50MA = 50
# Calculate the Simple Moving Average, Std Deviation, Upper Band and Lower Band
#Calculating the Simple Moving Average
data['20MA'] = data['Close'].rolling(window=period20MA, min_periods=1).mean()
data['50MA'] = data['Close'].rolling(window=period50MA, min_periods=1).mean()
# Create Exponential Moving Averages
#data['20MA'] = data['Close'].ewm(window=period20MA).mean()
#data['50MA'] = data['Close'].ewm(window=period50MA).mean()

# Signals
# Create Signals
data['Signal'] = 0.0
data['Signal'] = np.where(data['20MA'] > data['50MA'], 1.0, 0.0)
data['Position'] = data['Signal'].diff()
    
#data['20MA'][-1]
#data['50MA'][-1]

# When Shorter-Term MA crosses above the longer-term MA
# Signals buy "Golden Cross"
# When Shorter0term MA crosses below the Longer-Term Ma
# Signals a Sell " Death Cross"


# Moving Averages Email Conditions 
message_death = "Assets Short Term MA " + "%0.2f" % data['20MA'][-1] + " has crossed below Longer Term MA: " + "%0.2f" % data['50MA'][-1] + ", Signalling a Death Cross at Price " +  "%0.2f" % data['Close'][-1] + "."
message_golden = "Assets Short Term MA " + "%0.2f" % data['20MA'][-1] + " has crossed above Longer Term MA: " + "%0.2f" % data['50MA'][-1] + ", Signalling a Golden Cross at Price " +  "%0.2f" % data['Close'][-1] + "."

#death, golden
message_below_cross = "Death Cross \n20 Day Moving Average: " + str(data['20MA'][-1])  +  "\n50 Day Moving Average: " + str(data['50MA'][-1]) + '\nCurrent Price: ' + str(data['Close'][-1])
message_above_cross = 'Golden Cross \n20 Day Moving Average: ' + str(data['20MA'][-1])  +  "\n50 Day Moving Average: " + str(data['50MA'][-1]) + '\nCurrent Price: ' + str(data['Close'][-1])
# 50 Day moving Average Cross and indication.

if data['Position'][-1] == 0: #-1.0
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, password) #logs into your email account
    #print("Login Success") #confirms that you have logged in succesfully
    server.sendmail(sender_email, rec_email, message_below_cross) #send the email with your custom mesage
    #print("Email was sent") #confirms that the email was sent
    #print(message_below_cross)
elif data['Position'][-1] == 1.0:
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, password) #logs into your email account
    #print("Login Success") #confirms that you have logged in succesfully
    server.sendmail(sender_email, rec_email, message_golden) #send the email with your custom mesage
    #print("Email was sent") #confirms that the email was sent
    #print(message_golden)

