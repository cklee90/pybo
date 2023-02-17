'''
파일명 : urls.py
설명 : pybo 의 모든 url 과 view 함수의 mapping 을 담당
생성일 : 2023/01/25
생성자 : ckair
'''

from django.urls import path
from board.views import base_views, board_views


app_name = 'board'

urlpatterns = [
    #base_view
    path('',base_views.index, name='index'), # views index 함수로 매핑
    path('<int:question_id>/', base_views.detail, name='detail'),

    #board
    path('board/create/', board_views.board_create, name='board_create'),
    path('board/modify/<int:board_id>/', board_views.board_modify, name='board_modify'),
    path('board/delete/<int:board_id>/', board_views.board_delete, name='board_delete'),

]
