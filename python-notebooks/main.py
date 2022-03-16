# IMPORTS
import pymongo
import pandas as pd
import requests as req
import logging
import json
from time import sleep
from tqdm import tqdm #For Progress Bars
from bs4 import BeautifulSoup as bs
import xml.etree.ElementTree as et

###############################################################################
# Configuration

head = {
    "User-Agent": "Digital-Alpha SEC Explorer/1.0",
    "Connection": "keep-alive"
}

company_data = pd.read_csv('./data/company_summary.csv')

logging.basicConfig(filename='error.log', encoding='utf-8', level=logging.DEBUG)

###############################################################################
# FUNCTIONS

def getFormData(root,base_url):
    trigger_list = [
    'BALANCE SHEETS',
    'CASH FLOW',
    'STATEMENTS OF OPERATIONS',
    'STATEMENTS OF COMPREHENSIVE INCOME',
    'SELECTED FINANCIAL DATA'
    'PROPERTY'
    ] # List of triggers to look for in table names
    keypoints = [
    'profit',
    'total assets',
    'total liabilities',
    'net loss',
    'net profit',
    'net cash',
    'net sales',
    'gross margin',
    'net income',
    'total comprehensive income'
    'total property'
    ] # List of triggers to look for in table entries

    data_dict = {}

    '''
    Getting Form Data
    Function Complexity:
    O(ABC) where
    A = number of reports
    B = number of trigger lists
    C = number of keypoints
    since B and C are fairly constant, the problem is essentially
    O(A)
    '''

    for report in root.iter('Report'):
        for trigger_word in trigger_list:
            if trigger_word.lower() in report.find('ShortName').text.lower():
                try:
                    content_dat = req.get(base_url + '/' + report.find('HtmlFileName').text, headers=head)
                    content_soup = bs(content_dat.text, 'html')
                except:
                    logging.error('cannot find name or url in component')
                    break

                data_dict['units'] = 'ones'
                try:
                    for i,row in enumerate(content_soup.table.find_all('tr')):
                        if (len(row.find_all('th')) != 0):
                            #Its a heading, check for units data:
                            header_text = [ e.text.strip() for e in row.find_all('th') ]
                            for h in header_text:
                                if 'thousand' in h.lower():
                                    data_dict['units'] = 'thousands'
                                    break
                                elif 'million' in h.lower():
                                    data_dict['units'] = 'millions'
                                    break
                                elif 'billion' in h.lower():
                                    data_dict['units'] = 'billions'
                                    break
                        if (len(row.find_all('th')) == 0 and len(row.find_all('strong')) == 0):
                            try:
                                dat = [ e.text.strip() for e in row.find_all('td') ]
                                dat = [ d for d in  dat if d ]
                                dat = [ d for d in  dat if d != ' ' ]
                                try:
                                    if has_keypoints(dat[0],keypoints): data_dict[ dat[0].lower() ] = int(''.join(filter(lambda i: i.isdigit(), dat[1])))
                                except:
                                    data_dict[ dat[0].lower() ] = None
                                    logging.warning('Cannot convert to int: ')
                            except:
                                logging.warning('Error @ Row ', i, ' In Table ')
                except:
                    logging.error('JOE CONTENT GOT NO SOUP')
    return data_dict
    

def has_keypoints(str, list):
    for key in list:
        if key in str.lower():
            return True
    return False

head = {
    "User-Agent": "Digital-Alpha SEC Explorer/1.0",
    "Connection": "keep-alive"
}

###############################################################################
# Mongo Variables

mongo_url = "mongodb+srv://huntrag:killsasuke@cluster0.staij.mongodb.net/myFirstDatabase?authSource=admin&replicaSet=atlas-a852oq-shard-0&w=majority&readPreference=primary&appname=MongoDB%20Compass&retryWrites=true&ssl=true"
try:
    client = pymongo.MongoClient(mongo_url)
    print("Connected to MongoDb Successfully")
except:
    logging.error("DB CONN ERROR")

mydb = client['tech-meet']

form_data = mydb['form-data']

################################################################################
# Filling up the mongo db

mother_data = []

for i in tqdm(company_data.index, desc="Filling in the MongoDb"):
    # For every Company
    try:
        company_summary = json.loads(company_data["HISTORY"][i])
        file_shelf = company_summary["filings"]["recent"] #Holds the db of files
        cik_num = company_summary["cik"]
        tickers = company_summary['tickers']
        file_num = len(file_shelf['accessionNumber'])
    except:
        logging.error("Unknown Error @ Company ", cik_num)
        continue

    for k in range(file_num):
        #For every file in that company
        if file_shelf['form'][k].replace("-","").lower() in ["10k","10q"]:
            
            data_point = {}

            data_point['cik'] = int(cik_num)
            try:
                if tickers:
                    data_point['ticker'] = tickers[0]
                else:
                    data_point['ticker'] = None
            except:
                logging.warning('No tickers for', cik_num, ' But still going for access')
                pass
            data_point['form'] = file_shelf['form'][k]
            data_point['accession-number'] = file_shelf['accessionNumber'][k]
            data_point['date'] = file_shelf['reportDate'][k]
            data_point['url'] ="https://www.sec.gov/Archives/edgar/data/" + cik_num + "/" + file_shelf['accessionNumber'][k].replace("-", "") + "/" + file_shelf["primaryDocument"][k]

            #the root folder of the document
            base_url = "https://www.sec.gov/Archives/edgar/data/" + cik_num + "/" + file_shelf['accessionNumber'][k].replace("-", "")
            #Get its filings summary
            res = req.get(base_url + "/FilingSummary.xml", headers=head)
            try:
                root = et.fromstring(res.text)
            except:
                logging.error("Error in generating HTML Root at @", cik_num, " , " , file_shelf['accessionNumber'][k])
                pass
            # Store in dict format
            data_point['data'] = getFormData(root, base_url)
            mother_data.append(data_point)
            try:
                form_data.insert_one(data_point)
            except:
                logging.error("Error in inserting data for", cik_num, " , " , file_shelf['accessionNumber'][k])
                pass

with open("final_data.json", "w") as outfile:
    json.dump(mother_data, outfile)
