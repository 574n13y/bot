'''
PROJECT NAME : DAR ES SALAAM STOCK MARKET STOKS'S PERFORMANCE
URL          : https://www.dse.co.tz/dse/market-report
PROJECT BY   : MBONEA GODWIN MJEMA
DATE         : 6/22/2017

MODULES USED:
            1.PRETTYTABLE
            2.BEAUTIFULSOUP
            3.URLLIB

'''
#!/usr/bin/python3.4
#import the all important modules
import prettytable
from prettytable import PrettyTable
from bs4 import BeautifulSoup as bs
from requests import Session as browse


def init():
    #CREATE A PRETTYTABLE OBJECT
    table=PrettyTable()

    #lists
    closePrice=[]
    prevClose=[]
    priceChange=[]
    Company=[]

    
    #URL CONTANING THE WEBSITE
    url="https://www.dse.co.tz/dse/market-report"

    #CREATE A REQUEST
    Response=browse().get(url,verify=False)



    #CREATE A BEAUTIFULSOUP OBJECT PASS THE HTML CODE 
    soup=bs(Response.text,"html.parser")

    #GET RAW NAMES OF STOCKS THEY CONTAIN TAGS AND THE TABLE FROM THE WEBSITE
    raw_names= soup("table",{"class":"market-report-table table table table-hover table-striped sticky-enabled"})[0].tbody('tr')

    #TITLE OF THE TABLE
    title=soup("table",{"class":"market-report-table table table table-hover table-striped sticky-enabled"})[0].thead('tr')
    
    # MARKET REPORTS
    pdf=soup("a",{"class":"prev-reports"})[0].attrs["href"]
    


    #READ ALL THE ROWS
    for r in raw_names:
        tds = r('td')
        Company.append(str(tds[0].string))
        closePrice.append(str(tds[1].string))
        priceChange.append(str(tds[3].string))

    #READ THE TITLE AND PASS THE INFOMATION TO THE TABLE
    for t in title:
        ti=t('th')
        type(ti[0].string)
        table.add_column(ti[0].string,Company)
        table.add_column(ti[1].string,closePrice)
        table.add_column(ti[3].string,priceChange)
    return str(table),pdf

