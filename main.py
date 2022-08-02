import os
import shutil
import sys
from datetime import datetime
from bs4 import BeautifulSoup
import requests
import json
import re


class GameWikiScraper:
    def __init__(self):
        self.square_bracket_trim = re.compile(r"\[.*?\]")

        self.url = "https://terraria.fandom.com/wiki"
        self.all_items = list()

        self.fetchWebPage()
        self.filterData()

    def fetchWebPage(self):
        r = requests.get(self.url+"/Guide:Class_setups")
        self.soup = BeautifulSoup(''.join(r.text), features="lxml")

    def filterData(self):
        infocards = self.soup.find_all(
            "div", attrs={"class": "infocard clearfix"})
        for card in infocards:
            classContainer = card.find("div", attrs={"class": "hgroup"})
            if len(classContainer) > 1:
                role = classContainer.findChildren()[1].text.lower().replace(
                    "summoning", "summoner")
                gamestage = self.gameStageConvert(
                    classContainer.findChildren()[0].text.lower())
                print(role, gamestage)
                for itemContainer in card.find_all("div", attrs={"class": "box"}):
                    self.pullItems(itemContainer, role, gamestage)

            elif classContainer.find("div", attrs={"class": "main"}).text in ["Mixed (early)", "Mixed (late)"]:
                role = "mixed"
                gamestage = 0
                for itemContainer in card.find_all("div", attrs={"class": "box"}):
                    self.pullItems(itemContainer, role, gamestage)

    def gameStageConvert(self, stage):
        gameStage = {
            "pre-bosses": 0,
            "pre-hardmode": 1,
            "pre-mech bosses": 2,
            "pre-plantera": 3,
            "pre-golem": 4,
            "pre-lunar events": 5,
            "endgame": 6
        }
        return gameStage.get(stage, 7)

    def pullItems(self, itemContainer, role, gamestage):
        # Look for span rather than li!
        if not itemContainer.find_all("li"):
            print(f"i'm an itemcontainer\n{itemContainer.find('p').text}\n\n")
            this_item = {
                "name": itemContainer.find("p").text.replace("(", "").replace(")", "").rstrip(),
                "role": role, "url": self.url+itemContainer.find("p").find("a")["href"],
                "imgPath": (itemContainer.find("p").find("img")["src"].split(".png")[0]+".png"),
                "category": itemContainer.find("div", attrs={"class": "title"}).text.lower(),
                "gameStageAvailable": gamestage}

            self.all_items.append(this_item)

        for item in itemContainer.find_all("li"):
            valid = True
            category = itemContainer.find(
                "div", attrs={"class": "title"}).text.lower()
            try:
                itemName = item.text.replace(
                    "(", "").replace(")", "").rstrip()
                itemName = self.square_bracket_trim.sub("", itemName)

            except:
                itemName = "unknown"
                valid = False
            try:
                itemURLExtension = item.find("a")["href"]
            except:
                itemURLExtension = "unknown"
                valid = False
            try:
                itemImgPath = item.find("img")["src"].split(".png")[0]+".png"
            except:
                itemImgPath = "unknown"
                valid = False
            if valid:
                this_item = {
                    "name": itemName,
                    "role": role,
                    "url": self.url+itemURLExtension,
                    "imgPath": itemImgPath,
                    "category": category,
                    "gameStageAvailable": gamestage}
                self.all_items.append(this_item)


if __name__ == "__main__":
    time_format = "%H:%M:%S"
    start_time = datetime.now().strftime(time_format)
    print(f"Start time = {start_time}")
    try:
        GameWikiScraper()
    except IOError:
        print("Ran into issues reading/copying files")
        print(
            "Check you've got enough disk space/your folder permissions/your folder path"
        )
    except KeyboardInterrupt:
        print("Goodbye")
    except Exception as e:
        print(e)
    finish_time = datetime.now().strftime(time_format)
    print(f"Finish time = {finish_time}")
    time_delta = datetime.strptime(finish_time, time_format) - datetime.strptime(
        start_time, time_format
    )
    total_seconds = time_delta.total_seconds()
    minutes = total_seconds / 60
    print(f"Time elapsed = {minutes} (minutes)")
