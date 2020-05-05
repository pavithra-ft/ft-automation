import scrapy
from ..items import FpLinkedInItem


class Fpprofiles(scrapy.Spider):
    name = "linkedin"
    allowed_domains = ['networkfp.com']

    def start_requests(self):
        urls = ['http://www.networkfp.com/members/']
        for url in urls:
            yield scrapy.Request(url=url, callback=self.link_parser)

    def link_parser(self, response):
        profile_links = response.css('li[class="member-view"] a::attr(href)').getall()
        items = FpLinkedInItem()
        for profile in profile_links:
            if profile.startswith("https://in.linkedin.com"):
                items['link'] = profile
                yield items
