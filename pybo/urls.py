'''
파일명 : urls.py
설명 : pybo 의 모든 url 과 view 함수의 mapping 을 담당
생성일 : 2023/01/25
생성자 : ckair
'''

from django.urls import path
from .views import base_views, question_views, answer_views, boot_views, board_views


app_name = 'pybo'

urlpatterns = [
    #base_view
    path('',base_views.index, name='index'), # views index 함수로 매핑
    path('<int:question_id>/', base_views.detail, name='detail'),

    #answer
    path('answer/create/<int:question_id>/', answer_views.answer_create, name='answer_create'),
    path('answer/modify/<int:answer_id>/', answer_views.answer_modify, name='answer_modify'),
    path('answer/delete/<int:answer_id>/', answer_views.answer_delete, name='answer_delete'),
    path('answer/vote/<int:answer_id>/', answer_views.answer_vote, name='answer_vote'),

    #question
    path('question/create/', question_views.question_create, name='question_create'),
    path('question/modify/<int:question_id>/', question_views.question_modify, name='question_modify'),
    path('question/delete/<int:question_id>/', question_views.question_delete, name='question_delete'),
    path('question/vote/<int:question_id>/', question_views.question_vote, name='question_vote'),

    #boot
    path('boot/menu',boot_views.boot_menu, name='boot_menu'),
    path('boot/list/',boot_views.boot_list, name='boot_list'),
    path('boot/reg/',boot_views.boot_reg, name='boot_reg'),
    #crawling
    path('crawling/cgv/',boot_views.crawling_cgv, name='crawling_cgv'),

    #board
    path('board/list/',board_views.board_list, name='board_list'),
    path('board/list/<int:board_id>/', board_views.board_detail, name='board_detail'),
    path('board/create/', board_views.board_create, name='board_create'),
    path('board/modify/<int:board_id>/', board_views.board_modify, name='board_modify'),
    path('board/delete/<int:board_id>/', board_views.board_delete, name='board_delete'),

]
