# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pandas as pd

class BundesratPipeline(object):
    def __init__(self):
        self.startPandas()

    def startPandas(self):
        committees = ['AV', 'AIS', 'AA', 'EU', 'Fz', 'FJ', 'G', 'In',
                      'K', 'R', 'Wo', 'U', 'Vk', 'V', 'Wi', 'other']

        meetings = ['year', 'id', 'date', 'committees', 'fdf'] + committees

        self.meetings = pd.DataFrame(columns=meetings)  # empty pd dataframe for storing the
        #  meetings ("Beratungsvorgaenge")


    def process_item(self, item, spider):

        meeting = pd.DataFrame([item])
        self.meetings = self.meetings.append(meeting)


    # this is a type of class deconstructor. It gets called automatically once the class
    # is no longer used (i.e. once the spider is closed)
    def __del__(self):
        self.closePipeline()


    def closePipeline(self):
        # Write output to file:
        self.meetings.to_csv('~/Documents/15-16/Code/bundesrat-beratungsvorgaenge/data/bundesrat.txt',
                             header=True, index=None, sep=' ', mode='a')