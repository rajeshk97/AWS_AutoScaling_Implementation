import boto3
import datetime
import collections
from functools import reduce
import random
import time
import numpy as np

file = open("access.txt","r")
access_key = file.readline()[:-1]
secret_access_key = file.readline()[:-1]
region = file.readline()[:-1]
p = int(file.readline()[:-1])
h = int(file.readline())
file.close()
ec2 = boto3.resource('ec2',aws_access_key_id=access_key,aws_secret_access_key=secret_access_key,region_name=region)
ec2_1 = boto3.client('ec2',aws_access_key_id=access_key,aws_secret_access_key=secret_access_key,region_name=region)
elb = boto3.client('elb',aws_access_key_id=access_key,aws_secret_access_key=secret_access_key,region_name=region)
cw = boto3.client('cloudwatch',aws_access_key_id=access_key,aws_secret_access_key=secret_access_key,region_name=region)
C = 0
M = 0
def main():
    x = get_instances()
    load_data = get_loaddata()
    performance_data_perinstance = get_performancedata(x)  
    load_data_perinstance = get_loaddata_perinstance(x,load_data)
    p = list()
    q = list()
    for i in load_data_perinstance:
        p.append(i[1])
    for i in performance_data_perinstance[0]:
        q.append(i[1])
    print (p)
    print (q)
    b = estimate_coef(np.array(p),np.array(q)) 
    global C 
    C = b[0]
    global M 
    M = b[1]
    print (C)
    print (M)
    error_perinstance = get_error_perinstance(load_data_perinstance,performance_data_perinstance,x)   
    print ("L(t,i)\n",load_data_perinstance,"\n\n")
    print ("P(t,i)\n",performance_data_perinstance,"\n\n")
    print ("E(t,i)\n",error_perinstance,"\n\n")
    vmscaling(x,load_data,performance_data_perinstance,error_perinstance)
    
def estimate_coef(x, y): 
	# number of observations/points 
	n = np.size(x) 

	# mean of x and y vector 
	m_x, m_y = np.mean(x), np.mean(y) 

	# calculating cross-deviation and deviation about x 
	SS_xy = np.sum(y*x) - n*m_y*m_x 
	SS_xx = np.sum(x*x) - n*m_x*m_x 

	# calculating regression coefficients 
	b_1 = SS_xy / SS_xx 
	b_0 = m_y - b_1*m_x 
    
	return(b_0, b_1) 
    
def start_ec2(x,z):
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
    
    #response = ec2_1.start_instances(InstanceIds=y[0:z])

        
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
    
    #response = ec2_1.stop_instances(InstanceIds=y[0:z])
    
def get_instances():
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
        if instance.id == 'i-0b66c1e492ea68218':
            continue
        else:
            y.append(instance.id)
        
    print (y)
    return y


def get_loaddata():
    data = cw.get_metric_statistics(
            Period=p,
            StartTime=datetime.datetime.utcnow() - datetime.timedelta(seconds=h),
            EndTime=datetime.datetime.utcnow(),
            MetricName='RequestCount',
            Namespace='AWS/ELB',
            Statistics=['Sum'],
            Dimensions=[{'Name':'LoadBalancerName', 'Value':'myELB'}]
            )
    
    filter_data = data['Datapoints'][:-1]
    dataset = dict()
    for i in range(0,len(filter_data)):
        s = filter_data[i]['Timestamp'].time().strftime("%X")
        dataset.update({s:filter_data[i]['Sum']})
    
    load_data = collections.OrderedDict(sorted(dataset.items()))
    load_data = list(load_data.items())
    print (load_data)
    return load_data


def get_performancedata(x):
    dataset = dict()
    performance_data_perinstance = list()
    
    for i in range(0,len(x)):
        data = cw.get_metric_statistics(
                Period=p,
                StartTime=datetime.datetime.utcnow() - datetime.timedelta(seconds=h),
                EndTime=datetime.datetime.utcnow(),
                MetricName='CPUUtilization',
                Namespace='AWS/EC2',
                Statistics=['Sum'],
                Dimensions=[{'Name':'InstanceId','Value':x[i]}]
                )
        
        filter_data = data['Datapoints']
        dataset.clear()
        for i in range(0,len(filter_data)):
            s = filter_data[i]['Timestamp'].time().strftime("%X")
            dataset.update({s:filter_data[i]['Sum']})
    
        od = collections.OrderedDict(sorted(dataset.items()))
        od = list(od.items())
        performance_data_perinstance.append(od)
    
    print (performance_data_perinstance)
    return performance_data_perinstance

   
def get_loaddata_perinstance(x,load_data):
    load_data_perinstance=list()
    for i in load_data:
        y = i[1]/len(x);
        load_data_perinstance.append((i[0],y))
        
    return load_data_perinstance


def get_error_perinstance(load_data_perinstance,performance_data_perinstance,x):
    error_perinstance = list()
    z = list()
    for i in range(0,len(x)):
        z.clear()
        for j in range(0,len(performance_data_perinstance[i])):
            e = (M*load_data_perinstance[j][1])+C
            y = abs(e - performance_data_perinstance[i][j][1])
            z.append((load_data_perinstance[j][0],y))
        error_perinstance.append(z)
    return error_perinstance

def sma(data, window):
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
            

def forecast_loaddata(load_data):
    if(len(load_data)>=10):
        p = load_data[-10:]
    else:
        p = load_data
    
    m = list()
    
    for i in range(0,len(p)):
        m.append(p[i][1])
    
    n = ema(m,5)
    return n
    
def forecast_error(error_perinstance):
    q = list()
    m = list()
    for i in error_perinstance:
        m.clear()
        if(len(i)>=10):
            p = i[-10:]
        else:
            p = i
        for j in range(0,len(p)):
            m.append(i[j][1])
        q.append(ema(m,5))
    return q
      
def forecast_performance(lt1_all,et1_all):
    p = list()
    e = (M*lt1_all)+C
    for i in et1_all:
        p.append(e-i)    
    return p
    
def vmscaling(x,load_data,performance_data_perinstance,error_perinstance):
    n = 1
    flag = 1
    lt1 = forecast_loaddata(load_data)
    while(n<=len(x)):
        flag=1
        lt1_all = lt1/n
        print (lt1_all)
        et1_all = forecast_error(error_perinstance)
        print (et1_all)
        pt1_all = forecast_performance(lt1_all,et1_all)
        print (pt1_all)
        for i in range(0,n):
            if(pt1_all[i] >= 6.5):
                flag = 0
            
        if(flag == 1):
            break; 
        else:
            n+=1
        
    if(n>len(x)):
        #start_ec2(x,(n-len(x)))
        print ("create",n-len(x),"VMs")
    else:
        #stop_ec2(x,(len(x)-n))
       print ("terminate",len(x)-n,"VMS")

if __name__== "__main__":
    i=1
    while(i<=1):
        main()
        #time.sleep(600)
        i+=1