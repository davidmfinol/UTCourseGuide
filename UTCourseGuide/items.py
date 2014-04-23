# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class UtcourseguideItem(Item):

    # Course Survey Meta-data
    instructor = Field()
    course = Field()
    organization = Field()
    college = Field()
    semester = Field()
    formsDistributed = Field()
    formsReturned = Field()
    
    # The course was well organized.
    wellOrganized = Field()
    
    # The instructor communicated information effectively.
    commmunicatedEffectively = Field()
    
    # The instructor showed interest in the progress of students.
    showedInterest = Field()
    
    # The tests/assignments were usually graded and returned promptly.
    gradedPromptly = Field()
    
    # The instructor made me feel free to ask questions, disagree, and express my ideas.
    freeToDisagree = Field()
    
    # At this point in time, I feel that this course will be (or has already been) of value to me.
    courseOfValue = Field()
    
    # Overall, this instructor was
    instructorWas = Field()
    
    # Overall, this course was
    courseWas = Field()
    
    # In my opinion, the workload in this course was
    workloadWas = Field()
    
    pass
