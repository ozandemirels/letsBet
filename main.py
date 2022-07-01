import requests
from bs4 import BeautifulSoup
import pandas as pd
import urllib.request
import json
from datetime import date
import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By


def saveAsExcel(df):
    df.to_excel("C:/Users/ozan.demirel/Desktop/betVersus.xlsx")

matchList = []

nesineUrl = urllib.request.urlopen("https://bulten.nesine.com/api/bulten/getprebultenfull")
data = json.loads(nesineUrl.read())
#data = json.dumps(data, indent=2)


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
                    if bet['OCA'][i]['N'] == 1:
                        ratioH = bet['OCA'][i]['O']
                    elif bet['OCA'][i]['N'] == 2:
                        ratioD = bet['OCA'][i]['O']
                    elif bet['OCA'][i]['N'] == 3:
                        ratioA = bet['OCA'][i]['O']
                matchList.append(['Nesine', homeTeam, awayTeam, str(ratioH), str(ratioD), str(ratioA)])


driver = webdriver.Chrome()
driver.get('https://www.690tempobet.com/todays_football.html')
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
            if k == 1:
                temporaryList.append('TempoBet')
                element = element.split('\n')
                element = element[1].split(' - ')
                for m in range(0, 2):
                    team = element[m]
                    temporaryList.append(team)
            else:
                temporaryList.append(element)
        matchList.append(temporaryList)
driver.close()

print()
for i in range(0, len(matchList)):
    for j in range(1, 3):
        matchList[i][j] = matchList[i][j].lower().replace('.', '').replace(' utd', ' united').replace('atl ', 'atletico ')
        matchList[i][j] = str(matchList[i][j]).split(' ')
        for word in matchList[i][j]:
            if len(word) <= 2:
                matchList[i][j].remove(word)
        teamName = ''
        for word in matchList[i][j]:
            teamName = teamName + word + ' '
        matchList[i][j] = teamName[:-1]


finalList = []
for i in range(0, len(matchList)):
    if matchList[i][0] == 'Nesine':
        for j in range(0, len(matchList)):
            if matchList[j][0] == 'TempoBet' and matchList[i][1] == matchList[j][1] and matchList[i][2] == matchList[j][2]:
                finalList.append([matchList[i][1], matchList[i][2], matchList[i][3], matchList[i][4], matchList[i][5], matchList[j][3], matchList[j][4], matchList[j][5]])

print(len(finalList))
df = pd.DataFrame(data=finalList, columns=['Home', 'Away', 'Nesine1', 'Nesine0', 'Nesine2', 'TempoBet1', 'TempoBet0', 'TempoBet2'])

print(df)
saveAsExcel(df)

