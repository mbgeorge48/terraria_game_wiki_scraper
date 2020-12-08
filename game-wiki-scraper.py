from bs4 import BeautifulSoup
import requests
import json
import re

URL = "https://terraria.gamepedia.com"
SQUAREBRACKETTRIM = re.compile("\[.*?\]")


def getWebPage():
    r = requests.get(URL+"/Guide:Class_setups")
    soup = BeautifulSoup(''.join(r.text), features="lxml")
    infocards = soup.find_all("div", attrs={"class": "infocard clearfix"})
    itemList = []
    for card in infocards:
        div = card.find("div", attrs={"class": "hgroup"})
        if len(div) > 1:
            role = div.findChildren()[1].text.lower().replace(
                "summoning", "summoner")
            gamestage = gameStageConvert(div.findChildren()[0].text.lower())
            for box in card.find_all("div", attrs={"class": "box"}):
                for item in box.find_all("li"):
                    valid = True
                    category = box.find("div", attrs={"class": "title"}).text
                    try:
                        itemName = item.text.replace(
                            "(", "").replace(")", "").rstrip()
                        itemName = SQUAREBRACKETTRIM.sub("", itemName)
                    except:
                        itemName = "unknown"
                        valid = False
                    try:
                        itemURLExtension = item.find("a")["href"]
                    except:
                        itemURLExtension = "unknown"
                        valid = False
                    try:
                        itemImgPath = item.find("img")["src"]
                    except:
                        itemImgPath = "unknown"
                        valid = False
                    if valid:
                        obj = {"name": itemName, "role": role,
                               "url": URL+itemURLExtension, "imgPath": itemImgPath, "category": category, "gameStageAvailable": gamestage}
                        itemList.append(obj)

    with open('items.json', 'w') as fp:
        json.dump(itemList, fp, indent=2)


def gameStageConvert(gameStageValue):
    gameStage = {
        "pre-bosses": "0",
        "pre-hardmode": "1",
        "pre-mech bosses": "2",
        "pre-plantera": "3",
        "pre-golem": "4",
        "pre-lunar events": "5",
        "endgame": "6"
    }
    return gameStage.get(gameStageValue, "unknown")


getWebPage()
# TODO
# Get Light Pets
# Get Pre Boss items
