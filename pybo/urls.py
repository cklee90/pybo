'''
파일명 : urls.py
설명 : pybo 의 모든 url 과 view 함수의 mapping 을 담당
생성일 : 2023/01/25
생성자 : ckair
'''

from django.urls import path
from . import views  # 현재 디렉토리의 views 모듈을 가져옴

app_name = 'pybo'

urlpatterns = [
    #base_view
    path('',views.index, name='index'), # views index 함수로 매핑
    path('<int:question_id>/', views.detail, name='detail'),

    #answer
    path('answer/create/<int:question_id>/', views.answer_create, name='answer_create'),
    path('answer/modify/<int:answer_id>/', views.answer_modify, name='answer_modify'),
    path('answer/delete/<int:answer_id>/', views.answer_delete, name='answer_delete'),

    #question
    path('question/create/', views.question_create, name='question_create'),
    path('question/modify/<int:question_id>/', views.question_modify, name='question_modify'),
    path('question/delete/<int:question_id>/', views.question_delete, name='question_delete'),


    #boot
    path('boot/menu',views.boot_menu, name='boot_menu'),
    path('boot/list/',views.boot_list, name='boot_list'),
    path('boot/reg/',views.boot_reg, name='boot_reg'),
    #crawling
    path('crawling/cgv/',views.crawling_cgv, name='crawling_cgv'),
]
