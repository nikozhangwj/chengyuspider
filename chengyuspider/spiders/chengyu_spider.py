import lxml
import scrapy
from bs4 import BeautifulSoup
from chengyuspider.items import ChengyuspiderItem


class ChenyuSpider(scrapy.Spider):

    name = "chengyu"

    def start_requests(self):

        urls = ["http://chengyu.t086.com/list/{0}_1.html".format(chr(i)) for i in range(ord("A"), ord("Z")+1)]
        # urls = ["http://chengyu.t086.com/list/A_1.html"]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        soup = BeautifulSoup(response.body, "lxml")
        # 找到成语列表
        div_listw = soup.find('div', class_='listw')
        # 找到分页信息
        mainbar3 = soup.find('div', class_='mainbar3')
        a2 = mainbar3.find('div', class_='a2')
        curpage = a2.find('span', class_='curpage').get_text()
        # 查看是否存在下一页
        has_next_page = a2.find(text="下一页")

        # 遍历列表获取item
        for ul in div_listw.ul:
            detail_url = 'http://chengyu.t086.com' + ul.a['href']
            yield scrapy.Request(detail_url, callback=self.parse_detil)

        # 通过判断是否存在下一页决定是否继续爬取该字母开头分类
        if has_next_page:
            next_page = str(int(curpage) + 1)
            url_split = response.url.split("/")
            url_end = url_split[-1].replace(curpage, next_page)
            url_split[-1] = url_end
            next_url = '/'.join(url_split)
            yield scrapy.Request(next_url, callback=self.parse)

    def parse_detil(self, response):
        # 实例化bs
        soup = BeautifulSoup(response.body, "lxml")
        # 找到目标div
        main_div = soup.find('div', id='main')
        # 直截取索引前五个tr
        all_tr = main_div.find_all('tr')[:4]
        # 实例化item
        item = ChengyuspiderItem()
        item['chengyu'] = all_tr[0].find_all('td')[1].get_text()
        item['pronunce'] = all_tr[1].find_all('td')[1].get_text()
        item['meanings'] = all_tr[2].find_all('td')[1].get_text()
        item['from_where'] = all_tr[3].find_all('td')[1].get_text()
        item['url'] = response.url
        yield item
