import time
from datetime import datetime
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


def parse_index(soup):
    table = soup.find("table", attrs={"class": "list_color"})
    rows = table.find_all("tr")
    scraped = []
    for row in rows:
        # 表面的に見えるテキスト部分を取得する
        cols = row.find_all("td")
        l = []
        for col in cols:
            if col:
                l.append(col.text)
            else:
                pass
        d = {}
        if l:
            # 公開日
            d["publishing_date"] = datetime.strptime(l[0], "%Y/%m/%d")
            # 配分機関
            d["funding_agency"] = l[1]
            # 公募名
            d["call_for_applications"] = l[2].replace("　", " ")
            # 応募単位
            d["application_unit"] = "".join(l[3].split())
            # 機関承認の有無
            d["approved_institution"] = "".join(l[4].split())
            # 受付開始日
            d["opening_date"] = datetime.strptime(l[5] + "+0900", "%Y/%m/%d %H:%M%z")
            # 受付終了日
            d["closing_date"] = datetime.strptime(l[6] + "+0900", "%Y/%m/%d %H:%M%z")
        # メタデータを取得する
        if row.find("a"):
            href = row.find("a").get("href").split(",")[0]
            # URLのディレクトリ部分
            href = href.split("'")[1]
            d["url"] = "https://www.e-rad.go.jp" + href
            # プライマリキー
            # reference_number = href.split("/")[-2]
            # d["reference_number"] = reference_number
            # 辞書を追加
            scraped.append(d)
    return scraped


def get_index():
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
    # soup = BeautifulSoup(r.text, "lxml")
    soup = BeautifulSoup(r.text)
    items = parse_index(soup)
    next_page = soup.find("div", attrs={"class": "btn_next hover pagelink_next"})
    while next_page:
        dynamic_url = urljoin(BASE_URL, next_page.find("a").get("href"))
        time.sleep(1)
        r = s.get(dynamic_url)
        # soup = BeautifulSoup(r.text, "lxml")
        soup = BeautifulSoup(r.text)
        next_page = soup.find("div", attrs={"class": "btn_next hover pagelink_next"})
        items_add = parse_index(soup)
        try:
            items.extend(items_add)
        except:
            pass
        try:
            dynamic_url = urljoin(BASE_URL, next_page.find("a").get("href"))
        except:
            pass
    return items
