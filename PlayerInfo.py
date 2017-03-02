import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# Go to the required webpage and login
driver = webdriver.Chrome("C:/Python/chromedriver.exe")
driver.get('https://fantasy.premierleague.com/')

username = driver.find_element_by_name('login')
password = driver.find_element_by_name('password')
username.send_keys("mathprofessor92@gmail.com")
password.send_keys("1123581321")

submit   = driver.find_element_by_xpath("//button[@type='submit']")
submit.click()


driver.implicitly_wait(10) # seconds
# Go to the transfers page
#driver.get('https://fantasy.premierleague.com/a/squad/transfers')
driver.get('https://fantasy.premierleague.com/a/statistics/total_points')

try:
    element = WebDriverWait(driver, 10).until(
#        EC.presence_of_element_located((By.XPATH, u"//a[@title='View player information']"))
        EC.presence_of_element_located((By.XPATH, u"//*[@id='ismr-main']/div/div[1]/table/tbody/tr[1]/td[1]/a"))
        
    )
    element.click()

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
    DataTable = driver.find_element_by_xpath("//*[@id='ismr-element-history-this']/div/div/table")
    TableRows = DataTable.find_elements_by_xpath("//*[@id='ismr-element-history-this']/div/div/table/tbody/tr")
    print(len(TableRows))
    
    for i in range(len(TableRows)):
        TableCols = driver.find_elements_by_xpath("//*[@id='ismr-element-history-this']/div/div/table/tbody/tr["+str(i+1)+"]/td")
        print(len(TableCols))
        for j in range(len(TableCols)):
            TableElem = driver.find_element_by_xpath("//*[@id='ismr-element-history-this']/div/div/table/tbody/tr["+str(i+1)+"]/td["+str(j+1)+"]")
            print(TableElem.text)
    
    
finally:
    print("blah")

#try:
#    element = WebDriverWait(driver, 10).until(
#        EC.presence_of_element_located((By.XPATH, u"//*[@id='ismjs-element-filter']"))
#    )
#finally:
#    print("blah")

#view = driver.find_element_by_xpath("//*[@id='ismjs-element-filter']")
#view = driver.find_element_by_xpath("//optgroup[@label='Global']")
#view.click()
#view.send_keys(Keys.ARROW_DOWN)
