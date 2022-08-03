from datetime import datetime
from bs4 import BeautifulSoup
import requests
import json
import re


class GameWikiScraper:
    def __init__(self):
        self.square_bracket_trim = re.compile(r"\[.*?\]")

        self.base_url = "https://terraria.fandom.com/wiki"
        self.all_items = list()

        self.fetchWebPage()
        self.filterData()
        with open('items.json', 'w') as fp:
            json.dump(self.all_items, fp, indent=2)

    def fetchWebPage(self):
        r = requests.get(self.base_url+"/Guide:Class_setups")
        self.soup = BeautifulSoup(''.join(r.text), features="lxml")

    def filterData(self):
        info_cards = self.soup.find_all(
            "div", attrs={"class": "infocard clearfix"})
        for card in info_cards:
            class_container = card.find("div", attrs={"class": "hgroup"})
            if len(class_container) > 1:
                role = class_container.findChildren()[1].text.lower().replace(
                    "summoning", "summoner")
                game_stage = self.gameStageConvert(
                    class_container.findChildren()[0].text.lower())
                for item_container in card.find_all("div", attrs={"class": "box"}):
                    self.pullItems(item_container, role, game_stage)

            elif class_container.find("div", attrs={"class": "main"}).text in ["Mixed (early)", "Mixed (late)"]:
                role = "mixed"
                game_stage = 0
                for item_container in card.find_all("div", attrs={"class": "box"}):
                    self.pullItems(item_container, role, game_stage)

    def gameStageConvert(self, stage):
        game_stages = {
            "pre-bosses": 0,
            "pre-hardmode": 1,
            "pre-mech bosses": 2,
            "pre-plantera": 3,
            "pre-golem": 4,
            "pre-lunar events": 5,
            "endgame": 6
        }
        return game_stages.get(stage, 7)

    def pullItems(self, item_container, role, game_stage):
        if not item_container.find_all("li"):
            category = self.convertCategory(item_container.find(
                "div", attrs={"class": "title"}).text.lower())
            for span in item_container.find("p").find_all("span", attrs={"style": "display:block;margin:0.5em 0;"}):
                name = span.find("a").get("title")
                url_ext = span.find("a").get("href")
                imageTag = span.find("a").find("img")
                if hasattr(imageTag, "data-src") and imageTag.get("data-src"):
                    imgPath = imageTag.get("data-src")
                else:
                    imgPath = imageTag.get("src")
                this_item = {
                    "name": name.replace("(", "").replace(")", "").rstrip(),
                    "url": self.base_url+url_ext,
                    "imgPath": imgPath.split(".png")[0] + ".png",
                    "role": role,
                    "category": category,
                    "gameStageAvailable": game_stage}
                self.all_items.append(this_item)

        for item in item_container.find_all("li"):
            valid = True
            category = self.convertCategory(item_container.find(
                "div", attrs={"class": "title"}).text.lower())
            try:
                item_name = item.text.replace(
                    "(", "").replace(")", "").rstrip()
                item_name = self.square_bracket_trim.sub("", item_name)
            except:
                item_name = "unknown"
                valid = False
            try:
                item_url_extension = item.find("a")["href"]
            except:
                item_url_extension = "unknown"
                valid = False
            try:
                item_img_path = item.find("img")["src"].split(".png")[0]+".png"
            except:
                item_img_path = "unknown"
                valid = False
            if valid:
                this_item = {
                    "name": item_name,
                    "role": role,
                    "url": self.base_url+item_url_extension,
                    "imgPath": item_img_path,
                    "category": category,
                    "gameStageAvailable": game_stage}
                self.all_items.append(this_item)

    def convertCategory(self, category):
        if "buffs" in category:
            return 'buffs'
        else:
            return category


if __name__ == "__main__":
    time_format = "%H:%M:%S"
    start_time = datetime.now().strftime(time_format)
    print(f"Start time = {start_time}")
    try:
        GameWikiScraper()
    except KeyboardInterrupt:
        print("Goodbye")

    finish_time = datetime.now().strftime(time_format)
    print(f"Finish time = {finish_time}")
    time_delta = datetime.strptime(finish_time, time_format) - datetime.strptime(
        start_time, time_format
    )
    total_seconds = time_delta.total_seconds()
    minutes = total_seconds / 60
    print(f"Time elapsed = {minutes} (minutes)")
