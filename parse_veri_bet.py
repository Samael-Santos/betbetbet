# THIS IS INCOMPLETE, and only kinda works... sorry to waste your time, I'm still studying
# and I couldn't learn how to do it, do it and do everything I had to do today in time
# Picked this up mostly for the exp of appllying for a job in my area, so I can do better later
# I'll probally finish this project anyway, I accept feedback at samuel888santos@gmail.com
# Again, sorry for wasting your time

import requests
from bs4 import BeautifulSoup
import json

class Item:
    sport_league: str = ''     # sport as we classify it, e.g. baseball, basketball, football
    event_date_utc: str = ''   # date of the event, in UTC, ISO format
    team1: str = ''            # team 1 name
    team2: str = ''            # team 2 name
    pitcher: str = ''          # optional, pitcher for baseball
    period: str = ''           # full time, 1st half, 1st quarter and so on
    line_type: str = ''        # whatever site reports as line type, e.g. moneyline, spread, over/under
    price: str = ''            # price site reports, e.g. '-133' or '+105'
    side: str = ''             # side of the bet for over/under, e.g. 'over', 'under'
    team: str = ''             # team name, for over/under bets this will be either team name or total
    spread: float = 0.0        # for handicap and over/under bets, e.g. -1.5, +2.5

aObj = Item()

# resp = requests.get('https://veri.bet/x-ajax-oddspicks?sDate=3-14-2025&showAll=yes')
# dom = BeautifulSoup(resp.content, 'html.parser')

with open('Veri.bet.html') as file:
    dom = BeautifulSoup(file, 'html.parser')

fullData = dom.find_all('div', class_ ="col col-md")
for partData in fullData:
    secData = partData.find_all('span', class_ = 'text-muted')

    # COMMON PARAM
    aObj.period = secData[0].text[:-4].strip()
    aObj.team1 = secData[4].text.strip()
    aObj.team2 = secData[8].text.strip()
    sLeag = secData[12].text.strip()
    if sLeag != 'NBA' and sLeag != 'NHL' and sLeag != 'MMA' and sLeag != 'NCAAB' and sLeag != 'MLB':
        aObj.sport_league = 'Soccer'
    else:
        aObj.sport_league = secData[12].text.strip()
    # aObj.event_date_utc =

    # ML 1
    aObj.line_type = 'moneyline'
    aObj.price = secData[5].text.strip()
    aObj.side = aObj.team1
    aObj.team = aObj.team1
    aObj.spread = 0

    # DUMPING TESTING
    with open("bet_data.json", "r") as jsonFile:
        betData = json.load(jsonFile)

    with open("bet_data.json", "w") as jsonFile:
        new_entry = json.dumps(vars(aObj))
        betData['entries'].append(new_entry)
        json.dump(betData, jsonFile)


    # ML 2
    aObj.line_type = 'moneyline'
    aObj.price = secData[9].text.strip()
    aObj.side = aObj.team2
    aObj.team = aObj.team2
    aObj.spread = 0
    # DUMP 


    # ML 3 SOCCER
    if aObj.sport_league == "Soccer":
        aObj.line_type = 'moneyline'
        aObj.price = secData[13].text.strip()
        aObj.side = 'draw'
        aObj.team = 'draw'
        aObj.spread = 0


    # SPREAD 1
    aObj.line_type = 'spread'
    if secData[6].text.strip() == 'N/A':
        aObj.price = 'N/A'
    else: 
        price = secData[6].text
        aObj.price = price[price.find("(")+1:price.find(")")]
    aObj.side = aObj.team1
    aObj.team = aObj.team1
    if secData[6] == 'N/A':
        aObj.spread = 0
    else:
        spread = secData[6].text
        aObj.spread = spread[:spread.find("(")].strip()
    # DUMP


    # SPREAD 2
    aObj.line_type = 'spread'
    if secData[10].text.strip() == 'N/A':
        aObj.price = 'N/A'
    else: 
        price = secData[10].text.strip()
        aObj.price = price[price.find("(")+1:price.find(")")]
    aObj.side = aObj.team2
    aObj.team = aObj.team2
    if secData[10] == 'N/A':
        aObj.spread = 0
    else:
        spread = secData[10].text
        aObj.spread = spread[:spread.find("(")].strip()
    # DUMP


    #O/U 1
    aObj.line_type = 'over/under'
    if secData[11].text.strip() == 'N/A':
        aObj.price = 'N/A'
    else: 
        price = secData[7].text.strip()
        aObj.price = price[price.find("(")+1:price.find(")")]
    aObj.side = 'over'
    aObj.team = 'total'
    if secData[7] == 'N/A':
        aObj.spread = 0
    else:
        spread = secData[7].text.split()
        aObj.spread = spread[1]
    # DUMP


    #O/U 2
    aObj.line_type = 'over/under'
    if secData[11].text.strip() == 'N/A':
        aObj.price = 'N/A'
    else:
        price = secData[11].text.strip()
        aObj.price = price[price.find("(")+1:price.find(")")]
    aObj.side = 'over'
    aObj.team = 'total'
    if secData[11] == 'N/A':
        aObj.spread = 0
    else:
        spread = secData[11].text.split()
        aObj.spread = spread[1]
    # DUMP
