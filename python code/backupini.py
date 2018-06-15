# -*- coding: utf-8 -*-
"""
Created on Thu Nov 09 21:26:43 2017

@author: Administrator
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cross_validation import KFold
from sklearn.preprocessing import StandardScaler
dataset = pd.read_csv(r'E:\Global Energy Forecasting Competition 2012 - Load Forecasting\Loadnew.csv').iloc[:,1:]
#null value at 32993 to 32999
#dataset = dataset.dropna(axis = 0,how = 'any')
#train = dataset.loc[(dataset['year']==2004)|(dataset['year']==2005)]
#cvset = dataset.loc[(dataset['year']==2006)]
#testset = dataset.loc[(dataset['year']==2007)]
##test code
mn = pd.read_csv(r'E:\Global Energy Forecasting Competition 2012 - Load Forecasting\fe.csv',header=None).iloc[:,:-1]

##test code for Z18
newscore = []
ytest = getytest(testset,17) #zoneid 0
ytrain = getnewytrain(train,cvset,17)
for i in range(11):
    npo = Tmodelcom(testset,temp,[i])
    xtest = npo.loc[npo['year']==2007]
    xtest = xtest.iloc[:,1:]
    m = npo.drop(npo.index[10320:10488])
    m = m.drop(npo.index[12864:13032])
    m = m.drop(npo.index[14832:15000])
    m = m.drop(npo.index[17376:17544])

    m = m.drop(npo.index[18576:18744])
    m = m.drop(npo.index[21000:21168])
    m = m.drop(npo.index[22656:22824])
    m = m.drop(npo.index[25344:25512])
    xtrain1 = m.loc[npo['year']==2005]
    xtrain2 = m.loc[npo['year']==2006]
    xtrain = pd.concat([xtrain1,xtrain2])
    xtrain = xtrain.iloc[:,1:]
#    m.index= [x for x in range(len(m))]
#    m['trend'] = m.index+1
    lr = LinearRegression()
    lr.fit(xtrain,ytrain)
    yact = lr.predict(xtest)
    newscore.append(Score(ytest,yact))
    

##test code for Ttest,score min 12.8
    res['Hourday'] = res['hour']*res['day']
    res['THour'] = np.array(res['temperature'],dtype=np.int64) * np.array(res['hour'],dtype=np.int64)
    res['T2Hour'] = np.array(res['tem2'],dtype=np.int64)*np.array(res['hour'],dtype=np.int64)
    res['T3Hour'] = np.array(res['tem3'],dtype=np.int64)*np.array(res['hour'],dtype=np.int64)
    res['TMonth'] = np.array(res['temperature'],dtype=np.int64) * np.array(res['month'],dtype=np.int64)
    res['T2Month'] = np.array(res['tem2'],dtype=np.int64)*np.array(res['month'],dtype=np.int64)
    res['T3Month'] = np.array(res['tem3'],dtype=np.int64)*np.array(res['month'],dtype=np.int64)  
  
    trainset = trainset.drop(['year','day'],axis=1) 
    testset = testset.drop(['year','day'],axis=1) 

#test all zone
newscore = []
ytest = getytest(testset,0) #zoneid 0
ytrain,yt = gety(train,cvset,0)
npo = Tmodelcom(testset,temp,[5, 9, 1])
xtest = npo.loc[npo['year']==2007]
npo = npo.iloc[:,1:]
xtest = xtest.iloc[:,1:]
m = npo.drop(npo.index[10320:10488])
m = m.drop(npo.index[12864:13032])
m = m.drop(npo.index[14832:15000])
m = m.drop(npo.index[17376:17544])
m = m.iloc[:16872,:]
m.index= [x for x in range(len(m))]
m['trend'] = m.index

lr = LinearRegression()
lr.fit(m,ytrain)
yact = lr.predict(xtest)
newscore.append(Score(ytest,yact))

##old Tmodel function 
def Tmodel(train,temp,i):
    ##initialize a trend variable ,which is in P82,
    ##HONG, TAO. Short Term Electric Load Forecasting.
    tempres = getSeriesTep(temp,i)
    #following code generate hour data
    res = genhour(tempres)
    res.index = [j for j in range(len(res))]
    res['trend'] = res.index+1
    res['tem2'] = np.array(res.iloc[:,4],dtype=np.int64)**2
    res['tem3'] = np.array(res.iloc[:,4],dtype=np.int64)**3 
    ##UPDATE 11/15
    ##update11/17,iloc nd1-nd3
    ##update 11/19,revise code
    ec = OneHotEncoder()
    ec.fit(np.array(res['day']).reshape((-1,1)))
    nd = (ec.transform(np.array(res['day']).reshape((-1,1))).toarray())#[:,1:]
    res = pd.concat([res,pd.DataFrame(nd)],axis=1)
    
    ec = OneHotEncoder()
    ec.fit(np.array(res['month']).reshape((-1,1)))
    nd2 = (ec.transform(np.array(res['month']).reshape((-1,1))).toarray())#[:,1:]
    res = pd.concat([res,pd.DataFrame(nd2)],axis=1)
    
    ec = OneHotEncoder()
    ec.fit(np.array(res['hour']).reshape((-1,1)))
    nd3 = (ec.transform(np.array(res['hour']).reshape((-1,1))).toarray())#[:,1:]
    res = pd.concat([res,pd.DataFrame(nd3)],axis=1)
    res = res.drop(['day','month','hour'],axis=1)   
    
    hourday = adadot(nd3,nd)
    thour = adadot(np.array(res['temperature']).reshape((-1,1)),nd3)
    t2hour = adadot(np.array(res['tem2']).reshape((-1,1)),nd3)
    t3hour = adadot(np.array(res['tem3']).reshape((-1,1)),nd3)
    tmonth = adadot(np.array(res['temperature']).reshape((-1,1)),nd2)
    t2month = adadot(np.array(res['tem2']).reshape((-1,1)),nd2)
    t3month = adadot(np.array(res['tem3']).reshape((-1,1)),nd2)
    res = pd.concat([res,pd.DataFrame(hourday),pd.DataFrame(thour),pd.DataFrame(t2hour),
                     pd.DataFrame(t3hour),pd.DataFrame(tmonth),pd.DataFrame(t2month),
                                 pd.DataFrame(t3month)],axis=1)
    
    return res.iloc[:,1:]

def genhour(tempres):
    data = newgenhour(tempres)
    daynew = np.ones((24,1642))
    con = 0
    for i in range(0,len(data),24):#
        mul = datetime(int(data.iloc[i,0]), int(data.iloc[i,1]), int(data.iloc[i,2])).weekday()+1  
        daynew[:,con] = daynew[:,con] * mul
        con = con+1
    data['day'] = daynew.T.reshape((-1,1))               
    return data   

def scale():
    ##code from main.py
    sc = StandardScaler()
    m = sc.fit_transform(m)
    sc1 = StandardScaler()
    sc2 = StandardScaler()
    xtrain = sc1.fit_transform(xtrain)
    xtest = sc2.fit_transform(xtest)
    
def cutdata():
    ##from Tmodel and tmodelcom
    c = res.loc[(res['year']==2004) | (res['year']==2005)]
    c = c.loc[~((c['year']==2005) & (c['month']==3)&(c['day'].isin([x for x in range(6,13)])))]
    c = c.loc[~((c['year']==2005) & (c['month']==6)&(c['day'].isin([x for x in range(20,27)])))]
    c = c.loc[~((c['year']==2005) & (c['month']==9)&(c['day'].isin([x for x in range(10,17)])))]
    trainset = c.loc[~((c['year']==2005) & (c['month']==12)&(c['day'].isin([x for x in range(25,32)])))]
    c = res.loc[(res['year']==2006)]
    c = c.loc[~((c['year']==2006) & (c['month']==2)&(c['day'].isin([x for x in range(13,20)])))]
    c = c.loc[~((c['year']==2006) & (c['month']==5)&(c['day'].isin([x for x in range(25,32)])))]
    c = c.loc[~((c['year']==2006) & (c['month']==8)&(c['day'].isin([x for x in range(2,9)])))]
    testset = c.loc[~((c['year']==2006) & (c['month']==11)&(c['day'].isin([x for x in range(22,29)])))]
    
    ##from Tmodel
    c = res.loc[(res['year']==2004) | (res['year']==2005)]
    c = c.loc[~((c['year']==2005) & (c['month']==3)&(c['day'].isin([x for x in range(6,13)])))]
    c = c.loc[~((c['year']==2005) & (c['month']==6)&(c['day'].isin([x for x in range(20,27)])))]
    c = c.loc[~((c['year']==2005) & (c['month']==9)&(c['day'].isin([x for x in range(10,17)])))]
    trainset = c.loc[~((c['year']==2005) & (c['month']==12)&(c['day'].isin([x for x in range(25,32)])))]
#   
n = load.loc[load['year']==2007].iloc[:,4:]
test = testset.iloc[:,4:]
res = np.sum(np.array(n)-np.array(test))

#xtrain.to_csv(r'E:\Global Energy Forecasting Competition 2012 - Load Forecasting\GEFCOM2012_Data\update\xtrain.csv')
#xtest.to_csv(r'E:\Global Energy Forecasting Competition 2012 - Load Forecasting\GEFCOM2012_Data\update\xtest.csv')
#pd.DataFrame(ytrain).to_csv(r'E:\Global Energy Forecasting Competition 2012 - Load Forecasting\GEFCOM2012_Data\update\ytrain.csv')
#pd.DataFrame(ytest).to_csv(r'E:\Global Energy Forecasting Competition 2012 - Load Forecasting\GEFCOM2012_Data\update\ytest.csv')

##newscore = []
#ytrain,ytest = sysloadtest(load)
#xtrain,xtest = Ttest(temp,[3, 6, 7, 0, 9, 5, 2, 8, 4 ,1 ,10])
#lr = Ridge(alpha=100,tol=1e-12)
##lr = LinearRegression(fit_intercept=False)
#lr.fit(xtrain,ytrain)
#yact = lr.predict(xtest)
#newscore.append(Score(ytest,yact))
#np.linalg.matrix_rank(np.array(xtest.iloc[:,:]))