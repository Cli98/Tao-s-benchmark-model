# -*- coding: utf-8 -*-
"""
Created on Thu Jun 14 22:44:29 2018

@author: Administrator
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from support import dataget,getSeriesTep,Tmodel,Score,gety,combSeries,Tmodelcom,getytest
from support import Ttest,getnewytrain,newgenhour,sysload,sysloadtest,Tmodelcomupdate,Tmodelup
from sklearn.linear_model import LinearRegression

load,testset,temp = dataget()
ytrain,ytest = sysload(load)
#res = np.vstack((ytrain,ytest))
#pd.DataFrame(xtest).to_csv(r'E:\Global Energy Forecasting Competition 2012 - Load Forecasting\GEFCOM2012_Data\newupdate\xtest.csv')
##check ytrain/ytest
#np.linalg.matrix_rank(np.array(xtrain))
score = []
d = 3
for k in range(11):
    m = Tmodelup(temp,k,d) #prefitted model,decide stationid
    lr = LinearRegression()
    lr.fit(m,ytrain[d-1:])
    yact = lr.predict(m)
    score.append(Score(ytrain[d-1:],yact))
score = pd.DataFrame(score)
score = score.sort_values(by=score.columns[0])
scind = score.index.tolist()
newscore = []
nc = []
for i in range(11):
    xtrain,xtest = Tmodelcomupdate(temp,scind[:i+1],d) 
    lr = LinearRegression()
    lr.fit(xtrain,ytrain[d-1:])
    yact = lr.predict(xtest)
    newscore.append(Score(ytest,yact))

print 'result for zone 21'
print 'the lowest MAPE is: '+str(min(newscore))
print 'the correspont stations are: '+ str(scind[:np.argmin(np.array(newscore))+1]) 