from bs4 import BeautifulSoup
import requests
from transformers import BertTokenizer, BertForSequenceClassification
from xml.etree import ElementTree as et
import re
import numpy as np


finbert = BertForSequenceClassification.from_pretrained('sec\\finbert-tone',num_labels=3)
tokenizer = BertTokenizer.from_pretrained('sec\\finbert-tone')

# print(finbert.eval()) # Uncomment to Check for Model

headers={'user-agent':'Mozilla/5.0 (X11; Fedora; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'}

def normalized(a, axis=-1, order=2):
    l2 = np.atleast_1d(np.linalg.norm(a, order, axis))
    l2[l2==0] = 1
    return a / np.expand_dims(l2, axis)

def getSentiment(cik,asc):
    base_url = "https://www.sec.gov/Archives/edgar/data/" + cik + "/" + asc
    xml_tree = requests.get(base_url + "/FilingSummary.xml", headers=headers).text
    trigger_one = 'DISCLOSURE' # We will primarily look for these documents
    trigger_list = ['ACCOUNTING', 'LEASES', 'DEBT','COMMITMENTS','STOCK',] # List of triggers to look for in each document name

    resdata = {} #Dict to hold end results

    root = et.fromstring(xml_tree.text) # Fetch XML ROOT

    for report in root.iter('Report'):
            for trigger_word in trigger_list:
                #Check if the trigger words exists in the document name
                partname = report.find('LongName').text
                if (trigger_word.lower() in partname.lower() and trigger_one.lower() in partname.lower()):
                    if ("table" in partname.lower() or "details" in partname.lower()):
                        continue
                    soup = BeautifulSoup(requests.get(base_url + '/' + report.find('HtmlFileName').text,headers=headers).text, 'html')
                    # Fragment the stripped text into list of sentences
                    txt_list_unrefined = re.split( r' *[\n\.\?!][\'"\)\]]* *' , soup.text.strip())
                    # Remove short sequences
                    txt_list = [ txt for txt in txt_list_unrefined if len(txt) > 100 ]
                    # Encode The Sentence
                    encoded_text = tokenizer(txt_list, return_tensors="pt", padding=True)
                    # Predict the sentiment tensor
                    sentiment_tensor = finbert(**encoded_text)[0].detach().numpy()
                    # Get the non-zero sentiments
                    refined_sentiment = [i for i in sentiment_tensor if np.argmax(i) != 0]
                    #Run their average, if all sentiments are neutral, average those instead
                    if refined_sentiment:
                        average_sentiment = np.average( refined_sentiment, axis=0)
                    else:
                        average_sentiment = np.average( sentiment_tensor, axis=0)
                    # do some modifications to the average sentiment
                    minval = np.min(average_sentiment)
                    maxval = np.max(average_sentiment)
                    for i in range(3):
                        average_sentiment[i] = (average_sentiment[i] - minval)/(maxval - minval)
                    resdata[partname] = {
                        'neutral': average_sentiment[0],
                        'good': average_sentiment[1],
                        'bad': average_sentiment[2]
                    }
                    break



def getSummary(cik):
    url=f'https://sec.report/CIK/{cik}'
    html_file=requests.get(url,headers=headers).text
    soup=BeautifulSoup(html_file,'lxml')

    match=soup.find('div',class_='panel-body')

    return match.text

