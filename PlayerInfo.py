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

# Go to the required webpage and login
chromedriver = "/Users/SabareeshNikhil/Downloads/chromedriver"
url = 'https://fantasy.premierleague.com/a/statistics/total_points'

# Dict to map xpath of each stat
XPATH = dict(club="//*[@id='ismr-element']/div/div[2]/div[1]/div[1]/div/div[2]/div[1]/div[1]",
                position="//*[@id='ismr-element']/div/div[2]/div[1]/div[1]/div/div[2]/div[1]/div[3]",
                form="//*[@id='ismr-element']/div/div[2]/div[1]/div[1]/ul[1]/li[1]/div",
                last_week_score="//*[@id='ismr-element']/div/div[2]/div[1]/div[1]/ul[1]/li[2]/div",
                total_score="//*[@id='ismr-element']/div/div[2]/div[1]/div[1]/ul[1]/li[3]/div",
                price="//*[@id='ismr-element']/div/div[2]/div[1]/div[1]/ul[1]/li[4]/div",
                teams_sel_by="//*[@id='ismr-element']/div/div[2]/div[1]/div[1]/ul[1]/li[5]/div",
                net_influence="//*[@id='ismr-element']/div/div[2]/div[1]/div[1]/ul[2]/li[1]/div",
                net_creativity="//*[@id='ismr-element']/div/div[2]/div[1]/div[1]/ul[2]/li[2]/div",
                net_threat="//*[@id='ismr-element']/div/div[2]/div[1]/div[1]/ul[2]/li[3]/div",
                net_ict="//*[@id='ismr-element']/div/div[2]/div[1]/div[1]/ul[2]/li[4]/div"
    )

MatchData = list(['pno', 'matchweek', 'scoreline', 'points', 'minsplayed', 'goals', 'assists', 'cleansheets', 'goalsconceded', 'owngoals', 'penssaved', 'pensmissed', 'yellowcards', 'redcards', 'saves', 'bonus', 'bonuspts', 'influence', 'creativity', 'threat', 'ict', 'nettransfers', 'selectedby', 'value'])
df = pd.DataFrame(columns=XPATH.keys()+MatchData)

#MatchData = namedtuple('MatchData', ['Opponent', 'Venue', 'TeamScore', 'OpponentScore', 'MinsPlayed', 'Goals', 'Assists', 'CleanSheets', 'GoalsConceded', 'OwnGoals', 'PensSaved', 'PensMissed', 'YellowCards', 'RedCards', 'Saves', 'Bonus', 'BonusPts', 'Influence'])
#PlayerData = namedtuple('PlayerData', ['PlayerNo', 'Name', 'Club', 'Position', 'Form', 'LastWeekScore', 'TotalScore', 'Price', 'TeamsSelBy', 'NetInfluence', 'Creativity', 'Threat', 'ICT', 'MatchList'])

def open_page(chromedriver, url) :
    """Function to call chromedriver and open webpage after authenticating"""
    driver = webdriver.Chrome(chromedriver)
    driver.get(url)
    driver.implicitly_wait(10) # seconds
    logger.info("Opened webpage %s to read player stats" % url)
    return driver

def read_data(driver) :
    try:
        count = 0
        # Get all the players in the 1st page and print their names. Should modify the loop below so that it extract the other information as well and stores in a table
        players = driver.find_elements_by_xpath("//*[@id='ismr-main']/div/div[1]/table/tbody/tr")
        #for pno in range(len(players)):
        for pno in range(20):
            Button = driver.find_element_by_xpath("//*[@id='ismr-main']/div/div[1]/table/tbody/tr["+str(pno+1)+"]/td[1]/a")
            Button.click()
            name = driver.find_element_by_class_name('ism-eiw-heading')
            pdata = [driver.find_element_by_xpath(XPATH[stat]).text.encode('ascii', 'ignore') for stat in XPATH.keys()]

            DataTable = driver.find_element_by_xpath("//*[@id='ismr-element-history-this']/div/div/table")
            TableRows = DataTable.find_elements_by_xpath("//*[@id='ismr-element-history-this']/div/div/table/tbody/tr")            
            for row in range(len(TableRows)):
                TableCols = driver.find_elements_by_xpath("//*[@id='ismr-element-history-this']/div/div/table/tbody/tr["+str(row+1)+"]/td")
                mdata= [pno] + [driver.find_element_by_xpath("//*[@id='ismr-element-history-this']/div/div/table/tbody/tr["+str(row+1)+"]/td["+str(col+1)+"]").text.encode('ascii', 'ignore') for col in range(len(TableCols))]
                df.loc[count] = pdata + mdata
                count += 1
            close = driver.find_element_by_xpath('//*[@id="ismr-element"]/div/div[1]/a')
            close.click()        
    finally:
        return df


driver = open_page(chromedriver, url)
df = read_data(driver)
print(df)
