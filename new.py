import boto3
import datetime
import collections
from functools import reduce
import random
import time

ec2 = boto3.resource('ec2',aws_access_key_id=access_key,aws_secret_access_key=secret_access_key,region_name=region)
def start_ec2(z):
    avail_instances = ec2.instances.filter(
        Filters=[
                    {
                            'Name': 'instance-state-name', 
                            'Values': ['stopped']
                    }
                ]
        )
    y = list()
    for instance in avail_instances:
        y.append(instance.id)
    print (y[0:z])
    
def stop_ec2(z):
    avail_instances = ec2.instances.filter(
        Filters=[
                    {
                            'Name': 'instance-state-name', 
                            'Values': ['running']
                    }
                ]
        )
    
    y = list()
    
    for instance in avail_instances:
        y.append(instance.id)
    print (y[0:z])

def sma(data, window):
        """
        Calculates Simple Moving Average
        http://fxtrade.oanda.com/learn/forex-indicators/simple-moving-average
        """
        if len(data) < window:
            return None
        return sum(data[-window:]) / float(window)
    
def ema(data, window):
    if len(data) < 2 * window:
        raise ValueError("data is too short")
    c = 2.0 / (window + 1)
    current_ema =sma(data[-window*2:-window], window)
    for value in data[-window:]:
        current_ema = (c * value) + ((1 - c) * current_ema)
    return current_ema

"""def ewma(l):
    length = len(l)
    #l = list(map(lambda x: x/length,l))
    e_l = list(map(lambda x: 0,l))
    print (l)
    val = 2/(length+1)
    for i in range(0,length):
        if i==0:
            e_l[i] = l[0]*val
        else:
            e_l[i] = (l[i]-e_l[i-1])*val + e_l[i-1] 
    return ()"""

print (1-3.1670371399462898)