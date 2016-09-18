# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import csv
import codecs

class BundesratPipeline(object):
    def __init__(self):
        self.openTxT()


    def openTxT(self):
        try: # if file already exists:
            with codecs.open('/Users/Annerose/Documents/15-16/Code/bundesrat/data/bundesrat.csv', 'r', encoding='utf-8') as f:
                w= csv.reader(f, delimiter=',')
                self.ids = [x[0] for x in w][1:] # getting id-column (without accessing column name, i.e.
                # the very first row. )


        except: # if file does not yet exist:
            with codecs.open('/Users/Annerose/Documents/15-16/Code/bundesrat/data/bundesrat.csv', 'w+', encoding='utf-8') as f:
                w = csv.writer(f, delimiter=',')
                cols = ['id', 'title', 'date', 'year', 'committees', 'AV',
                                   'AIS', 'AA', 'EU', 'Fz', 'FJ', 'G', 'In', 'K', 'R', 'Wo', 'U',
                                   'Vk', 'V', 'Wi', 'other', 'fdf']
                cols = sorted(cols) # sort the column names alphabetically as this is
                # how the item will be written to the file.
                w.writerow(cols)
                self.ids = [] # empty ids list - no id numbers are yet written to the file.


    def process_item(self, item, spider):

        # Check here whether item already exists in the text file ==
        # prevent duplicates:
        if item['id'] not in self.ids:
            self.toTxt(item)

        return item

    def toTxt(self, item):
        with codecs.open('/Users/Annerose/Documents/15-16/Code/bundesrat/data/bundesrat.csv', 'a+', encoding='utf-8') as f:
            w = csv.writer(f, delimiter=',')
            w.writerow([value for (key, value) in sorted(item.items())]) # items need to be sorted correctly!
