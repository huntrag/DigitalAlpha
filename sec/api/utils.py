from bs4 import BeautifulSoup
import requests
import pandas as pd
import pymongo
# from transformers import BertTokenizer, BertForSequenceClassification
from sklearn.linear_model import LinearRegression
from xml.etree import ElementTree as et
import re
import numpy as np


# finbert = BertForSequenceClassification.from_pretrained('sec\\finbert-tone',num_labels=3)
# tokenizer = BertTokenizer.from_pretrained('sec\\finbert-tone')

# print(finbert.eval()) # Uncomment to Check for Model

headers={'user-agent':'Mozilla/5.0 (X11; Fedora; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'}

def normalized(a, axis=-1, order=2):
    l2 = np.atleast_1d(np.linalg.norm(a, order, axis))
    l2[l2==0] = 1
    return a / np.expand_dims(l2, axis)

# def getSentiment(cik,asc):
#     asc = asc.replace("-", "")
#     cik = str(cik)
#     base_url = "https://www.sec.gov/Archives/edgar/data/" + cik + "/" + asc
#     xml_tree = requests.get(base_url + "/FilingSummary.xml", headers=headers)
#     trigger_one = 'DISCLOSURE' # We will primarily look for these documents
#     trigger_list = ['ACCOUNTING', 'LEASES', 'DEBT','COMMITMENTS','STOCK',] # List of triggers to look for in each document name
#     resdata = {} #Dict to hold end results
#     root = et.fromstring(xml_tree.text) # Fetch XML ROOT
#     for report in root.iter('Report'):
#             for trigger_word in trigger_list:
#                 #Check if the trigger words exists in the document name
#                 partname = report.find('LongName').text
#                 if (trigger_word.lower() in partname.lower() and trigger_one.lower() in partname.lower()):
#                     if ("table" in partname.lower() or "details" in partname.lower()):
#                         continue
#                     soup = BeautifulSoup(requests.get(base_url + '/' + report.find('HtmlFileName').text,headers=headers).text, 'lxml')
#                     # Fragment the stripped text into list of sentences
#                     txt_list_unrefined = re.split( r' *[\n\.\?!][\'"\)\]]* *' , soup.text.strip())
#                     # Remove short sequences
#                     txt_list = [ txt for txt in txt_list_unrefined if len(txt) > 100 ]
#                     # Encode The Sentence
#                     encoded_text = tokenizer(txt_list, return_tensors="pt", padding=True)
#                     # Predict the sentiment tensor
#                     sentiment_tensor = finbert(**encoded_text)[0].detach().numpy()
#                     # Get the non-zero sentiments
#                     refined_sentiment = [i for i in sentiment_tensor if np.argmax(i) != 0]
#                     #Run their average, if all sentiments are neutral, average those instead
#                     if refined_sentiment:
#                         average_sentiment = np.average( refined_sentiment, axis=0)
#                     else:
#                         average_sentiment = np.average( sentiment_tensor, axis=0)
#                     # do some modifications to the average sentiment

#                     minval = np.min(average_sentiment)
                    
#                     for i in range(3):
#                         average_sentiment[i] = (average_sentiment[i] - minval)

#                     sumval = np.sum(average_sentiment)
#                     for i in range(3):
#                         average_sentiment[i] = average_sentiment[i]/sumval
#                     if average_sentiment[1] > 0.5:
#                         resdata[partname] = 'good'
#                     elif average_sentiment[2] > 0.5:
#                         resdata[partname] = 'bad'
#                     else:
#                         resdata[partname] = 'neutral'
#                     break
#     return resdata

def fetchCompanyMetrics(cik,startDate,endDate):
    '''
    
    '''
    mongo_url = "mongodb+srv://huntrag:killsasuke@cluster0.staij.mongodb.net/myFirstDatabase?authSource=admin&replicaSet=atlas-a852oq-shard-0&w=majority&readPreference=primary&appname=MongoDB%20Compass&retryWrites=true&ssl=true"
    client = pymongo.MongoClient(mongo_url)
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
    sample_10q = form_data.find_one({"cik": cik, "form": "10-Q"}) #To get common attribs

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
                    
                except:
                    print("Insufficient Values, cannot predict")
                    break
            continue
        init = [ x for x in datdf[col] if  not pd.isnull(x) ]
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
def convertToJson(newfile):  #newfile is dataframe assuming column names are the keys
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
    
# print(getSentiment(1342936,"0001342936-12-000012"))

# CDK = fetchCompanyMetrics(796343,"1800-00-00","2023-00-00")
# for key in CDK.keys():
#     print(key,": ",len(CDK[key])," nulls: ",CDK[key].count(None))

# newfile = pd.DataFrame.from_dict(CDK)
# newfile.to_csv("CDK.csv")

CDK = generateDF(796343,1,"1800-00-00","2023-00-00")
newfile = pd.DataFrame.from_dict(CDK)
newfile.to_csv("CDK.csv")
