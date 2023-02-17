'''
파일명 : base_views.py
설명 : 
생성일 : 2023/02/16
생성자 : ckair
'''

import logging

from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404

from ..models import Board


# 큰트롤 알트 o  ; 임포트 정리

def detail(request, board_id):
    '''board 상세'''
    logging.info('1. board_id:{}'.format(board_id))
    # question = Question.objects.get(id=question_id)
    board = get_object_or_404(Board, pk=board_id)
    logging.info('2. question:{}'.format(board))
    context = {'board': board}
    return render(request, 'pybo/question_detail.html', context)


def index(request):
    '''board 목록'''
    # list order create_date desc
    logging.info('index 레벨로 출력')

    # 입력인자

    # http://127.0.0.1:8000/?kw=%ED%8C%8C%EC%9D%B4%EC%8D%AC&page=1
    page = request.GET.get('page', '1')  # 페이지
    kw = request.GET.get('kw', '')  # 키워드
    div = request.GET.get('div', '')
    size = request.GET.get('size', '10')
    logging.info('kw:{}'.format(kw))
    logging.info('page:{}'.format(page))
    logging.info('div:{}'.format(div))
    logging.info('size:{}'.format(size))

    board_list = Board.objects.order_by('-create_date')  # order_by('-필드') 마이너스 표시 붙이면 DESC, 없으면 ASC
    # subject__contains : 사용 __contains 또는 __icontains (대소문자 구분)
    if '10' == div:
        board_list = board_list.filter(subject__contains=kw)
    elif '20' == div:
        board_list = board_list.filter(content__contains=kw)
    elif '30' == div:
        # 포린키 관계 : author__username__contains
        # author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_question')
        board_list = board_list.filter(author__username__contains=kw)

    # paging
    paginator = Paginator(board_list, size)
    page_obj = paginator.get_page(page)
    # paginator.count : 전체 게시물 수
    # paginator.per_page : 페이지당 보여줄 게시물 수
    # paginatior.page_range : 페이지 범위
    # number : 현재 페이지 번호
    # previous_page_number : 이전 페이지 번호
    # next_page_number : 다음 페이지 번호
    # has_previous : 이전 페이지 유무
    # has_next : 다음 페이지 유무
    # start_index : 현재 페이지 시작 인덱스(1부터)
    # end_index : 현재 페이지 끝 인덱스

    # question_list = Question.objects.filter(id=99)   # 없을때 잘 되는지 확인
    context = {'board_list': page_obj, 'kw': kw, 'page': page, 'div': div, 'size': size}
    logging.info('board_list:{}'.format(page_obj))
    return render(request, 'pybo/board.html', context)

