# This script runs on Python 2! (?)

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

meetings = ['year', 'id', 'committees'] + committees

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


html = driver.page_source
soup = BeautifulSoup(html,  "lxml")


for link in soup.find_all('h2', attrs={"class": "top-number"}):
    top_nr = link.get_text()
    meeting = pd.DataFrame({'id': [top_nr]})
    meetings = meetings.append(meeting)



driver.close()