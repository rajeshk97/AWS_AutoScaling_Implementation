# -*- coding: utf-8 -*-
"""
Created on Thu Dec  5 13:07:02 2019

@author: rajes
"""
import boto3
import datetime
import collections
from functools import reduce
import random
import time
import numpy as np
import matplotlib.pyplot as plt

def norm_avg(t,data):
    sum = 0
    for i in data:
        sum = sum + i
    sum = sum/len(data)
    plt.plot(t,[sum]*10,':',label='Average Value');
    return sum
    
def sma(data, window):
        if len(data) < window:
            return None
        return sum(data[-window:]) / float(window)
    
def ema(t,data, window):
    if len(data) < 2 * window:
        raise ValueError("data is too short")
    c = 2.0 / (window + 1)
    current_ema =sma(data[-window*2:-window], window)
    for value in data[-window:]:
        current_ema = (c * value) + ((1 - c) * current_ema)
    t = [1,2,3,4,5,6,7,8,9,10]
    plt.plot(t,[current_ema]*10,'--',label='EWMA Value');
    plt.legend()
    return current_ema

t = [1,2,3,4,5,6,7,8,9,10]
data = [16005.0, 584.0, 596.0, 584.0, 583.0, 590.0, 590.0, 596.0, 589.0, 584.0]
plt.xlabel('Time')
plt.ylabel('Expected Load')
plt.plot(t,data,'r',label='Previous datapoints');

avg = norm_avg(t,data)
s = ema(t,data,5)
print ("EWMA Prediction = ",s)
print ("Normal Average Prediction = ",avg)