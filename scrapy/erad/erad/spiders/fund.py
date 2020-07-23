import scrapy
from erad.items import EradItem


class FundSpider(scrapy.Spider):
    name = 'fund'
    allowed_domains = ['www.e-rad.go.jp']

    def __init__(self, kensakutaisho, *args, **kwargs):
        super(FundSpider, self).__init__(*args, **kwargs)
        self.formdata = {
            "kensakuMoji": "00",
            "kensakuText": "",
            "kensakutaisho": kensakutaisho,
            "hyoujiKensu": "100",
            "downloadKb": "1",
            "nendo": "2020",
            "search": "abc",
        }

    def start_requests(self):
        FQDN = self.FQDN = "https://www.e-rad.go.jp"
        start_url = FQDN + "/erad/portal/jigyolist/present/present?locale=ja"
        yield scrapy.FormRequest(start_url, self.parse, formdata=self.formdata)

    def parse(self, response):
        for tr in response.css("table.list_color tr"):
            # 先頭行はデータを取得しない
            if tr.css("th"):
                continue
            # データを取得する
            item = EradItem()
            item["publishing_date"] = tr.xpath("td[1]/text()").extract_first()
            item["funding_agency"] = tr.xpath("td[2]/text()").extract_first()
            item["call_for_applications"] = tr.xpath(
                "td[3]/a/text()").extract_first()
            erad_url = tr.xpath("td[3]/a/@href").extract_first()
            item["erad_key"] = erad_url.split("/")[-2]
            item["erad_url"] = self.FQDN + erad_url.split(",")[0].split("'")[1]
            item["application_unit"] = tr.xpath("td[4]/text()").extract_first()
            item["approved_institution"] = tr.xpath(
                "td[5]/text()").extract_first()
            item["opening_date"] = tr.xpath("td[6]/text()").extract_first()
            item["closing_date"] = tr.xpath("td[7]/text()").extract_first()
            yield scrapy.Request(item["erad_url"],
                                 callback=self.parse_detail,
                                 meta={"item": item})

        next_page = response.css("div.btn_next a::attr(href)").extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)

    def parse_detail(self, response):
        item = response.meta["item"]
        item["url"] = response.xpath(
            "//*[@id='outline']/table/tr/th[contains(text(), '公募要領URL')]/following-sibling::td[1]/a/@href").get()
        yield item
