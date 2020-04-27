from django.core.management import BaseCommand
import time
from datetime import datetime
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

from erad.models import Item


class Command(BaseCommand):
    help = "scraping test"

    def handle(self, *args, **options):
        scraped = self.get_index()
        for d in scraped:
            Item.objects.update_or_create(url=d["url"], defaults=d)

        self.stdout.write(self.style.SUCCESS("success!"))

    def get_index(self):
        BASE_URL = "https://www.e-rad.go.jp"
        # 1st cycle
        URL = urljoin(BASE_URL, "/erad/portal/jigyolist/present/present/")
        s = requests.Session()
        r = s.post(
            URL,
            data={
                "hyoujiKensu": "100",
                "kensakuMoji": "00",
                "kensakuText": "",
                "kensakutaisho": "1",
                "hyoujiKensu": "100",
                "search": "abc",
            },
        )
        soup = BeautifulSoup(r.text, "html.parser")
        items = self.parse_index(soup)
        next_page = soup.find(
            "div", attrs={"class": "btn_next hover pagelink_next"})
        while next_page:
            dynamic_url = urljoin(BASE_URL, next_page.find("a").get("href"))
            time.sleep(1)
            r = s.get(dynamic_url)
            soup = BeautifulSoup(r.text, "html.parser")
            next_page = soup.find(
                "div", attrs={"class": "btn_next hover pagelink_next"})
            items_add = self.parse_index(soup)
            try:
                items.extend(items_add)
            except Exception:
                pass
            try:
                dynamic_url = urljoin(
                    BASE_URL, next_page.find("a").get("href"))
            except Exception:
                pass
        return items

    def parse_index(self, soup):
        table = soup.find("table", attrs={"class": "list_color"})
        rows = table.find_all("tr")
        scraped = []
        for row in rows:
            # テキストを取得する
            cols = row.find_all("td")
            txt = []
            for col in cols:
                if col:
                    txt.append(col.text)
            d = {}
            if txt:
                d["publishing_date"] = datetime.strptime(txt[0], "%Y/%m/%d")
                d["funding_agency"] = txt[1]
                d["call_for_applications"] = txt[2].replace("　", " ")
                d["application_unit"] = "".join(txt[3].split())
                d["approved_institution"] = "".join(txt[4].split())
                d["opening_date"] = datetime.strptime(
                    txt[5] + "+0900", "%Y/%m/%d %H:%M%z")
                d["closing_date"] = datetime.strptime(
                    txt[6] + "+0900", "%Y/%m/%d %H:%M%z")
            # メタデータを取得する
            if row.find("a"):
                href = row.find("a").get("href").split(",")[0]
                href = href.split("'")[1]
                d["url"] = "https://www.e-rad.go.jp" + href
                # 辞書を追加
                scraped.append(d)
        return scraped
