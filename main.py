import requests
from bs4 import BeautifulSoup
import pandas as pd
import urllib.request
import json
from datetime import date
from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

"""
nesineUrl = urllib.request.urlopen("https://bulten.nesine.com/api/bulten/getprebultenfull")
data = json.loads(nesineUrl.read())
#data = json.dumps(data, indent=2)

nesineMatchList = []
matchNum = -1
matches = data['sg']['EA']
today = str(date.today())
today = today[8:10] + '.' + today[5:7] + '.' + today[0:4]
for match in matches:
    matchNum += 1
    matchType = match['TYPE']
    matchDate = match['D']
    if matchType == 1 and matchDate == today:
        print(str(matchNum)+'. Matches data searching')
        bets = match['MA']
        betNum = -1
        for bet in bets:
            betNum += 1
            sov = bet['SOV']
            mtid = bet['MTID']
            if mtid == 1:
                homeTeam = match['HN']
                awayTeam = match['AN']
                ratioH = ''
                ratioD = ''
                ratioA = ''
                print(str(betNum)+'. Bet data searching')
                betCount = len(bet['OCA'])
                for i in range(0, betCount):
                    if bet['OCA'][i]['N'] == 1:   #bruada kaldın
                        ratioH = bet['OCA'][i]['O']
                    elif bet['OCA'][i]['N'] == 2:
                        ratioD = bet['OCA'][i]['O']
                    elif bet['OCA'][i]['N'] == 3:
                        ratioA = bet['OCA'][i]['O']
                nesineMatchList.append([homeTeam, awayTeam, ratioH, ratioD, ratioA])
"""



tempoBetMatchList = [[]]
driver = webdriver.Chrome()
driver.get('https://www.686tempobet.com/todays_football.html')
driver.maximize_window()
driver.implicitly_wait(15)

last_height = driver.execute_script("return document.body.scrollHeight")
while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        driver.execute_script("window.scrollTo(0, 0);")
        break
    last_height = new_height


tempoBetLeagueList = driver.find_elements(By.XPATH, '//div[@class="collapsible"]/div')
for i in range(1, len(tempoBetLeagueList)+1):
    tempoBetMatchList = driver.find_elements(By.XPATH, '//div[@class="collapsible"]/div[' + str(i) + ']/table/tbody/tr')
    for j in range(2, len(tempoBetMatchList)+1):
        temporaryList = []
        tempoBetMatchInfosList = driver.find_elements(By.XPATH, '//div[@class="collapsible"]/div[' + str(i) + ']/table/tbody/tr[' + str(j) + ']/td')
        for k in range(1, len(tempoBetMatchInfosList)):
            element = driver.find_element(By.XPATH, '//div[@class="collapsible"]/div[' + str(i) + ']/table/tbody/tr[' + str(j) + ']/td[' + str(k) + ']').text
            if k==1:
                element = element.split('\n')
                element = element[1].split('-')
                for l in range(0, 2):
                    if l==0:
                        element[l] = element[l][:-1]
                    else:
                        element[l] = element[l][1:]
                    temporaryList.append(element[l])
            else:
                temporaryList.append(element)

        print(temporaryList)


#df = pd.DataFrame(data=orderDict(dic), columns=['Word', 'Count'])
#saveAsExcel(df)

