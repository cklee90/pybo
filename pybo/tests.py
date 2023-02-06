import logging
import unittest
import datetime
import requests
import pyperclip  # 클립보드를 쉽겍 활용할수 있게 해주는 모듈
from bs4 import BeautifulSoup
from urllib.request import urlopen

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys     # 컨트롤 c 컨트롤 v



import time
from selenium.webdriver import *


from django.test import TestCase

# Create your tests here.
class Crawling(unittest.TestCase):
    def setUp(self):
        #webdriver Firefox 객체 생성
        self.browser = webdriver.Firefox(executable_path='/Users/ckair/Desktop/Dev/big_ai0102/01_python_basic/app/geckodriver')
        logging.info('setUp')

    def tearDown(self):
        logging.info('tearDown')
        #self.browser.quit()    # webdriver 종료


    @unittest.skip
    def test_selenium(self):    # Selenium 사용
        #Firefox 웹 드라이버 객체에게 Get을 통하여 네이버의 http 요청을 하게 함
        self.browser.get('http://127.0.0.1:8000/pybo/5')
        print('self.browser.title:{}'.format(self.browser.title))
        self.assertIn('Pybo',self.browser.title)

        content_textarea = self.browser.find_element(By.ID,'content')
        content_textarea.send_keys('안녕하세요. 셀레니움 테스트입니다. ')
        content_button = self.browser.find_element(By.ID, 'answer_reg')
        content_button.click()  # 버튼 클릭

    def test_clipboard_naver(self):
        '''clipboard 를 통한 naver login'''
        self.browser.get('http://nid.naver.com/nidlogin.login?mode=form&url=https%3A%2F%2Fwww.naver.com')
        user_id = 'mushu444'
        user_pw = 'Fkdtns23!@#'

        #id
        id_textinput = self.browser.find_element(By.ID,'id')
        id_textinput.click()
        #클립보드로 copy
        pyperclip.copy(user_id)
        id_textinput.send_keys(Keys.COMMAND,'v')  # 클립보드에서 id_textinput 으로 copy
        time.sleep(1)

        #password
        pw_textinput = self.browser.find_element(By.ID,'pw')
        pw_textinput.click()
        pyperclip.copy(user_pw)
        pw_textinput.send_keys(Keys.COMMAND,'v')
        time.sleep(1)

        #로그인버튼
        btn_login = self.browser.find_element(By.ID,'log.login')
        btn_login.click()


    @unittest.skip
    def test_loginNaver(self):    # Selenium 사용
        self.browser.get('http://nid.naver.com/nidlogin.login?mode=form&url=https%3A%2F%2Fwww.naver.com')
        user_id = 'mushu444'
        user_pw = 'Fkdtns23!@#'
        content_id = self.browser.find_element(By.ID,'id')
        content_id.click()
        time.sleep(3)
        pyperclip.copy(user_id)
        pyperclip.paste()
        content_pw = self.browser.find_element(By.ID,'pw')
        content_pw.click()
        time.sleep(3)
        pyperclip.copy(user_id)
        pyperclip.paste()
        content_button = self.browser.find_element(By.ID,'log.login')
        content_button.click()



    @unittest.skip
    def test_zip(self):
        ''' 여러개의 list를 묶어서 하나의 iteration 객체로 다룰수 있게 한다.'''
        integers = [1,2,3]
        letters = ['a','b','c']
        floats = [4.0, 8.0, 10.0]
        zipped = zip(integers, letters, floats)
        list_data = list(zipped)
        print(('list_data:{}'.format(list_data)))
        print(list_data[1][1])

    @unittest.skip
    def test_naver_stock(self):
        '''주식 크롤링'''
        #https://finance.naver.com/item/main.naver?code=005930
        codes = {'삼성전자':'005930','현대차':'005380'}
        for code in codes.keys():
            url = 'https://finance.naver.com/item/main.naver?code='
            url = url+str(codes[code])
            response = requests.get(url)
            if 200 == response.status_code:
                html = response.text
                soup = BeautifulSoup(html, 'html.parser')
                price = soup.select_one('#chart_area div.rate_info div.today span.blind')
                print('today:{}, {}, {}'.format(code,codes[code],price.getText()))
            else:
                print('접속오류')


    @unittest.skip
    def test_slamdunk(self):
        '''https://movie.naver.com/movie/point/af/list.naver?st=mcode&sword=223800&page=1'''
        url = 'https://movie.naver.com/movie/point/af/list.naver?st=mcode&sword=223800&page='
        for i in range(1,4,1):
            self.call_slamdunk(url+str(i))



    @unittest.skip
    def call_slamdunk(self,url):
        response = requests.get(url)
        if 200 == response.status_code:
            html = response.text
            soup = BeautifulSoup(html,'html.parser')
            #평점
            score = soup.select('div.list_netizen_score em')
            #댓글
            review = soup.select('table tbody tr td.title')
            for i in range(0, len(score)):
                review_text = review[i].getText().split('\n')
                if len(review_text)>2:    # 평점만 넣고 감상평 없는 경우 처리
                    tmp_text = review_text[5]
                else:
                    tmp_text = review_text[0]
                print('평점, 감상평:{} ,{}:'.format(score[i].getText(),tmp_text))
        else:
            print('url 확인하세요.')
            pass



    @unittest.skip
    def test_cgv(self):
        '''CGV http://www.cgv.co.kr/movies/?lt=1&ft=0'''
        url = 'http://www.cgv.co.kr/movies/?lt=1&ft=0'
        response = requests.get(url)
        if 200== response.status_code:
            html = response.text
            #print('html:{}'.format(html))
            #box-contents
            soup = BeautifulSoup(html,'html.parser')
            #제목
            title = soup.select('div.box-contents strong.title')
            reserv = soup.select('strong.percent span')
            poster = soup.select('span.thumb-image img')
            #print('title:{}'.format(title))
            for page in range(0,7,1):
                posterImg = poster[page]
                imgUrlPath = posterImg.get('src')  # <img src='' /> 에 접근
                # print('poster[page]:{}'.format(imgUrlPath))
                print('제목 : {}, {}, {}'.format(title[page].getText()
                                     ,reserv[page].getText()
                                     ,imgUrlPath
                                           ))




        else:
            print('response.status_code:{}'.format(response.status_code))

    @unittest.skip('테스트 연습')
    def test_weather(self):
        '''날씨'''
        logging.info('test_weather')
        now = datetime.datetime.now()
        #yyyymmdd hh:mm
        nowDate = now.strftime('%Y-%m-%d, %H:%M:%S')
        print('nowDate:{}'.format(nowDate))

        #------------------------------------------------------
        naverWeatherUrl = 'https://weather.naver.com/today/09545101'
        html = urlopen(naverWeatherUrl)

        bsObject = BeautifulSoup(html, 'html.parser')
        tmpes = bsObject.find('strong','current')
        print('현재 금천구 가산동 날씨:{}'.format(tmpes.getText()))