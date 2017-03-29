import threading
import time
import logging
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from collections import namedtuple

logger = logging.getLogger()
#logger.setLevel(logging.DEBUG)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter("%(levelname)-8s %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)


#Array of ChromeDrivers
Initial         = 15
Final           = 18
WindowCount     = Final - Initial + 1
chromedriver    = "/Users/SabareeshNikhil/Downloads/chromedriver"
chromedriver    = "C:/Python/chromedriver.exe"

url = 'https://fantasy.premierleague.com/a/statistics/total_points'

# Dict to map xpath of each stat. If there is an element with class ism-media, then the centre element of all the arrays below should be 2
XPATH = dict(   club            = ["//*[@id='ismr-element']/div/div[2]/div[",1,"]/div[1]/div/div[2]/div[1]/div[1]"],
                position        = ["//*[@id='ismr-element']/div/div[2]/div[",1,"]/div[1]/div/div[2]/div[1]/div[3]"],
                form            = ["//*[@id='ismr-element']/div/div[2]/div[",1,"]/div[1]/ul[1]/li[1]/div"],
                last_week_score = ["//*[@id='ismr-element']/div/div[2]/div[",1,"]/div[1]/ul[1]/li[2]/div"],
                total_score     = ["//*[@id='ismr-element']/div/div[2]/div[",1,"]/div[1]/ul[1]/li[3]/div"],
                price           = ["//*[@id='ismr-element']/div/div[2]/div[",1,"]/div[1]/ul[1]/li[4]/div"],
                teams_sel_by    = ["//*[@id='ismr-element']/div/div[2]/div[",1,"]/div[1]/ul[1]/li[5]/div"],
                net_influence   = ["//*[@id='ismr-element']/div/div[2]/div[",1,"]/div[1]/ul[2]/li[1]/div"],
                net_creativity  = ["//*[@id='ismr-element']/div/div[2]/div[",1,"]/div[1]/ul[2]/li[2]/div"],
                net_threat      = ["//*[@id='ismr-element']/div/div[2]/div[",1,"]/div[1]/ul[2]/li[3]/div"],
                net_ict         = ["//*[@id='ismr-element']/div/div[2]/div[",1,"]/div[1]/ul[2]/li[4]/div"]
    )

MatchData = list(['pno', 'name', 'matchweek', 'scoreline', 'points', 'minsplayed', 'goals', 'assists', 'cleansheets', 'goalsconceded', 'owngoals', 'penssaved', 'pensmissed', 'yellowcards', 'redcards', 'saves', 'bonus', 'bonuspts', 'influence', 'creativity', 'threat', 'ict', 'nettransfers', 'selectedby', 'value'])

#MatchData = namedtuple('MatchData', ['Opponent', 'Venue', 'TeamScore', 'OpponentScore', 'MinsPlayed', 'Goals', 'Assists', 'CleanSheets', 'GoalsConceded', 'OwnGoals', 'PensSaved', 'PensMissed', 'YellowCards', 'RedCards', 'Saves', 'Bonus', 'BonusPts', 'Influence'])
#PlayerData = namedtuple('PlayerData', ['PlayerNo', 'Name', 'Club', 'Position', 'Form', 'LastWeekScore', 'TotalScore', 'Price', 'TeamsSelBy', 'NetInfluence', 'Creativity', 'Threat', 'ICT', 'MatchList'])

def open_page(chromedriver, url, WindowCount) :
    """Function to call chromedriver and open webpage after authenticating"""
    DriverArray     = [webdriver.Chrome(chromedriver) for i in range(WindowCount)]
    for i in range(WindowCount):
        driver = DriverArray[i]
        driver.get(url)
        driver.implicitly_wait(10) # seconds
        logger.info("Opened webpage %s to read player stats using driver number %d",url,i)
    return DriverArray

def go_to_page(driver,page) :
    if page > 0:
        Next = driver.find_element_by_xpath('//*[@id="ismr-main"]/div/div[2]/a[1]')
        Next.click()
        page = page - 1
    for i in range(page):
        Next = driver.find_element_by_xpath('//*[@id="ismr-main"]/div/div[2]/a[3]/div[1]')
        Next.click()
    return driver
            

def read_data(driver,page) :
    try:
        count = 0
        df = pd.DataFrame(columns=list(XPATH.keys())+MatchData)

        #Go to the correct page number
        driver = go_to_page(driver,page)

        # Get all the players in the 1st page and print their names. Should modify the loop below so that it extract the other information as well and stores in a table
        players = driver.find_elements_by_xpath("//*[@id='ismr-main']/div/div[1]/table/tbody/tr")
        for pno in range(len(players)):
        #for pno in [0,1,2,3,4]:
            Button = driver.find_element_by_xpath("//*[@id='ismr-main']/div/div[1]/table/tbody/tr["+str(pno+1)+"]/td[1]/a")
            Button.click()
            name = driver.find_element_by_xpath('//*[@id="ismjs-dialog-title"]')
            print(name.text)
            StatusExists    = len(driver.find_elements_by_class_name("ism-element-status-bar__content")) #Check if a player is suspended or injured. Change the xpath accordingly
            pdata           = [driver.find_element_by_xpath(value[0]+str(value[1]+StatusExists)+value[2]).text.encode('ascii', 'ignore') for key, value in XPATH.items()]

            TableSize = 23
            Table     = driver.find_elements_by_xpath("//*[@id='ismr-element-history-this']/div/div/table//tr//td")
            ElemCount = 0
            RowData   = []
            for elem in Table:
                RowData.append(elem.text)
                if ElemCount < (TableSize-1) :
                    ElemCount += 1
                else:
                    mdata           = [pno,name.text] + RowData
                    df.loc[count]   = pdata + mdata
                    count          += 1
                    RowData         = []
                    ElemCount       = 0

            logger.info("Printed %d rows for %s, no %d", len(Table)/TableSize, name.text, pno)

            close = driver.find_element_by_xpath('//*[@id="ismr-element"]/div/div[1]/a')
            close.click()

    finally:
        writer = pd.ExcelWriter('Test'+str(page)+'.xlsx')
        df.to_excel(writer,'Sheet')
        writer.save()
        print(page)
        #return df



DriverArray = open_page(chromedriver, url,WindowCount)
for i in range(Initial,Final+1):
    t = threading.Thread(target=read_data, args = (DriverArray[i-Initial],i))
    t.daemon = True
    t.start()
 #DriverArray = [read_data(DriverArray[i],i) for i in range(5)]
