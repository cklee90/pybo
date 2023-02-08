'''
파일명 : boot_views.py
설명 : 
생성일 : 2023/02/08
생성자 : ckair
'''

import requests
from bs4 import BeautifulSoup
from django.shortcuts import render


#큰트롤 알트 o  ; 임포트 정리

def boot_menu(request):
    '''개발에 사용되는 임시 메뉴'''
    return render(request,'pybo/menu.html')


def boot_reg(request):
    '''bootstrap reg template'''
    return render(request,'pybo/reg.html')

#bootstrap list
def boot_list(request):
    '''bootstrap template'''
    return render(request, 'pybo/list.html')

def crawling_cgv(request):
    '''CGV 무비차트'''
    url = 'http://www.cgv.co.kr/movies/?lt=1&ft=0'
    response = requests.get(url)
    context = {}
    if 200 == response.status_code:
        html = response.text
        # print('html:{}'.format(html))
        # box-contents
        soup = BeautifulSoup(html, 'html.parser')
        # 제목
        title = soup.select('div.box-contents strong.title')
        reserv = soup.select('strong.percent span')
        poster = soup.select('span.thumb-image img')
        # print('title:{}'.format(title))
        title_list = []
        reserv_list = []
        poster_list = []
        for page in range(0, 7, 1):
            posterImg = poster[page]
            imgUrlPath = posterImg.get('src')  # <img src='' /> 에 접근
            # print('poster[page]:{}'.format(imgUrlPath))
            title_list.append(title[page].getText())
            reserv_list.append(reserv[page].getText())
            poster_list.append(imgUrlPath)
            print('제목 : {}, {}, {}'.format(title[page].getText()
                                           , reserv[page].getText()
                                           , imgUrlPath
                                           ))
            pass
        #화면에 타이틀을 [] 로 전달
        context = {'context': zip(title_list,reserv_list,poster_list)}
    else:
        print('response.status_code:{}'.format(response.status_code))

    return render(request,'pybo/crawling_cgv.html',context)

