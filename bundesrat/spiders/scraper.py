# This script runs on Python 3!

# ***************************************** #
# Useful inspiration and docs for Selenium crawler:
# https://github.com/voliveirajr/seleniumcrawler/blob/master/seleniumcrawler/spiders/seleniumcrawler_spider.py
# http://stackoverflow.com/questions/17975471/selenium-with-scrapy-for-dynamic-page
# https://seleniumhq.github.io/selenium/docs/api/py/api.html

# ***************************************** #
from scrapy.spiders import Spider
from scrapy import Request

from bundesrat.items import MeetingsItem

from selenium import webdriver
# See the official documentation for selenium at
# http://selenium-python.readthedocs.io/getting-started.html
from selenium.webdriver.common.keys import Keys

import time
from random import randint, uniform

import re # for string matching

# ***************************************** #
class BundesratSpider(Spider):

    name = "BundesratSpider"
    allowed_domains = ["bundesrat.de"]

    # Define the years for which you want to have the data:
    # 2014 to 2016. (can be extended to greater time periods by
    # changing start and end year).
    startyear = 2014
    endyear = 2016
    years = list(range(startyear, endyear + 1))

    # Define the websites that should be scraped (starturls):
    start_urls = ["http://www.bundesrat.de/DE/dokumente/beratungsvorgaenge/" + \
                  str(year) + "/beratungsvorgaenge-node.html" for year in years]

    start_urls = ["http://www.bundesrat.de/DE/dokumente/beratungsvorgaenge/2014/beratungsvorgaenge-node.html"] # for development
    # start_urls = ["http://www.bundesrat.de/DE/dokumente/beratungsvorgaenge/2007/beratungsvorgaenge-node.html?cms_gtp=5032152_list%253D24"]


# ***************************************** #
    def __init__(self):
        self.driver = webdriver.Firefox()

    def parse(self, response):
        self.driver.get(response.url)

        print(response.url)
        time.sleep(uniform(2,3))

        # Start with just one website for developing the script:
        # driver.get("http://www.bundesrat.de/DE/dokumente/beratungsvorgaenge/2015/beratungsvorgaenge-node.html") # for development


        tops = self.driver.find_elements_by_xpath("//li[contains(@class, 'top-item type-')]")

        # top = tops[2] # for development
        # top = driver.find_element_by_xpath("//li[contains(@id, 'top-644/15')]") # for development
        # top = driver.find_element_by_xpath("//li[contains(@id, 'top-643/15')]") # for development
        # top = driver.find_element_by_xpath("//li[contains(@id, 'top-529/08')]") # for development

        # ***************************************** #
        for top in tops:
            item = MeetingsItem()
            top_nr = (top.find_element_by_xpath(".//h2[@class='top-number']")).text
            # print(top_nr)
            item['id'] = top_nr

            title = (top.find_element_by_xpath(".//h2/a")).text
            item['title'] = title

            details = top.find_element_by_xpath(".//div[@class='top-item-switcher']/a")

            details.send_keys("\n")
            #  this works for 644/15, 643/15, 640/15
            # see http://stackoverflow.com/questions/8832858/using-python-bindings-selenium-webdriver-click-is-not-working-sometimes

            time.sleep(uniform(2,3))  # I need to wait until the new content has appeared!!! Better wait longer, gives less errors,
            # makes script more stable.

            mustend = time.time() + 30 # give loop maximum of 20 seconds.
            date = None
            # http://stackoverflow.com/questions/4606919/in-python-try-until-no-error
            while date is None and time.time() < mustend: # necessary condition to break the while loop
                try:
                    date = (top.find_elements_by_xpath(".//div[@class='zusatztitel']/following-sibling::p"))[0].text
                    item['date'] = date

                except:
                    time.sleep(uniform(3, 4))
                    print("Slept as pop-up was not shown yet.")


            year = date.split(".")[-1]
            item['year'] = year

            # If there are details on the committees involved, get those details:
            com_list2 = ['AV', 'EU', 'Fz', 'FJ', 'G', 'In',
                         'K', 'R', 'Wo', 'U', 'Vk', 'V', 'Wi', 'other']

            try:
                committees = (top.find_element_by_xpath(".//h3[contains(text(), 'Ausschusszuweisung')]/following-sibling::p")).text

                item['committees'] = committees

                fdf = committees.split(" - ")
                fdf = str([i for i in fdf if "fdf" in i][0])
                fdf = fdf.replace(" (fdf)", "")
                item['fdf'] = fdf

                com_list = committees.replace(" (fdf)", "").split(" - ")

                for com in com_list2[2:]:
                    # print(com)
                    item[com] = (1 if com in com_list else 0)

                item["AA"] =  (1 if len([c for c in ["AA", "A"] if c in com_list]) >0 else 0 )# there a two alternative
                # abbreviations for the "AA" committee on the website: "AA" and "A"
                item["AIS"] = (1 if len([c for c in ["AIS", "AS"] if c in com_list]) >0 else 0 ) # there a two alternative
                # abbreviations for the "AIS" committee on the website: "AIS" and "AS"

            except: # if no details on the "Ausschusszuweisung" given:
                # Define the items as None:
                item['committees'] = None
                item['fdf'] = None
                for com in com_list2:
                    # print(com)
                    item[com] = None
                item["AA"] = None
                item["AIS"] = None
                pass

            print(item)
            yield item

        # ***************************************** #
        # # Go to the next page and continue scraping:
        try: # only if there are older pages to follow.
            next_page = self.driver.find_element_by_xpath("//li[@class='next']/a").get_attribute("href")
            time.sleep(4)
            yield Request(next_page, callback=self.parse)

        except:
            print("Last page reached")
            pass


        # ***************************************** #
    # Close the driver (only at the end of the process):
    def __del__(self):
        # self.driver.close() # sometimes better not to close, as I then can see
        # on which page the scraper stopped. This is helpful for potential debugging.
        pass