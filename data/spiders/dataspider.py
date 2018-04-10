from __future__ import unicode_literals
import scrapy
import json
import os, sys
from scrapy.spiders import Spider
from scrapy.http import FormRequest
from scrapy.http import Request
from data.items import DataItem
from lxml import etree
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from lxml import html
import time
import datetime
import random
import Tkinter as tk
import tkMessageBox
import pdb


class DataspiderSpider(scrapy.Spider):
    name = 'dataspider'
    allowed_domains = ['https://ttdsevaonline.com']
    start_urls = ['https://ttdsevaonline.com']

    def __init__(self):
        _chrome_options = Options()
        _chrome_options.add_argument('disable-infobars')
        self.driver = webdriver.Chrome(executable_path="./chromedriver", chrome_options=_chrome_options)
        self.driver.set_window_size(1850, 1000)
        filename = 'input.txt'
        with open(filename, 'r') as data_file:
            self.input_list = json.load(data_file)

    def start_requests(self):
        init_url = 'http://python.org'
        yield scrapy.Request(url=init_url, callback=self.body)

    def body(self, response):
        root = tk.Tk()
        root.withdraw()
        print('AAAAAAAAA------------------------------------------')
        for item in self.input_list:
            username = item['email']
            password = item['password']
            today_date = item['date']
            number_of_user = str(len(item['people']))
            number_of_additional_laddus = str(int(number_of_user) * 2)

            self.driver.get("https://ttdsevaonline.com/#/login")
            try:
                ele = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.ID, 'login_sub')))

                self.driver.find_element_by_xpath('//input[contains(@class, "u_name")]').send_keys(username)
                self.driver.find_element_by_xpath('//input[contains(@class, "u_pass")]').send_keys(password)
                ele.click()

                ele = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//div[@class="menu"]//span[@class="Services"]')))
                ele.click()

                ele = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//ul[@class="nav"]//li//a[contains(@class, "eSpecial")]')))
                ele.click()

                str1 = '//span[contains(@class, "' + today_date + '")]'
                ele = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, str1)))
                source = self.driver.page_source.encode("utf8")
                tree = etree.HTML(source)

                current_span = tree.xpath('//span[contains(@class, "' + today_date + '")]')
                status = ''

                if len(current_span) == 0:
                    tkMessageBox.showwarning('Title','Date is invalid')
                    break
                else:
                    statusVal = current_span[0].xpath('./@class')[0]
                    status = self.check_status(statusVal);

                    if status is False:
                        tkMessageBox.showwarning('Title','Not available to book')
                        time.sleep(1)
                        self.redo(item, 'https://ttdsevaonline.com/#/sedAvailability')
                    else:
                        _path = etree.ElementTree(tree).getpath(current_span[0])
                        try:
                            self.driver.find_element_by_xpath(_path).click()
                        except:
                            print _path

                        ele = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '(//div[@class="cal_inrcnt"])[1]')))
                        ele.click()

                        # click number of people
                        ele = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//select[@id="person"]')))
                        ele.click()

                        source = self.driver.page_source.encode("utf8")
                        tree = etree.HTML(source)

                        option_list = tree.xpath('//select[@id="person"]//option')

                        for option in option_list:
                            opt_number = option.xpath('./text()')[0]
                            if opt_number == number_of_user:
                                _path = etree.ElementTree(tree).getpath(option)
                                self.driver.find_element_by_xpath(_path).click()
                                break

                        ele = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//select[@id="person"]')))
                        ele.click()
                        ele = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//select[@id="addladdus"]//option')))
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
                        
                        ele = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//form[contains(@id, "othersForm")]')))
                        source = self.driver.page_source.encode("utf8")
                        tree = etree.HTML(source)
                        form_list = tree.xpath('//form[contains(@id, "othersForm")]')

                        num = 0
                        print form_list

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
                            try:
                                ele = WebDriverWait(self.driver, 4).until(EC.visibility_of_element_located((By.XPATH, '//select[contains(@name, "' + selector + '")]')))
                                ele.click()
                            except:
                                time.sleep(1)
                                self.driver.find_element_by_xpath('//select[contains(@name, "' + selector + '")]').click()
                            # ele.click()
                            option_list = tree.xpath('//select[contains(@name, "' + selector + '")]//option')

                            for option in option_list:
                                try:
                                    gender = option.xpath('./text()')[0]
                                    if item['people'][num]['gender'] in gender:
                                        _path = etree.ElementTree(tree).getpath(option)
                                        self.driver.find_element_by_xpath(_path).click()
                                        break
                                except:
                                    pass
                                

                            # select id category
                            selector = 'proofS' + str(num)
                            try:
                                ele = WebDriverWait(self.driver, 4).until(EC.visibility_of_element_located((By.XPATH, '//select[contains(@name, "' + selector + '")]')))
                                ele.click()
                            except:
                                time.sleep(1)
                                self.driver.find_element_by_xpath('//select[contains(@name, "' + selector + '")]').click()
                            # ele.click()
      
                            source = self.driver.page_source.encode("utf8")
                            tree = etree.HTML(source)
                            option_list = tree.xpath('//select[contains(@name, "' + selector + '")]//option')

                            for option in option_list:
                                try:
                                    gender = option.xpath('./text()')[0]
                                    if item['people'][num]['id'] in gender:
                                        _path = etree.ElementTree(tree).getpath(option)
                                        self.driver.find_element_by_xpath(_path).click()
                                        break
                                except:
                                    pass

                            num = num + 1

                        
                        num = 0
                        for form in form_list:
                            #proofID input proofId0
                            selector = 'proofId' + str(num)
                            id_number_element = tree.xpath('//input[@id="' + selector + '"]')[0]
                            _path = etree.ElementTree(tree).getpath(id_number_element)
                            self.driver.find_element_by_xpath(_path).send_keys(item['people'][num]['id_number'])
                            num = num + 1

                        # check
                        is_error = False
                        try:
                            ele = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//button[@id="sedpiligrim_continue"')))
                            ele.click()

                            ele = WebDriverWait(self.driver, 3).until(EC.visibility_of_element_located((By.XPATH, '//button[@id="sedpay_paynow"')))
                            is_error = self.check_error(self.dirver.current_url)
                        except:
                            pass

                        if is_error is False:
                            tkMessageBox.showwarning('Title','INPUT ERROR')                        
                            time.sleep(10000)
                        else:
                            tkMessageBox.showinfo('Title','Success')
                            time.sleep(10000)
            except:
                self.redo(item, 'https://ttdsevaonline.com/#/sedAvailability')

    def check_status(self, status):
        returnVal = True
        for item in ['booked', 'prevDay', 'quotaNotReleased']:
            if item in status:
                returnVal = False
        
        return returnVal

    def check_error(self, status):
        if 'https://ttdsevaonline.com/#/sedPay' not in 'status':
            return False
        else:
            return True

    def redo(self, item, current_url=None):
        username = item['email']
        password = item['password']
        today_date = item['date']
        number_of_user = str(len(item['people']))
        number_of_additional_laddus = str(int(number_of_user) * 2)

        tmp = "https://ttdsevaonline.com/#/login"
        if current_url:
            tmp = current_url
        self.driver.get(tmp)

        try:
            str1 = '//span[contains(@class, "' + today_date + '")]'
            ele = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, str1)))
            source = self.driver.page_source.encode("utf8")
            tree = etree.HTML(source)

            current_span = tree.xpath('//span[contains(@class, "' + today_date + '")]')
            status = ''

            if len(current_span) == 0:
                tkMessageBox.showwarning('Title','Date is invalid')
                self.redo(item, 'https://ttdsevaonline.com/#/sedAvailability')
            else:
                statusVal = current_span[0].xpath('./@class')[0]
                status = self.check_status(statusVal);

                if status is False:
                    tkMessageBox.showwarning('Title','Not available to book')
                    time.sleep(1)
                    self.redo(item, 'https://ttdsevaonline.com/#/sedAvailability')
                else:
                    _path = etree.ElementTree(tree).getpath(current_span[0])
                    try:
                        self.driver.find_element_by_xpath(_path).click()
                    except:
                        print _path

                    ele = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '(//div[@class="cal_inrcnt"])[1]')))
                    ele.click()

                    # click number of people
                    ele = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//select[@id="person"]')))
                    ele.click()

                    source = self.driver.page_source.encode("utf8")
                    tree = etree.HTML(source)

                    option_list = tree.xpath('//select[@id="person"]//option')

                    for option in option_list:
                        opt_number = option.xpath('./text()')[0]
                        if opt_number == number_of_user:
                            _path = etree.ElementTree(tree).getpath(option)
                            self.driver.find_element_by_xpath(_path).click()
                            break

                    ele = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//select[@id="person"]')))
                    ele.click()
                    ele = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//select[@id="addladdus"]//option')))
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
                    
                    ele = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//form[contains(@id, "othersForm")]')))
                    source = self.driver.page_source.encode("utf8")
                    tree = etree.HTML(source)
                    form_list = tree.xpath('//form[contains(@id, "othersForm")]')

                    num = 0
                    print form_list

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
                        try:
                            ele = WebDriverWait(self.driver, 4).until(EC.visibility_of_element_located((By.XPATH, '//select[contains(@name, "' + selector + '")]')))
                            ele.click()
                        except:
                            time.sleep(1)
                            self.driver.find_element_by_xpath('//select[contains(@name, "' + selector + '")]').click()

                        option_list = tree.xpath('//select[contains(@name, "' + selector + '")]//option')

                        for option in option_list:
                            try:
                                gender = option.xpath('./text()')[0]
                                if item['people'][num]['gender'] in gender:
                                    _path = etree.ElementTree(tree).getpath(option)
                                    self.driver.find_element_by_xpath(_path).click()
                                    break
                            except:
                                pass
                            

                        # select id category
                        selector = 'proofS' + str(num)
                        try:
                            ele = WebDriverWait(self.driver, 4).until(EC.visibility_of_element_located((By.XPATH, '//select[contains(@name, "' + selector + '")]')))
                            ele.click()
                        except:
                            time.sleep(1)
                            self.driver.find_element_by_xpath('//select[contains(@name, "' + selector + '")]').click()
        
                        source = self.driver.page_source.encode("utf8")
                        tree = etree.HTML(source)
                        option_list = tree.xpath('//select[contains(@name, "' + selector + '")]//option')

                        for option in option_list:
                            try:
                                gender = option.xpath('./text()')[0]
                                if item['people'][num]['id'] in gender:
                                    _path = etree.ElementTree(tree).getpath(option)
                                    self.driver.find_element_by_xpath(_path).click()
                                    break
                            except:
                                pass

                        num = num + 1

                    
                    num = 0
                    for form in form_list:
                        #proofID input proofId0
                        selector = 'proofId' + str(num)
                        id_number_element = tree.xpath('//input[@id="' + selector + '"]')[0]
                        _path = etree.ElementTree(tree).getpath(id_number_element)
                        self.driver.find_element_by_xpath(_path).send_keys(item['people'][num]['id_number'])
                        num = num + 1

                    # check
                    is_error = False
                    try:
                        ele = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//button[@id="sedpiligrim_continue"')))
                        ele.click()

                        ele = WebDriverWait(self.driver, 3).until(EC.visibility_of_element_located((By.XPATH, '//button[@id="sedpay_paynow"')))
                        is_error = self.check_error(self.dirver.current_url)
                    except:
                        pass

                    if is_error is False:
                        tkMessageBox.showwarning('Title','INPUT ERROR')                        
                        time.sleep(10000)
                    else:
                        tkMessageBox.showinfo('Title','Success')
                        time.sleep(10000)
        except:
            self.redo(item, 'https://ttdsevaonline.com/#/sedAvailability')



