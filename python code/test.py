# -*- coding: utf-8 -*-
"""
Created on Sat Nov 18 14:37:47 2017

@author: Administrator
"""
##To do,check inconsistent in train,cv,test 
##no inconsistent found
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from support import dataget,getSeriesTep,Tmodel,Score,gety,combSeries,Tmodelcom,getytest
from support import Ttest,getnewytrain,newgenhour,sysload,sysloadtest,Ttestup
from sklearn.linear_model import LinearRegression
load,testset,temp = dataget()
newscore = []
#for i in range(1,21):
train = load.loc[load['zone_id']==3]
ytrain = np.array(train.loc[(train['year']==2005) | (train['year']==2006)].iloc[:,4:],dtype=np.int32).reshape((-1,1))

##TO DO:test Zone18 for test accuracy
ytest = getytest(testset,2) #zoneid 0
#for i in range(11):
xtrain,xtest = Ttest(temp,[8, 6, 10, 1, 9, 4])
lr = LinearRegression()
lr.fit(xtrain,ytrain)
yact = lr.predict(xtest)
newscore.append(Score(ytest,yact))

##To do, revise zone21
newscore = []
seq=[3, 6, 7, 0, 9, 5, 2, 8, 4 ,1 ,10]
ytrain,ytest = sysloadtest(load)
xtrain,xtest = Ttest(temp,seq)
lr = LinearRegression()
#lr = LinearRegression(fit_intercept=False)
lr.fit(xtrain,ytrain)
yact = lr.predict(xtest)
newscore.append(Score(ytest,yact))

fig, ax = plt.subplots()
ax1, ax2 = two_scales(ax, [i for i in range(len(ytest[7607:7776]))], ytest[7607:7776], np.array(xtest['temperature'])[7607:7776], 'black', 'r')
ax1.set_ylim([1000000,2200000])
ax2.set_ylim([30,80])

fig, ax = plt.subplots()
ax1, ax2 = two_scales(ax, [i for i in range(len(ytest[4032:4200]))], ytest[4032:4200], np.array(xtest['temperature'])[4032:4200], 'black', 'r')
ax1.set_ylim([900000,2700000])
ax2.set_ylim([50,100])
##To do, read page 
newscore = []
for d in range(1,10):

    seq=[3, 6, 7, 0, 9, 5, 2, 8, 4 ,1 ,10]
    ytrain,ytest = sysloadtest(load)
    xtrain,xtest = Ttestup(temp,seq,d)
    lr = LinearRegression()
    #lr = LinearRegression(fit_intercept=False)
    lr.fit(xtrain,ytrain)
    yact = lr.predict(xtest)
    newscore.append(Score(ytest,yact))
    print newscore[-1]

xtrain1,xtest1 = Ttest(temp,[2])
lr1 = LinearRegression()
#lr = LinearRegression(fit_intercept=False)
lr1.fit(xtrain1,ytrain)
yact1 = lr.predict(xtest1)
newscore.append(Score(ytest,yact1))
##
plt.scatter([i for i in range(500)],yact[:500])
plt.scatter([i for i in range(500)],yact1[:500])
