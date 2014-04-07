# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class UtcourseguideItem(Item):
    instructor = Field()
    course = Field()
    organization = Field()
    college = Field()
    semester = Field()
    formsDistributed = Field()
    formsReturned = Field()
    pass
