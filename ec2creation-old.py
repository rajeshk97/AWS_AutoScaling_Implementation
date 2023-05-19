# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 22:39:14 2019

@author: rajes
"""

import boto3
file = open("access1.txt","r")
access_key = file.readline()[:-1]
secret_access_key = file.readline()[:-1]
region = file.readline()[:-1]
p = int(file.readline()[:-1])
h = int(file.readline())
file.close()
user_data = '''#!/bin/bash
sudo su
yum update -y
yum install httpd -y
service httpd start
chkconfig httpd on
aws s3 cp s3://s3bucket423/index.html /var/www/html/index.html
'''
ec2 = boto3.resource('ec2',aws_access_key_id=access_key,aws_secret_access_key=secret_access_key,region_name=region)
instance = ec2.create_instances(
    ImageId = 'ami-02913db388613c3e1',
    MinCount = 1,
    MaxCount = 3,
    InstanceType = 't2.micro',
    SecurityGroupIds=['sg-081176202dc04ef63'],
    UserData=user_data,
    KeyName='my-ec2key',
     IamInstanceProfile={
                            'Arn': 'arn:aws:iam::603490627527:instance-profile/FullAdminAccess'
                     }
    
    )
    
for i in instance:
    print (i.id)