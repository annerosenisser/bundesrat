# This script runs on Python 2! (?)

# ***************************************** #
# Useful inspiration for Selenium crawler:
# https://github.com/voliveirajr/seleniumcrawler/blob/master/seleniumcrawler/spiders/seleniumcrawler_spider.py


# ***************************************** #
from bs4 import BeautifulSoup
from selenium import webdriver
# See the official documentation for selenium at
# http://selenium-python.readthedocs.io/getting-started.html
from selenium.webdriver.common.keys import Keys

import pandas as pd # for easy storing of data.

import urllib
import re

# ***************************************** #
# Create an empty dictionary in which I will store the data:
# The dictionary should contain the abbreviations for all
# committees as well as one remainder category for data that
# can't be identified (for example wrongly published committee names
# on the website
committees = ['AV', 'AIS', 'AA', 'EU', 'Fz', 'FJ', 'G', 'In',
              'K', 'R', 'Wo', 'U', 'Vk', 'V', 'Wi', 'other']

meetings = ['year', 'id', 'date', 'committees'] + committees

meetings = pd.DataFrame(columns = meetings) # empty pd dataframe for each
# meeting ("Beratungsvorgang")

# ***************************************** #
# Define the years for which you want to have the data:
# 2014 to 2016. (can be extended to greater time periods by
# changing start and end year).
startyear = 2014
endyear = 2016
years = list(range(startyear, endyear + 1))

# Define the websites that should be scraped (starturls):
websites = ["http://www.bundesrat.de/DE/dokumente/beratungsvorgaenge/" + \
            str(year) + "/beratungsvorgaenge-node.html" for year in years]


# ***************************************** #
# Open the websites:
driver = webdriver.Firefox()

# Start with just one website for developing the script:
driver.get("http://www.bundesrat.de/DE/dokumente/beratungsvorgaenge/2015/beratungsvorgaenge-node.html")


tops = driver.find_elements_by_xpath("//li[contains(@class, 'top-item type-')]")

# top = tops[2] # for development
top = driver.find_element_by_xpath("//li[contains(@id, 'top-644/15')]") # for development
top = driver.find_element_by_xpath("//li[contains(@id, 'top-643/15')]") # for development
top = driver.find_element_by_xpath("//li[contains(@id, 'top-640/15')]") # for development


for top in tops:
    top_nr = (top.find_element_by_xpath(".//h2[@class='top-number']")).text
    print(top_nr)

    top_nr_short = top_nr.split("/")[0]
    top_nr_short = int(top_nr_short)

    # details = top.find_element_by_xpath(".//div[@class='top-item-switcher']")
    # details.click()
    # details.send_keys("\n")
    #  this works for 644/15, 640/15
    # However, it does not effectively OPEN the drop-down menu.

    details = top.find_element_by_xpath(".//div[@class='top-item-switcher']/a")
    # details.click()
    #  this works for 640/15
    # it does NOT work for 644/15

    details.send_keys("\n")
    #  this works for 644/15, 643/15, 640/15
    # see http://stackoverflow.com/questions/8832858/using-python-bindings-selenium-webdriver-click-is-not-working-sometimes

    # try: # for even numbers
        # details = top.find_element_by_class_name("top-item-switcher")
        # details.click()
        # this works for 640/15
        # it does NOT work for 644/15

    # except:
    #     details = top.find_elements_by_tag_name("a")[0]
    #     details.click()
        # this works for 643/15
        # it does NOT work for 644/15


    # else:
    #     print("Could not access details for %s" % top_nr)


    # details = top.find_elements_by_xpath("//a[1]")[0] # this SHOULD work for odd numbers
    # (though it doesn't). ...
    # it does NOT work for 644/15



    # If there are details on the committees involved, get those details:
    date = top.find_element_by_xpath("//p[@class='date']").text

    year = date.split(".")[-1]

    try:
        committees = top.find_element_by_xpath("//h3[contains(text(), 'Ausschusszuweisung')]/following-sibling::p").text

        com_list = committees.replace(" (fdf)", "").split(" - ")

        # add a function for coding "(fdf)" ("federführend") later!!

        meeting = pd.DataFrame({'id': [top_nr],
                                'date': date,
                                'committees': committees,
                                'AV': (1 if 'AV' in com_list else 0),  # note: this should be put in a function later!
                                'AIS': (1 if 'AIS' in com_list else 0),
                                'AA': (1 if 'AA' in com_list else 0),
                                'EU': (1 if 'EU' in com_list else 0),
                                'Fz': (1 if 'Fz' in com_list else 0),
                                'FJ': (1 if 'FJ' in com_list else 0),
                                'G': (1 if 'G' in com_list else 0),
                                'In': (1 if 'In' in com_list else 0),
                                'K': (1 if 'K' in com_list else 0),
                                'R': (1 if 'R' in com_list else 0),
                                'Wo': (1 if 'Wo' in com_list else 0),
                                'U': (1 if 'U' in com_list else 0),
                                'Vk': (1 if 'Vk' in com_list else 0),
                                'V': (1 if 'V' in com_list else 0),
                                'Wi': (1 if 'Wi' in com_list else 0),
                                'year': year})

    except: # if no details on the "Ausschusszuweisung" given:
        meeting = pd.DataFrame({'id': [top_nr],
                                'date': date,
                                'year': year})

    # meetings.iloc[:, 3:17] = meetings.iloc[:, 3:17].astype(int)
    meetings = meetings.append(meeting)

# Write output to file:
meetings.to_csv('bundestag.txt', header=True, index=None, sep=' ', mode='a')




# Close the driver:
driver.close()



# ***************************************** #
# Unused, old code (potentially to be used again):
# html = driver.page_source
# soup = BeautifulSoup(html,  "lxml")

# for link in soup.find_all('h2', attrs={"class": "top-number"}):
#     top_nr = link.get_text()
#     meeting = pd.DataFrame({'id': [top_nr]})
#     meetings = meetings.append(meeting)
