from bs4 import BeautifulSoup
import requests
import json
import re

URL = "https://terraria.gamepedia.com"
SQUAREBRACKETTRIM = re.compile(r"\[.*?\]")

ITEMLIST = []


def getWebPage():
    r = requests.get(URL+"/Guide:Class_setups")
    soup = BeautifulSoup(''.join(r.text), features="lxml")
    infocards = soup.find_all("div", attrs={"class": "infocard clearfix"})
    for card in infocards:
        div = card.find("div", attrs={"class": "hgroup"})
        if len(div) > 1:
            role = div.findChildren()[1].text.lower().replace(
                "summoning", "summoner")
            gamestage = gameStageConvert(div.findChildren()[0].text.lower())
            for box in card.find_all("div", attrs={"class": "box"}):
                pullItems(box, role, gamestage)

        elif div.find("div", attrs={"class": "main"}).text in ["Mixed (early)", "Mixed (late)"]:
            role = "mixed"
            gamestage = "0"
            for box in card.find_all("div", attrs={"class": "box"}):
                pullItems(box, role, gamestage)

    with open('items.json', 'w') as fp:
        json.dump(ITEMLIST, fp, indent=2)


def pullItems(box, role, gamestage):
    if not box.find_all("li"):
        obj = {"name": box.find("p").text.replace("(", "").replace(")", "").rstrip(), "role": role, "url": URL+box.find("p").find("a")["href"], "imgPath": box.find("p").find("img")["src"], "category": box.find("div", attrs={"class": "title"}).text.lower(), "gameStageAvailable": gamestage}
        ITEMLIST.append(obj)
    for item in box.find_all("li"):
        valid = True
        category = box.find("div", attrs={"class": "title"}).text.lower()
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
            ITEMLIST.append(obj)


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
