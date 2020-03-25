import scrapy
import os
import re
import json
from pathlib import Path


class CompanyNameSpider(scrapy.Spider):
    name = "Company_Code"
    company_code = {}
    OUT_DIR = '../result'

    def start_requests(self):
        '''
        This method must return an iterable with
        the first Requests to crawl for this spider.
        It is called by Scrapy when the spider is
        opened for scraping. Scrapy calls it only once,
        so it is safe to implement start_requests() as a generator

        :return:
        '''
        start_url = ['https://www.asx.com.au/asx/research/listedCompanies.do']
        for url in start_url:
            request = scrapy.Request(url=url, callback=self.parse)
            yield request

    def find_company_code(self, string):
        '''
        This method will take the will take the html response and
        try to match pattern after applying specific regex

        :param string: Text to match against pattern
        :return: list of matching text
        '''

        pattern = re.compile('company\W(.*)">')
        match = re.findall(pattern=pattern, string=string)
        return match

    def save_json(self, filename, out_dict):
        '''
        This method will take the dictionary & filename as input
        and dump the dict into json format in file having filename

        :param filename: json file name
        :param out_dict: dict to be saved as json
        :return: success message
        '''
        dirname = str(Path(__file__).parent.parent) + '/result'
        print(dirname)
        try:
            with open(os.path.join(dirname, filename), 'w') as fp:
                json.dump(json_str, fp)
                return f"Json dumped in file : {filename}"
        except Exception as e:
            print(f"Exception occured with error\n{e}")

    def parse(self, response):
        '''
        This is the default callback used by
        Scrapy to process downloaded responses, when their requests don’t specify a callback.
        :param response: the response to parse
        '''
        page = response.xpath('//*[@id="content"]').get()
        match = self.find_company_code(page)
        match.remove(match[0])
        company_code = {index: value for index,
                                         value in enumerate(match)}
        self.save_json(filename='company_code.txt',
                       json_str=company_code)
