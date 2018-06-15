# -*- coding: utf-8 -*-
"""
Created on Fri Nov 10 19:29:25 2017

@author: Administrator
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from support import dataget,getSeriesTep,Tmodel,Score,gety,combSeries,Tmodelcom,getytest
from support import Ttest,getnewytrain,newgenhour,sysload,sysloadtest,Tmodelcomupdate,Tmodelup
from sklearn.linear_model import LinearRegression

load,testset,temp = dataget()
#generate system zone
#combtrainy,combtesty = gety(load,0)
##TO DO:Feature scaling     8:24 update,solved
finalscore = []
group = []
for j in range(20):
    score = []
    ytrain,ytest = gety(load,j)  #decide Zoneid
    for k in range(11):
        m = Tmodel(temp,k) #prefitted model,decide stationid
        lr = LinearRegression()
        lr.fit(m,ytrain)
        yact = lr.predict(m)
        score.append(Score(ytrain,yact))
    score = pd.DataFrame(score)
    score = score.sort_values(by=score.columns[0])
    scind = score.index.tolist()
    ##combine temperature
    newscore = []
    nc = []
    for i in range(11):
        xtrain,xtest = Tmodelcom(temp,scind[:i+1]) 
        lr = LinearRegression()
        lr.fit(xtrain,ytrain)
        yact = lr.predict(xtest)
        newscore.append(Score(ytest,yact))
    print 'result for zone '+str(j+1)
    print 'the lowest MAPE is: '+str(min(newscore))
    finalscore.append(min(newscore))
    print 'the correspont stations are: '+ str(scind[:np.argmin(np.array(newscore))+1])
    group.append(scind[:np.argmin(np.array(newscore))+1])
##test on sysload
ytrain,ytest = sysload(load)
#pd.DataFrame(xtest).to_csv(r'E:\Global Energy Forecasting Competition 2012 - Load Forecasting\GEFCOM2012_Data\newupdate\xtest.csv')
d = 5#act=2
##check ytrain/ytest
score = []
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
for i in range(11):
    xtrain,xtest = Tmodelcomupdate(temp,scind[:i+1],d) 
    lr = LinearRegression()
    lr.fit(xtrain,ytrain[d-1:])
    yact = lr.predict(xtest)
    newscore.append(Score(ytest,yact))

print 'result for zone 21'
print 'the lowest MAPE is: '+str(min(newscore))
print 'the correspont stations are: '+ str(scind[:np.argmin(np.array(newscore))+1]) 

ytrain,ytest = sysload(load)
#res = np.vstack((ytrain,ytest))
#pd.DataFrame(xtest).to_csv(r'E:\Global Energy Forecasting Competition 2012 - Load Forecasting\GEFCOM2012_Data\newupdate\xtest.csv')
##check ytrain/ytest
#np.linalg.matrix_rank(np.array(xtrain))
score = []
for k in range(11):
    m = Tmodel(temp,k) #prefitted model,decide stationid
    lr = LinearRegression()
    lr.fit(m,ytrain)
    yact = lr.predict(m)
    score.append(Score(ytrain,yact))
score = pd.DataFrame(score)
score = score.sort_values(by=score.columns[0])
scind = score.index.tolist()
newscore = []
nc = []
for i in range(11):
    xtrain,xtest = Tmodelcom(temp,scind[:i+1]) 
    lr = LinearRegression()
    lr.fit(xtrain,ytrain)
    yact = lr.predict(xtest)
    newscore.append(Score(ytest,yact))

print 'result for zone 21'
print 'the lowest MAPE is: '+str(min(newscore))
print 'the correspont stations are: '+ str(scind[:np.argmin(np.array(newscore))+1]) 
