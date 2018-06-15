# -*- coding: utf-8 -*-
"""
Created on Sat Mar 03 23:00:04 2018

@author: Administrator
"""



def newgenhour(tempres):
    res = tempres.iloc[:,4:]
    #get all hours data in this weatherid
    res = np.array(res,dtype=np.float64).reshape((1,-1)).tolist()[0] 
    datamatrix = pd.DataFrame(repmat(np.array(tempres.iloc[:,1:4]),24,1))
    data = datamatrix.sort_values([0,1,2])
    data.columns =  ['year','month','day']
    data['hour'] = repmat(np.array([x for x in range(1,25)]).reshape((-1,1)),len(data)/24,1)
    data['temperature'] = res       
    return data      

def combSeries(seq,temp):
    res = np.array(getSeriesTep(temp,seq[0]),dtype = np.float64)
    for i in range(1,len(seq)):
        newtep = np.array(getSeriesTep(temp,seq[i]),dtype=np.float64)
        res = res+newtep
    res = np.array(res,dtype=np.float64)*1.0/len(seq)
    return pd.DataFrame(res)    