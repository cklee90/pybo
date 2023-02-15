'''
파일명 : board_views.py
설명 : 
생성일 : 2023/02/15
생성자 : ckair
'''

import logging

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from ..forms import BoardForm
from ..models import Board


# 큰트롤 알트 o  ; 임포트 정리

def board_detail(request, board_id):
    '''board 상세'''
    logging.info('1. board_id:{}'.format(board_id))
    # question = Question.objects.get(id=question_id)
    board = get_object_or_404(Board, pk=board_id)
    logging.info('2. board:{}'.format(board))
    context = {'board': board}
    return render(request, 'pybo/board_detail.html', context)


def board_list(request):
    '''board 목록'''

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
    print('boardList:{}'.format(board_list))
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


    # question_list = Question.objects.filter(id=99)   # 없을때 잘 되는지 확인
    context = {'board_list': page_obj, 'kw': kw, 'page': page, 'div': div, 'size': size}
    logging.info('board_list:{}'.format(page_obj))
    return render(request, 'pybo/board_list.html', context)


@login_required(login_url='common:login')
def board_delete(request, board_id):
    ''' 질문 삭제 '''
    logging.info('1. board_delete')
    logging.info('2. board_id:{}'.format(board_id))
    board = get_object_or_404(Board, pk=board_id)  # question_id 로 question 데이터 조회
    if request.user != board.author:
        messages.error(request, '삭제 권한이 없습니다.')
        return redirect('pybo:board_detail', board_id=board.id)

    board.delete()  # 삭제
    return redirect('pybo:board_list')


@login_required(login_url='common:login')
def board_modify(request, board_id):
    '''질문 수정'''
    logging.info('1. board_modify')
    board = get_object_or_404(Board, pk=board_id)  # question_id 로 question 데이터 조회
    # 권한 체크
    if request.user != board.author:
        messages.error(request, '수정 권한이 없습니다.')
        return redirect('pybo:board_detail', board_id=board.id)

    if request.method == 'POST':
        logging.info('2. board modify post')
        form = BoardForm(request.POST, instance=board)

        if form.is_valid():
            logging.info('3. form is valid():{}'.format(form.is_valid()))
            board = form.save(commit=False)  # 질문 내용,
            board.modify_date = timezone.now()  # 수정일시 저장
            board.save()  # 수정날짜 까지 생성해서 저장 ( commit)
            return redirect("pybo:board_detail", board_id=board.id)
    else:
        form = BoardForm(instance=board)
    context = {'form': form}
    return render(request, 'pybo/board_form.html', context)


@login_required(login_url='common:login')  # 로그인이 되어있지 않으면 login 페이지로 이동시킴
def board_create(request):
    '''질문 등록'''
    logging.info('1. request.method:{}'.format(request.method))
    if request.method == 'POST':
        logging.info('2. board_create post')
        # 저장
        form = BoardForm(request.POST)  # request.post 로 표시를 해줘야함.(subject, content 자동 생성)
        logging.info('3. board_create post')
        logging.info('4. form is valid():{}'.format(form.is_valid()))
        if form.is_valid():  # form(질문등록) 이 유효하면
            logging.info('4. form is valid():{}'.format(form.is_valid()))
            board = form.save(commit=False)  # subject, content 만 저장(확정commit은 하지 않음)
            board.create_date = timezone.now()
            board.author = request.user  # author 속성에 로그인 계정 저장

            logging.info('4. board.author:{}'.format(board.author))

            board.save()  # 날짜 까지 생성해서 저장 ( commit)
            return redirect('pybo:board_list')
    else:
        form = BoardForm()
    context = {'form': form}
    return render(request, 'pybo/board_form.html', context)
