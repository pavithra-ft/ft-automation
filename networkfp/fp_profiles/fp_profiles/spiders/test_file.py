import scrapy
from ..items import FpProfilesItem


class Fpprofiles(scrapy.Spider):
    name = "fpspider"
    allowed_domains = ['networkfp.com']

    def start_requests(self):
        urls = ['http://www.networkfp.com/members/']
        for url in urls:
            yield scrapy.Request(url=url, callback=self.link_parser)

    def link_parser(self, response):
        profile_links = response.css('li[class="member-view"] a::attr(href)').getall()
        for profile in profile_links:
            if profile.startswith("http"):
                yield scrapy.Request(url=profile, callback=self.profile_parser, dont_filter=True)

    def profile_parser(self, response):
        items = FpProfilesItem()
        name = response.css('div[class="comapny-info"] h2::text').get()
        if name:
            items['name'] = name.replace("\n", "").strip()

        designation = response.css('div[class="comapny-info"] p span::text').get()
        if designation:
            items['designation'] = designation.replace("\xa0", "")

        company = response.css('div[class="comapny-info"] p::text').get()
        if company:
            items['company'] = company.replace("\xa0", "")

        city = response.css('div[class="profile_lists"] ul li:nth-child(1)')
        if city:
            city_name = city.css('label::text').get()
            items['city'] = city_name

        mailid = response.css('div[class="profile_lists"] ul li:nth-child(2)')
        if mailid:
            mail = mailid.css('label::text').get()
            items['mailid'] = mail

        mobile = response.css('div[class="profile_lists"] ul li:nth-child(3)')
        if mobile:
            mobile_num = mobile.css('label::text').get()
            items['mobile'] = mobile_num

        amfi = response.css('div[class="profile_lists"] ul li:nth-child(4)')
        if amfi:
            amfi_arn = amfi.css('label::text').get()
            items['amfi_arn'] = amfi_arn

        site = response.css('div[class="profile_lists"] ul li:nth-child(5)')
        if amfi:
            website = site.css('label::text').get()
            items['website'] = website

        address = response.css('div[class="profile_lists"] ul li:nth-child(8)')
        if address:
            address_label = address.css('label::text').get()
            if address_label:
                items['address'] = address_label.replace("\r", "").replace("\n", "")

        yield items
