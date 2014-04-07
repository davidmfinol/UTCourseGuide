from scrapy.spider import Spider
from scrapy.http import FormRequest

class UtcourseguideSpider(Spider):
    name = "utcourseguide"
    allowed_domains = ["utdirect.utexas.edu"]
    start_urls = [
        "https://utdirect.utexas.edu/", # login first
        "https://utdirect.utexas.edu/ctl/ecis/results/index.WBX", # probably don't need this page
    #	"https://utdirect.utexas.edu/ctl/ecis/results/search.WBX", # do searches from here
    #   "https://utdirect.utexas.edu/ctl/ecis/results/view_results.WBX?s_me_cis_id=2005935720000001"
    ]
    
    username = ""
    password = ""
    
    def  __init__(self, username=None, password=None, *args, **kwargs):
        super(UtcourseguideSpider, self).__init__(*args, **kwargs)
        self.username = username;
        self.password = password;
    
    def parse(self, response):
        return [FormRequest.from_response(response,
                    formdata={'LOGON': self.username, 'PASSWORDS': self.password},
                    callback=self.after_login)]
    
    def after_login(self, response):
        print(response.body)
        