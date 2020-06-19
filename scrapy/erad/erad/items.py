# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class EradItem(scrapy.Item):
    publishing_date = scrapy.Field()
    funding_agency = scrapy.Field()
    call_for_applications = scrapy.Field()
    application_unit = scrapy.Field()
    approved_institution = scrapy.Field()
    opening_date = scrapy.Field()
    closing_date = scrapy.Field()
    url = scrapy.Field()
    id = scrapy.Field()
