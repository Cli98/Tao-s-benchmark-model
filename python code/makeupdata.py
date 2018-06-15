# -*- coding: utf-8 -*-
"""
Created on Tue Nov 21 12:48:28 2017

@author: Administrator
"""

##fill the data of eight weeks
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from support import dataget,getSeriesTep,Tmodel,Score,gety,combSeries,Tmodelcom,getytest
from support import Ttest,getnewytrain,newgenhour

#load = pd.read_csv(r'E:\Global Energy Forecasting Competition 2012 - Load Forecasting\GEFCOM2012_Data\newupdate\load.csv')
#loads = pd.read_csv(r'E:\Global Energy Forecasting Competition 2012 - Load Forecasting\GEFCOM2012_Data\newupdate\loads.csv').iloc[:,1:]

load = pd.read_csv(r'E:\Global Energy Forecasting Competition 2012 - Load Forecasting\GEFCOM2012_Data\update\load1.csv')
loads = pd.read_csv(r'E:\Global Energy Forecasting Competition 2012 - Load Forecasting\GEFCOM2012_Data\update\loads.csv').iloc[:,1:-1]

cols = [x for x in range(4,28)]
for i in range(1,21):
    c = loads.loc[(loads['zone_id']==i) &((loads['year']==2005) | (loads['year']==2006))]
    
    d = c.loc[((c['year']==2005) & (c['month']==3)&(c['day'].isin([x for x in range(6,13)])))]
    index = ((load['zone_id']==i)&(load['year']==2005) & (load['month']==3)&(load['day'].isin([x for x in range(6,13)]))).tolist()
    load.loc[index,load.columns[cols]] = np.array(d.iloc[:,4:])
    
    d = c.loc[((c['year']==2005) & (c['month']==6)&(c['day'].isin([x for x in range(20,27)])))]
    index = ((load['zone_id']==i)&(load['year']==2005) & (load['month']==6)&(load['day'].isin([x for x in range(20,27)]))).tolist()
    load.loc[index,load.columns[cols]] = np.array(d.iloc[:,4:])
    
    d = c.loc[((c['year']==2005) & (c['month']==9)&(c['day'].isin([x for x in range(10,17)])))]
    index = ((load['zone_id']==i)&(load['year']==2005) & (load['month']==9)&(load['day'].isin([x for x in range(10,17)]))).tolist()
    load.loc[index,load.columns[cols]] = np.array(d.iloc[:,4:])
    
    d = c.loc[((c['year']==2005) & (c['month']==12)&(c['day'].isin([x for x in range(25,32)])))]
    index = ((load['zone_id']==i)&(load['year']==2005) & (load['month']==12)&(load['day'].isin([x for x in range(25,32)]))).tolist()
    load.loc[index,load.columns[cols]] = np.array(d.iloc[:,4:])
    
    d = c.loc[((c['year']==2006) & (c['month']==2)&(c['day'].isin([x for x in range(13,20)])))]
    index = ((load['zone_id']==i)&(load['year']==2006) & (load['month']==2)&(load['day'].isin([x for x in range(13,20)]))).tolist()
    load.loc[index,load.columns[cols]] = np.array(d.iloc[:,4:])
    
    d = c.loc[((c['year']==2006) & (c['month']==5)&(c['day'].isin([x for x in range(25,32)])))]
    index = ((load['zone_id']==i)&(load['year']==2006) & (load['month']==5)&(load['day'].isin([x for x in range(25,32)]))).tolist()
    load.loc[index,load.columns[cols]] = np.array(d.iloc[:,4:])
    
    d = c.loc[((c['year']==2006) & (c['month']==8)&(c['day'].isin([x for x in range(2,9)])))]
    index = ((load['zone_id']==i)&(load['year']==2006) & (load['month']==8)&(load['day'].isin([x for x in range(2,9)]))).tolist()
    load.loc[index,load.columns[cols]] = np.array(d.iloc[:,4:])
    
    d = c.loc[((c['year']==2006) & (c['month']==11)&(c['day'].isin([x for x in range(22,29)])))]
    index = ((load['zone_id']==i)&(load['year']==2006) & (load['month']==11)&(load['day'].isin([x for x in range(22,29)]))).tolist()
    load.loc[index,load.columns[cols]] = np.array(d.iloc[:,4:])

res = load.loc[~(load['year']==2008)] 
res = np.sum(pd.isnull(res))
##1st test passed
##TO DO: Check difference with current dataset
load.to_csv(r'E:\Global Energy Forecasting Competition 2012 - Load Forecasting\GEFCOM2012_Data\newupdate\loadf.csv')
##End of stage 1

##stage2
load = pd.read_csv(r'E:\Global Energy Forecasting Competition 2012 - Load Forecasting\GEFCOM2012_Data\update\loadf.csv')
loadnew = pd.read_csv(r'E:\Global Energy Forecasting Competition 2012 - Load Forecasting\GEFCOM2012_Data\Load.csv')
a=[]
##Z7 incorrect
for i in range(1,21):
#    t1 = load.loc[(load['zone_id']==i) &((load['year']==2005) | (load['year']==2006))]
#    t2 = loadnew.loc[(loadnew['zone_id']==i) &((loadnew['year']==2005) | (loadnew['year']==2006))] 
    t1 = load.loc[(load['zone_id']==7) &( (load['year']==2006))]
    t2 = loadnew.loc[(loadnew['zone_id']==7) &( (loadnew['year']==2006))] 
    print np.sum(np.array(t1.iloc[:,4:]).reshape((-1,1))-np.array(t2.iloc[:,4:]).reshape((-1,1)))
    a.append(np.sum(np.array(t1.iloc[:,4:]).reshape((-1,1))-np.array(t2.iloc[:,4:]).reshape((-1,1))))
    
##A test for the function of combseries
seq = [x for x in range(11)]
res = combSeries(seq,temp)
d = np.array(res.iloc[:,4:]).reshape((-1,1))
## test passed
a = np.array([[1,2],[3,4],[5,7]]).T
b = np.array([[3,4],[5,7]]).T
res = adadot(a,b)
##adadot test passed