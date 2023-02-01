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
    path('',views.index, name='index'), # views index 함수로 매핑
    path('<int:question_id>/', views.detail, name='detail'),
    path('answer/create/<int:question_id>/', views.answer_create, name='answer_create'),
    path('question/create/', views.question_create, name='question_create'),
    #temp menu
    path('boot/menu',views.boot_menu, name='boot_menu'),
    #bootstrap template
    path('boot/list/',views.boot_list, name='boot_list'),
    path('boot/reg/',views.boot_reg, name='boot_reg'),
]
