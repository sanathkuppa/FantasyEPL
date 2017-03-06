import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys


# Go to the required webpage 
driver = webdriver.Chrome("C:/Python/chromedriver.exe")
driver.get('https://fantasy.premierleague.com/a/statistics/total_points')
driver.implicitly_wait(10) # seconds

try:
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, u"//*[@id='ismr-main']/div/div[1]/table/tbody/tr[1]/td[1]/a"))
        
    )
    element.click()

    # Get the main attributes for the first player - Should be made neat later 
    name = driver.find_element_by_class_name('ism-eiw-heading')
    print(name.text) # Player name
    club = driver.find_element_by_xpath("//*[@id='ismr-element']/div/div[2]/div[1]/div[1]/div/div[2]/div[1]/div[1]")
    print(club.text)
    position = driver.find_element_by_xpath("//*[@id='ismr-element']/div/div[2]/div[1]/div[1]/div/div[2]/div[1]/div[3]")
    print(position.text)
    form = driver.find_element_by_xpath("//*[@id='ismr-element']/div/div[2]/div[1]/div[1]/ul[1]/li[1]/div")
    print(form.text)
    LastWeekScore = driver.find_element_by_xpath("//*[@id='ismr-element']/div/div[2]/div[1]/div[1]/ul[1]/li[2]/div")
    print(LastWeekScore.text)
    TotalScore = driver.find_element_by_xpath("//*[@id='ismr-element']/div/div[2]/div[1]/div[1]/ul[1]/li[3]/div")
    print(TotalScore.text)
    Price = driver.find_element_by_xpath("//*[@id='ismr-element']/div/div[2]/div[1]/div[1]/ul[1]/li[4]/div")
    print(Price.text)
    TSB = driver.find_element_by_xpath("//*[@id='ismr-element']/div/div[2]/div[1]/div[1]/ul[1]/li[5]/div")
    print(TSB.text)
    Influence = driver.find_element_by_xpath("//*[@id='ismr-element']/div/div[2]/div[1]/div[1]/ul[2]/li[1]/div")
    print(Influence.text)
    Creativity = driver.find_element_by_xpath("//*[@id='ismr-element']/div/div[2]/div[1]/div[1]/ul[2]/li[2]/div")
    print(Creativity.text)
    Threat = driver.find_element_by_xpath("//*[@id='ismr-element']/div/div[2]/div[1]/div[1]/ul[2]/li[3]/div")
    print(Threat.text)
    ICT = driver.find_element_by_xpath("//*[@id='ismr-element']/div/div[2]/div[1]/div[1]/ul[2]/li[4]/div")
    print(ICT.text)

    # Main Data for the first player
    DataTable = driver.find_element_by_xpath("//*[@id='ismr-element-history-this']/div/div/table")
    TableRows = DataTable.find_elements_by_xpath("//*[@id='ismr-element-history-this']/div/div/table/tbody/tr")
    print(len(TableRows))

    # Printing the main data for the first player
##    for i in range(len(TableRows)):
##        TableCols = driver.find_elements_by_xpath("//*[@id='ismr-element-history-this']/div/div/table/tbody/tr["+str(i+1)+"]/td")
##        print(len(TableCols))
##        for j in range(len(TableCols)):
##            TableElem = driver.find_element_by_xpath("//*[@id='ismr-element-history-this']/div/div/table/tbody/tr["+str(i+1)+"]/td["+str(j+1)+"]")
##            print(TableElem.text)

    # Close the first player's dialog
    close = driver.find_element_by_xpath('//*[@id="ismr-element"]/div/div[1]/a')
    close.click()

    # Get all the players in the 1st page and print their names. Should modify the loop below so that it extract the other information as well and stores in a table
    players = driver.find_elements_by_xpath("//*[@id='ismr-main']/div/div[1]/table/tbody/tr")
    for i in range(len(players)):
        Button = driver.find_element_by_xpath("//*[@id='ismr-main']/div/div[1]/table/tbody/tr["+str(i+1)+"]/td[1]/a")
        Button.click()
        name = driver.find_element_by_class_name('ism-eiw-heading')
        print(name.text) # Player name
        close = driver.find_element_by_xpath('//*[@id="ismr-element"]/div/div[1]/a')
        close.click()
finally:
    print("blah")
