from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.http import Response 
from scrapy.http import TextResponse 
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from UTCourseGuide.items import UtcourseguideItem

class UtcourseguideSpider(Spider):

    # Settings for Scrapy
    name = "utcourseguide"
    allowed_domains = ["utdirect.utexas.edu"]
    start_urls = [
        #"https://utdirect.utexas.edu/", # will require login
        #"https://utdirect.utexas.edu/ctl/ecis/results/index.WBX", # probably don't need the home-page
    	#"https://utdirect.utexas.edu/ctl/ecis/results/search.WBX", # do searches from here
        "https://utdirect.utexas.edu/ctl/ecis/results/view_results.WBX?s_me_cis_id=2005935720000001" # example page
    ]
    
    # Settings for Selenium
    login_xpaths = {
        'LOGON' : ".//*[@id='eid']",
        'PASSWORDS' : ".//*[@id='pw']",
        'submit' :   "html/body/div[1]/table[1]/tbody/tr/td[1]/table/tbody/tr[5]/td[2]/input"
    }
    
    # Xpaths for the fields that we will be mining with scrapy
    field_xpaths = {
        'courseSurveyMeta' : ".//*[@id='service_content']/fieldset/div",
        'courseSpecific' : ".//*[@id='service_content']/table[1]",
        'courseOverall' : ".//*[@id='service_content']/table[2]",
        'courseWorkload' : ".//*[@id='service_content']/table[3]"
    }
    
    
    # Initialize scrapy and selenium
    def  __init__(self, username, password, *args, **kwargs):
        super(UtcourseguideSpider, self).__init__(*args, **kwargs)
        self.username = username;
        self.password = password;
        self.browser = webdriver.Firefox()
    
    
    # Scrapy calls this on all the start-urls
    def parse(self, response):
    
        # login with selenium
        self.browser.get(response.url)
        self.browser.find_element_by_xpath(self.login_xpaths['LOGON']).clear()
        self.browser.find_element_by_xpath(self.login_xpaths['LOGON']).send_keys(self.username)
        self.browser.find_element_by_xpath(self.login_xpaths['PASSWORDS']).clear()
        self.browser.find_element_by_xpath(self.login_xpaths['PASSWORDS']).send_keys(self.password)
        self.browser.find_element_by_xpath(self.login_xpaths['submit']).click()
        
        # Click the alert message that pops-up when you log-in
        WebDriverWait(self.browser, 3).until(EC.alert_is_present(),
                                   'Timed out waiting for PA creation ' +
                                   'confirmation popup to appear.')
        alert = self.browser.switch_to_alert()
        alert.accept()
        
        # Pass the selenium page to scrapy
        time.sleep(5)
        text_html = self.browser.page_source.encode('utf-8')
        html_str = str(text_html)
        resp_for_scrapy = TextResponse('none', 200, {}, html_str, [], None)
        selector = Selector(resp_for_scrapy)
        
        # Set up scrapy to parse the page
        items = []
        item = UtcourseguideItem()
        courseSurveyMeta = selector.xpath(self.field_xpaths['courseSurveyMeta'])
        courseSpecific = selector.xpath(self.field_xpaths['courseSpecific'])
        courseOverall = selector.xpath(self.field_xpaths['courseOverall'])
        courseWorkload = selector.xpath(self.field_xpaths['courseWorkload'])
        
        # Course survey meta-data
        item['instructor'] = courseSurveyMeta[0].xpath('text()').extract()
        item['course'] = courseSurveyMeta[1].xpath('text()').extract()
        item['organization'] = courseSurveyMeta[2].xpath('text()').extract()
        item['college'] = courseSurveyMeta[3].xpath('text()').extract()
        item['semester'] = courseSurveyMeta[4].xpath('text()').extract()
        item['formsDistributed'] = courseSurveyMeta[5].xpath('text()').extract()
        item['formsReturned'] = courseSurveyMeta[6].xpath('text()').extract()
        
        # The course was well organized.
        wellOrganized = []
        xpath = courseSpecific.xpath('tbody/tr[2]/td')
        for x in range(2, 11):
            wellOrganized.append(xpath[x].xpath('text()').extract())
        item['wellOrganized'] = wellOrganized
        
        # The instructor communicated information effectively.
        commmunicatedEffectively = []
        xpath = courseSpecific.xpath('tbody/tr[3]/td')
        for x in range(2, 11):
            commmunicatedEffectively.append(xpath[x].xpath('text()').extract())
        item['commmunicatedEffectively'] = commmunicatedEffectively
        
        # The instructor showed interest in the progress of students.
        showedInterest = []
        xpath = courseSpecific.xpath('tbody/tr[4]/td')
        for x in range(2, 11):
            showedInterest.append(xpath[x].xpath('text()').extract())
        item['showedInterest'] = showedInterest
        
        # The tests/assignments were usually graded and returned promptly.
        gradedPromptly = []
        xpath = courseSpecific.xpath('tbody/tr[5]/td')
        for x in range(2, 11):
            gradedPromptly.append(xpath[x].xpath('text()').extract())
        item['gradedPromptly'] = gradedPromptly
        
        # The instructor made me feel free to ask questions, disagree, and express my ideas.
        freeToDisagree = []
        xpath = courseSpecific.xpath('tbody/tr[6]/td')
        for x in range(2, 11):
            freeToDisagree.append(xpath[x].xpath('text()').extract())
        item['freeToDisagree'] = freeToDisagree
        
        # At this point in time, I feel that this course will be (or has already been) of value to me.
        courseOfValue = []
        xpath = courseSpecific.xpath('tbody/tr[7]/td')
        for x in range(2, 11):
            courseOfValue.append(xpath[x].xpath('text()').extract())
        item['courseOfValue'] = courseOfValue
        
        # Overall, this instructor was
        instructorWas = []
        xpath = courseOverall.xpath('tbody/tr[2]/td')
        for x in range(2, 11):
            instructorWas.append(xpath[x].xpath('text()').extract())
        item['instructorWas'] = instructorWas
        
        # Overall, this course was
        courseWas = []
        xpath = courseOverall.xpath('tbody/tr[3]/td')
        for x in range(2, 11):
            courseWas.append(xpath[x].xpath('text()').extract())
        item['courseWas'] = courseWas
        
        # In my opinion, the workload in this course was
        workloadWas = []
        xpath = courseWorkload.xpath('tbody/tr[2]/td')
        for x in range(2, 11):
            workloadWas.append(xpath[x].xpath('text()').extract())
        item['workloadWas'] = workloadWas
        
        # Clean-up
        items.append(item)
        self.browser.close()
        return items
        
        