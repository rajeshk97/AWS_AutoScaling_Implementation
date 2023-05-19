import boto3
client = boto3.client('elb',
                      aws_access_key_id="AKIAJZGOYQWDPHYQXTNQ",
                      aws_secret_access_key="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",
                      region_name='us-east-1'
                      )
ec2 = boto3.resource('ec2',aws_access_key_id="AKIAJZGOYQWDPHYQXTNQ",
    aws_secret_access_key="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",region_name='us-east-1')
vpc = ec2.Vpc('vpc-ef129f95')
x=[]
for i in vpc.instances.all():
    x.append({'InstanceId':i.id})
    
print (x)
response = client.create_load_balancer(
    LoadBalancerName='my-elb4',
    Listeners=[
        {
            'Protocol': 'HTTP',
            'LoadBalancerPort': 80,
            'InstanceProtocol': 'HTTP',
            'InstancePort': 80,
        },
    ],
    AvailabilityZones=[
        'us-east-1a','us-east-1b','us-east-1c','us-east-1d','us-east-1e','us-east-1f'
    ],
    SecurityGroups=[
        'sg-03d3549c37aa2c23f',
    ],
    Scheme=''
)
response = client.configure_health_check(
    LoadBalancerName='myELB',
    HealthCheck={
        'Target': 'HTTP:80/index.html',
        'Interval': 30,
        'Timeout': 5,
        'UnhealthyThreshold': 2,
        'HealthyThreshold': 10
    }
)
response1 = client.register_instances_with_load_balancer(
    LoadBalancerName='myELB',
    Instances=x
)
response = client.configure_health_check(
    LoadBalancerName='myELB',
    HealthCheck={
        'Target': 'HTTP:80/index.html',
        'Interval': 30,
        'Timeout': 5,
        'UnhealthyThreshold': 2,
        'HealthyThreshold': 10
    }
)
print (response1)
#print ("Map the CNAME of your website to: %s" % (response.dns_name))
