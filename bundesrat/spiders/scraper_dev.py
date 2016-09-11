# This script runs on Python 3!

# Development version of the scraper.
# import time
#
# from selenium import webdriver
# import selenium.webdriver.support.ui as UI
#
# start_urls = ["http://www.bundesrat.de/DE/dokumente/beratungsvorgaenge/2015/beratungsvorgaenge-node.html"]
#
#
# # ***************************************** #
# driver = webdriver.Firefox()
# wait = UI.WebDriverWait(driver, 5000)
#
# # Start with just one website for developing the script:
# driver.get("http://www.bundesrat.de/DE/dokumente/beratungsvorgaenge/2015/beratungsvorgaenge-node.html")
#
#
# tops = driver.find_elements_by_xpath("//li[contains(@class, 'top-item type-')]")
#
# # top = tops[2] # for development
# # top = driver.find_element_by_xpath("//li[contains(@id, 'top-644/15')]") # for development
# # top = driver.find_element_by_xpath("//li[contains(@id, 'top-643/15')]") # for development
# # top = driver.find_element_by_xpath("//li[contains(@id, 'top-640/15')]") # for development
#
#
# for top in tops:
#     item = {}
#     top_nr = (top.find_element_by_xpath(".//h2[@class='top-number']")).text
#     print(top_nr)
#     item['id'] = top_nr
#
#     details = top.find_element_by_xpath(".//div[@class='top-item-switcher']/a")
#
#     details.send_keys("\n")
#     #  this works for 644/15, 643/15, 640/15
#     # see http://stackoverflow.com/questions/8832858/using-python-bindings-selenium-webdriver-click-is-not-working-sometimes
#
#     time.sleep(2) # I need to wait until the new content has appeared!!!
#
#
#     # date = wait.until((top.find_elements_by_xpath(".//div[@class='zusatztitel']/following-sibling::p"))[0].text)
#     # item['date'] = date
#     #
#     # year = date.split(".")[-1]
#     # item['year'] = year
#
#     # If there are details on the committees involved, get those details:
#     try:
#         committees = (top.find_element_by_xpath(".//h3[contains(text(), 'Ausschusszuweisung')]/following-sibling::p")).text
#
#         item['committees'] = committees
#
#         com_list = committees.replace(" (fdf)", "").split(" - ")
#
#         # add a function for coding "(fdf)" ("federführend") later!!
#
#         com_list2 = ['AV', 'AIS', 'AA', 'EU', 'Fz', 'FJ', 'G', 'In',
#                       'K', 'R', 'Wo', 'U', 'Vk', 'V', 'Wi', 'other']
#
#         for com in com_list2:
#             print(com)
#             item[com] = (1 if com in com_list else 0)
#
#
#     except: # if no details on the "Ausschusszuweisung" given:
#         pass
#
#
#
#     print(item)
#
#
#
#
# # Close the driver:
# driver.close()
#
#
