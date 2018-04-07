from __future__ import unicode_literals
import scrapy
import json
import os
from scrapy.spiders import Spider
from scrapy.http import FormRequest
from scrapy.http import Request
from data.items import DataItem
from lxml import etree
from selenium import webdriver
from lxml import html
import time
import datetime
import random
import pdb


class DataspiderSpider(scrapy.Spider):
    name = 'dataspider'
    allowed_domains = ['data.com']
    start_urls = ['https://ttdsevaonline.chromedriver']

    def __init__(self):
        self.driver = webdriver.Chrome("./chromedriver")
        self.driver.set_window_size(1850, 1000)
        with open('input.txt', 'r') as data_file:
            self.input_list = json.load(data_file)
        script_dir = os.path.dirname(__file__)

    def start_requests(self):
        init_url = 'http://python.org'
        yield scrapy.Request(url=init_url, callback=self.body)

    def body(self, response):
        for item in self.input_list:
            username = item['email']
            password = item['password']
            today_date = item['date']
            number_of_user = str(len(item['people']))
            number_of_additional_laddus = str(int(number_of_user) * 2)

            self.driver.get("https://ttdsevaonline.com/#/login")
            time.sleep(3)
            self.driver.find_element_by_xpath('//input[contains(@class, "u_name")]').send_keys(username)
            self.driver.find_element_by_xpath('//input[contains(@class, "u_pass")]').send_keys(password)
            self.driver.find_element_by_xpath("//button[@id='login_sub']").click()

            time.sleep(5)
            self.driver.find_element_by_xpath('//div[@class="menu"]//span[@class="Services"]').click()
            time.sleep(5)
            self.driver.find_element_by_xpath('//ul[@class="nav"]//li//a[contains(@class, "eSpecial")]').click()
            time.sleep(5)
            source = self.driver.page_source.encode("utf8")
            tree = etree.HTML(source)

            current_span = tree.xpath('//span[contains(@class, "' + today_date + '")]')

            status = ''

            if len(current_span) == 0:
                print('no such date')
                break
            else:
                status = current_span[0].xpath('./@class')[0]

                if 'booked' in status:
                    print('already booked')
                    break
                elif 'prevDay' in status or 'quotaNotReleased' in status:
                    print ('Not available')
                    break
                else:
                    _path = etree.ElementTree(tree).getpath(current_span[0])
                    self.driver.find_element_by_xpath(_path).click()
                    time.sleep(6)
                    
                    self.driver.find_element_by_xpath('(//div[@class="cal_inrcnt"])[1]').click()

                    # click number of people
                    self.driver.find_element_by_xpath('//select[@id="person"]').click()
                    time.sleep(1)
                    source = self.driver.page_source.encode("utf8")
                    tree = etree.HTML(source)

                    option_list = tree.xpath('//select[@id="person"]//option')

                    for option in option_list:
                        opt_number = option.xpath('./text()')[0]
                        if opt_number == number_of_user:
                            _path = etree.ElementTree(tree).getpath(option)
                            self.driver.find_element_by_xpath(_path).click()
                            break

                    self.driver.find_element_by_xpath('//select[@id="person"]').click()
                    time.sleep(1)
                    source = self.driver.page_source.encode("utf8")
                    tree = etree.HTML(source)
                    additional_laddus_list = tree.xpath('//select[@id="addladdus"]//option')

                    for option in additional_laddus_list:
                        opt_number = option.xpath('./text()')[0]
                        if opt_number == number_of_additional_laddus:
                            _path = etree.ElementTree(tree).getpath(option)
                            self.driver.find_element_by_xpath(_path).click()
                            break

                    self.driver.find_element_by_xpath('//input[@id="booking_others"]').click()
                    self.driver.find_element_by_xpath('//button[@id="sedavailability_contiune"]').click()
                    time.sleep(8)
                    
                    source = self.driver.page_source.encode("utf8")
                    tree = etree.HTML(source)
                    form_list = tree.xpath('//form[contains(@id, "othersForm")]')

                    num = 0
                    for form in form_list:
                        # name input
                        selector = 'fName' + str(num)
                        name_element = tree.xpath('//input[contains(@name, "' + selector + '")]')[0]
                        _path = etree.ElementTree(tree).getpath(name_element)
                        self.driver.find_element_by_xpath(_path).send_keys(item['people'][num]['name'])
                        # age input
                        selector = 'age' + str(num)
                        age_element = tree.xpath('//input[contains(@name, "' + selector + '")]')[0]
                        _path = etree.ElementTree(tree).getpath(age_element)
                        self.driver.find_element_by_xpath(_path).send_keys(item['people'][num]['age'])
                        
                        # select gender
                        selector = 'gender' + str(num)
                        self.driver.find_element_by_xpath('//select[contains(@name, "' + selector + '")]').click()
                        time.sleep(1)
                        option_list = tree.xpath('//select[contains(@name, "' + selector + '")]//option')

                        for option in option_list:
                            gender = option.xpath('./text()')[0]
                            if item['people'][num]['gender'] in gender:
                                _path = etree.ElementTree(tree).getpath(option)
                                self.driver.find_element_by_xpath(_path).click()
                                break

                        # select id category
                        selector = 'proofS' + str(num)
                        self.driver.find_element_by_xpath('//select[contains(@name, "' + selector + '")]').click()
                        time.sleep(1)
                        source = self.driver.page_source.encode("utf8")
                        tree = etree.HTML(source)
                        option_list = tree.xpath('//select[contains(@name, "' + selector + '")]//option')

                        for option in option_list:
                            gender = option.xpath('./text()')[0]
                            if item['people'][num]['id'] in gender:
                                _path = etree.ElementTree(tree).getpath(option)
                                self.driver.find_element_by_xpath(_path).click()
                                break

                        num = num + 1

                    
                    num = 0
                    for form in form_list:
                        #proofID input proofId0
                        selector = 'proofId' + str(num)
                        id_number_element = tree.xpath('//input[@id="' + selector + '"]')[0]
                        _path = etree.ElementTree(tree).getpath(id_number_element)
                        self.driver.find_element_by_xpath(_path).send_keys(item['people'][num]['id_number'])
                        num = num + 1

                    pdb.set_trace()
                    self.driver.find_element_by_xpath('//button[@id="sedpiligrim_continue"]').click()
                    time.sleep(5)
                    if 'https://ttdsevaonline.com/#/sedPiligrim' is self.driver.current_url:
                        print ('Error in continue')
                    else:
                        pass