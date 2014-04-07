from scrapy.spider import Spider

class UtcourseguideSpider(Spider):
    name = "utcourseguide"
    allowed_domains = ["utdirect.utexas.edu"]
    start_urls = [
        "https://utdirect.utexas.edu/ctl/ecis/results/index.WBX",
    #	"https://utdirect.utexas.edu/ctl/ecis/results/search.WBX",
    #   "https://utdirect.utexas.edu/ctl/ecis/results/view_results.WBX?s_me_cis_id=2005935720000001"
    ]
    
    def parse(self, response):
        print(response.body)
        #filename = response.url.split("/")[-1]
        #open(filename, 'wb').write(response.body)