import logging
import unittest
import datetime
import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen


from django.test import TestCase

# Create your tests here.
class Crawling(unittest.TestCase):
    def setUp(self):
        logging.info('setUp')

    def tearDown(self):
        logging.info('tearDown')

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