import boto3
import datetime
import matplotlib.pyplot as plt
import collections
cw = boto3.client('cloudwatch',aws_access_key_id="AKIAJZGOYQWDPHYQXTNQ",
    aws_secret_access_key="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",region_name='us-east-1')

data = cw.get_metric_statistics(
        Period=60,
        StartTime=datetime.datetime.utcnow() - datetime.timedelta(seconds=3600),
        EndTime=datetime.datetime.utcnow(),
        MetricName='RequestCount',
        Namespace='AWS/ELB',
        Statistics=['Sum'],
        Dimensions=[{'Name':'LoadBalancerName', 'Value':'myELB'}]
        )

filter_data = data['Datapoints']
dataset = dict()
for i in range(0,len(filter_data)):
    s = filter_data[i]['Timestamp'].time().strftime("%X")
    dataset.update({s:filter_data[i]['Sum']})

print (dataset)
od = collections.OrderedDict(sorted(dataset.items()))
print (od)
x=list()
y=list()
length = len(od)
print (length)
print (x) 
for i in od:
    x.append(int(i.replace(':','')))
    y.append(od[i])
plt.plot(x,y);
plt.show();