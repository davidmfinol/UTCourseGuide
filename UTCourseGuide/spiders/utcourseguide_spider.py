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
        'courseSurveyMeta' : ".//*[@id='service_content']/fieldset/div"
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
        
        # Use scrapy to get the course survey meta-data
        item = UtcourseguideItem()
        courseSurveyMeta = selector.xpath(self.field_xpaths['courseSurveyMeta'])
        item['instructor'] = courseSurveyMeta[0].extract()
        item['course'] = courseSurveyMeta[0].extract()
        item['organization'] = courseSurveyMeta[0].extract()
        item['college'] = courseSurveyMeta[0].extract()
        
        # Clean-up
        self.browser.close()
        
        