# -*- coding: utf-8 -*-
from scrapy import Spider
from scrapy.http import Request

def validate_field(field):
    if field:
        field.strip()
        field = field.replace("\r\n", "")
    else:
        field = ""
    return field

class BatdongsanSpider(Spider):
    name = 'batdongsan'
    allowed_domains = ['batdongsan.com.vn']
    start_urls = ['http://batdongsan.com.vn/']

    def parse(self, response):
        type_urls = response.xpath('//*[@class="dropdown-navigative-menu"]/li/a/@href')[0:2].extract()
        #type_urls = response.xpath('//*[@class="dropdown-navigative-menu"]/li/a/@href')[1:2].extract()
        for type_url in type_urls:
            type_url = response.urljoin(type_url)
            yield Request(type_url, callback=self.parse_pages)

    def parse_pages(self, response):
        item_urls = response.xpath('//*[@class="p-title"]/h3/a/@href').extract()
        for item_url in item_urls:
            item_url = response.urljoin(item_url)
            yield Request(item_url, callback=self.parse_info)

        next_page_number = 2

        try:
            while(next_page_number < 11):
                if '/nha-dat-ban' in response.request.url:
                    absolute_next_page_url = 'https://batdongsan.com.vn/nha-dat-ban/p' + str(next_page_number)
                elif '/nha-dat-cho-thue' in response.request.url:
                    absolute_next_page_url = 'https://batdongsan.com.vn/nha-dat-cho-thue/p' + str(next_page_number)

                #absolute_next_page_url = 'https://batdongsan.com.vn/nha-dat-ban/p' + str(next_page_number)
                yield Request(absolute_next_page_url, callback=self.parse_pages)
                next_page_number = next_page_number + 1
        except:
            pass

    def parse_info(self, response):
        name = response.xpath('//*[@id="LeftMainContent__productDetail_contactName"]/div/following-sibling::div/text()').extract_first()
        mobile = response.xpath('//*[@id="LeftMainContent__productDetail_contactMobile"]/div/following-sibling::div/text()').extract_first()
        url = response.request.url

        name = validate_field(name)
        mobile = validate_field(mobile)

        yield {
            'URL': url,
            'Name': name,
            'Mobile': mobile
        }
