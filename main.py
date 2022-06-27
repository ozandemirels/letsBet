import requests
from bs4 import BeautifulSoup
import pandas as pd
import urllib.request
import json
from datetime import date
from selenium import webdriver
from selenium.webdriver.common.by import By


def saveAsExcel(df):
    df.to_excel("C:/Users/ozan.demirel/Desktop/betVersus.xlsx")


nesineUrl = urllib.request.urlopen("https://bulten.nesine.com/api/bulten/getprebultenfull")
data = json.loads(nesineUrl.read())
#data = json.dumps(data, indent=2)

nesineMatches = []
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
                homeTeam = homeTeam.split(' ')
                for x in homeTeam:
                    print(homeTeam)
                    if len(x) <= 2:
                        homeTeam.remove(x)
                        print(homeTeam)
                if len(homeTeam) == 1:
                    homeTeam = homeTeam[0]
                elif len(homeTeam) == 2:
                    homeTeam = homeTeam[0] + ' ' + homeTeam[1]
                elif len(homeTeam) == 3:
                    homeTeam = homeTeam[0] + ' ' + homeTeam[1] + ' ' + homeTeam[2]
                homeTeam = homeTeam.replace('-', ' ')
                print(homeTeam)
                print()


                awayTeam = match['AN']
                awayTeam = awayTeam.split(' ')
                for y in awayTeam:
                    if len(y) <= 2:
                        awayTeam.remove(y)
                        print(awayTeam)
                if len(awayTeam) == 1:
                    awayTeam = awayTeam[0]
                elif len(awayTeam) == 2:
                    awayTeam = awayTeam[0] + ' ' + awayTeam[1]
                elif len(awayTeam) == 3:
                    awayTeam = awayTeam[0] + ' ' + awayTeam[1] + ' ' + awayTeam[2]
                awayTeam = awayTeam.replace('-', ' ')
                print(awayTeam)
                print()



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
                nesineMatches.append(['Nesine', homeTeam, awayTeam, str(ratioH), str(ratioD), str(ratioA)])


print(nesineMatches)
print()


tempoBetMatches = []
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
                element = element[1].split(' - ')
                print(element[0])
                print(element[1])
                temporaryList.append('TempoBet')
                for m in range(0, 2):
                    team = element[m]
                    team = team.split(' ')
                    print(team)
                    for y in team:
                        if len(y) <= 2:
                            team.remove(y)
                            print(team)
                    if len(team) == 1:
                        team = team[0]
                    elif len(team) == 2:
                        team = team[0] + ' ' + team[1]
                    elif len(team) == 3:
                        team = team[0] + ' ' + team[1] + ' ' + team[2]
                    elif len(team) == 4:
                        team = team[0] + ' ' + team[1] + ' ' + team[2] + '' + team[3]
                    print(team)

                    team = team.replace('-', ' ')
                    temporaryList.append(team)
            else:
                temporaryList.append(element)
        tempoBetMatches.append(temporaryList)

print(nesineMatches)
print(tempoBetMatches)

finalList = []
df = pd.DataFrame(data=finalList, columns=['Home', 'Away', 'Nesine1', 'Nesine0', 'Nesine2','Tempo1','Tempo0','Tempo2'])


print(len(nesineMatches))
print(len(tempoBetMatches))
for i in range(1, len(nesineMatches)+1):
    print(nesineMatches[i][1],nesineMatches[i][2])
    print()
    for j in range(1, len(tempoBetMatches)+1):
        print(i,j)
        print(tempoBetMatches[j][1], tempoBetMatches[j][2])
        print()
        if nesineMatches[i][1] == tempoBetMatches[j][1] and nesineMatches[i][2] == tempoBetMatches[j][2]:
            df.append(nesineMatches[i][1], nesineMatches[i][2], nesineMatches[3], nesineMatches[4], nesineMatches[5], tempoBetMatches[3], tempoBetMatches[4], tempoBetMatches[5])

print(df)
saveAsExcel(df)

