# -*- coding: utf-8 -*-
"""
Created on Sat Apr 27 15:42:31 2019

@author: rajes
"""

import numpy as np 
import matplotlib.pyplot as plt 

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

def plot_regression_line(x, y, b): 
	# plotting the actual points as scatter plot 
	plt.scatter(x, y, color = "m", 
			marker = "o", s = 30) 

	# predicted response vector 
	y_pred = b[0] + b[1]*x 

	# plotting the regression line 
	plt.plot(x, y_pred, color = "g") 

	# putting labels 
	plt.xlabel('x') 
	plt.ylabel('y') 

	# function to show plot 
	plt.show() 

# observations
ec2 = boto3.resource('ec2',aws_access_key_id=access_key,aws_secret_access_key=secret_access_key,region_name=region)
elb = boto3.client('elb',aws_access_key_id=access_key,aws_secret_access_key=secret_access_key,region_name=region)
cw = boto3.client('cloudwatch',aws_access_key_id=access_key,aws_secret_access_key=secret_access_key,region_name=region)
x = np.array([562.0, 514.0, 532.0, 505.0, 555.0, 506.0, 544.0, 557.0, 520.0, 572.0])
y = np.array([0.099365564508657, 0.033981661572663, 0.0861581920903929, 0.0156756506436981, 0.084083541724555, 0.082161711586548, 0.013661202185793, 0.050676113735294, 0.016666666666667, 0.01704177086228])
b = estimate_coef(x, y)
print("Estimated coefficients:\nb_0 = {} \\nb_1 = {}".format(b[0], b[1]))
# plotting regression line
plot_regression_line(x, y, b) 

if __name__ == "__main__": 
	main() 
