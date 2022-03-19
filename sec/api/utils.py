import pandas as pd
from dotenv import load_dotenv
import os
import pymongo
from sklearn.linear_model import LinearRegression
from xml.etree import ElementTree as et
load_dotenv()
MONGODB_URI = os.environ['MONGODB_URI']
import numpy as np
headers={'user-agent':'Mozilla/5.0 (X11; Fedora; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'}

def normalized(a, axis=-1, order=2):
    l2 = np.atleast_1d(np.linalg.norm(a, order, axis))
    l2[l2==0] = 1
    return a / np.expand_dims(l2, axis)

def fetchCompanyMetrics(cik,startDate,endDate):
    client = pymongo.MongoClient(MONGODB_URI)
    mydb = client['tech-meet']
    form_data = mydb['form-data']
    find_q = {
        "cik": int(cik),
        "$and": [
            {"date": {"$gte": startDate}},
            {"date": {"$lte": endDate}}
        ]
    }
    docs = form_data.find(find_q).sort('date',1)
    #To get common attribs
    sample_10q = form_data.find_one({"cik": cik, "form": "10-Q"}) 

    resdata = {}
    resdata['date'] = []
    for key in sample_10q['data'].keys():
        if key == 'units':
            continue
        resdata[key] = []
    for doc in docs:
        for key in resdata.keys():
            if key == 'date':
                continue
            try:
                resdata[key].append(doc['data'][key])
            except:
                resdata[key].append(None)
        resdata['date'].append(doc['date'])
    return resdata

def generateDF(cik,nval,startDate,endDate = "2024-01-01"):
    '''
    Generates a dataframe from the data fetched from the API
    '''
    metrics = fetchCompanyMetrics(cik,startDate,endDate)
    datdf = pd.DataFrame.from_dict(metrics)
    finaldict = {}
    for col in datdf.columns:
        if col == 'date':
            finaldict[col] = []
            for q in range(nval):
                try:
                    finaldict[col].append( str(int(datdf['date'].iloc[-4+q][:4])+1)+"-"+str(datdf['date'].iloc[-4+q][5:]) )
                    # print(finaldict[col])
                except:
                    print("Insufficient Values, cannot predict")
                    break
            continue
        init = [ x for x in datdf[col] if  not pd.isnull(x) ]
        datdf[col] = datdf[col].fillna(0)
        finaldict[col] = getMLR(init,int(len(init)/6),nval)
    outdf = pd.DataFrame.from_dict(finaldict)
    datdf = pd.concat([datdf,outdf],ignore_index=True)
    return datdf

def getMLR(series,inp_dim,out_length):
    features = []
    target = []
    for i in range(len(series) - inp_dim):
        features.append(series[i:i+inp_dim])
        target.append(series[i+inp_dim])
    features = np.array(features)
    target = np.array(target)

    model = LinearRegression()
    model.fit(features,target)

    out = []

    for _ in range(out_length):
        npout = model.predict( [ series[-inp_dim:] ] )
        out.append( np.abs(npout[0]) )
        series.append(out[-1])

    return out

#function to convert dataframes to json
#newfile is dataframe assuming column names are the keys
def convertToJson(newfile):  
    res=[]
    mapping=[]
    for r in newfile:
        mapping.append(r)
    for i in range(newfile.shape[0]):
        dic={}
        for keys in mapping:
            dic[keys]=newfile.iloc[i][keys]
        res.append(dic)
    return res