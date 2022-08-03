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
                name = span.find("a").get("title").replace("(", "").replace(")", "").rstrip()
                url_ext = span.find("a").get("href")
                img_path = self.compareImgSrc(span.find("a").find("img"))

                this_item = {
                    "name": name,
                    "url": self.base_url+url_ext,
                    "imgPath": img_path,
                    "role": role,
                    "category": category,
                    "gameStageAvailable": game_stage}
                self.all_items.append(this_item)

        for item in item_container.find_all("li"):
            valid = True
            category = self.convertCategory(item_container.find(
                "div", attrs={"class": "title"}).text.lower())
            try:
                name = item.text.replace(
                    "(", "").replace(")", "").rstrip()
                name = self.square_bracket_trim.sub("", name)
            except:
                name = "unknown"
                valid = False
            try:
                url_ext = item.find("a")["href"]
            except:
                url_ext = "unknown"
                valid = False
            try:
                img_path = self.compareImgSrc(item.find("img"))
            except:
                img_path = "unknown"
                valid = False
            if valid:
                this_item = {
                    "name": name,
                    "role": role,
                    "url": self.base_url+url_ext,
                    "imgPath": img_path,
                    "category": category,
                    "gameStageAvailable": game_stage}
                self.all_items.append(this_item)

    def convertCategory(self, category):
        if "buffs" in category:
            return 'buffs'
        else:
            return category

    def compareImgSrc(self, image_tag):
        if hasattr(image_tag, "data-src") and image_tag.get("data-src") and image_tag.get("data-src").split(':')[0] != 'data' :
            path = image_tag.get("data-src")
        else:
            path = image_tag.get("src")
        print(path.split(".png")[0] + ".png")
        return path.split(".png")[0] + ".png"


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
