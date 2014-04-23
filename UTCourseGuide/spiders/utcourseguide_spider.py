from scrapy.spider import Spider
from scrapy.http import FormRequest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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
    xpaths = {
        'LOGON' : ".//*[@id='eid']",
        'PASSWORDS' : ".//*[@id='pw']",
        'submit' :   "html/body/div[1]/table[1]/tbody/tr/td[1]/table/tbody/tr[5]/td[2]/input"
    }
    
    
    # Initialize scrapy and selenium
    def  __init__(self, username=None, password=None, *args, **kwargs):
        super(UtcourseguideSpider, self).__init__(*args, **kwargs)
        self.username = username;
        self.password = password;
        self.browser = webdriver.Firefox()
    
    
    # Scrapy calls this on all the start-urls
    def parse(self, response):
    
        # login with Selenium
        self.browser.get(response.url)
        self.browser.find_element_by_xpath(self.xpaths['LOGON']).clear()
        self.browser.find_element_by_xpath(self.xpaths['LOGON']).send_keys(self.username)
        self.browser.find_element_by_xpath(self.xpaths['PASSWORDS']).clear()
        self.browser.find_element_by_xpath(self.xpaths['PASSWORDS']).send_keys(self.password)
        self.browser.find_element_by_xpath(self.xpaths['submit']).click()
        
        # Click the alert message that pops-up when you log-in
        WebDriverWait(self.browser, 3).until(EC.alert_is_present(),
                                   'Timed out waiting for PA creation ' +
                                   'confirmation popup to appear.')
        alert = self.browser.switch_to_alert()
        alert.accept()
        
        # Actually parse the page 
        time.sleep(5)
        hxs = HtmlXPathSelector(self.browser.page_source)
        print(self.browser.page_source)
        
        