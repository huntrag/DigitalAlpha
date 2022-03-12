from bs4 import BeautifulSoup
import requests

headers={'user-agent':'Mozilla/5.0 (X11; Fedora; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'}


def getSummary(cik):
    url=f'https://sec.report/CIK/{cik}'
    html_file=requests.get(url,headers=headers).text
    soup=BeautifulSoup(html_file,'lxml')

    match=soup.find('div',class_='panel-body')

    return match.text

