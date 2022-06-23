import time
import requests
from bs4 import BeautifulSoup
import pandas as pd
import urllib.request
import json
from datetime import date

jsonUrl = urllib.request.urlopen("https://bulten.nesine.com/api/bulten/getprebultenfull")
data = json.loads(jsonUrl.read())
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





print(nesineMatchList)
print(len(nesineMatchList))
time.sleep(55)





df = pd.DataFrame(data=orderDict(dic), columns=['Word', 'Count'])
saveAsExcel(df)

