import logging

import requests
from bs4 import BeautifulSoup
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from .forms import QuestionForm, AnswerForm
from .models import Question, Answer

@login_required(login_url='common:login')
def answer_delete(request, answer_id):
    '''답변 삭제'''
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:
        messages.error(request, '삭제 권한이 없습니다')
    else:
        answer.delete()
    return redirect('pybo:detail',question_id = answer.question.id)

@login_required(login_url='common:login')
def answer_modify(request, answer_id):
    '''답변 수정'''
    logging.info('1. answer_modify:{}'.format(answer_id))
    #1. answer_id 에 해당되는 데이터 조회
    #2. 수정 권한 체크: 권한이 없는 경우 메세지 전달
    #3. POST : 실제 수정
    #3. GET : 수정 form 전달

    #1.
    answer = get_object_or_404(Answer, pk=answer_id)
    #2.
    if request.user != answer.author:
        messages.error(request,'수정 권한이 없습니다.')
        #수정화면 보내기
        return redirect('pybo:detail',question_id=answer.question.id)
    #3.
    if request.method == 'POST':   # 수정
        form = AnswerForm(request.POST, instance=answer)
        logging.info('2. answer_modify POST answer:{}'.format(answer))

        if form.is_valid():
            answer = form.save(commit=False)
            answer.modify_date = timezone.now()
            logging.info('3. answer.form.is_valid:{}'.format(answer))
            answer.save()
            # 수정화면 보내기
            return redirect('pybo:detail', question_id=answer.question.id)

    else:                          # 수정 form 의 template 을 띄워줌
        form = AnswerForm(instance=answer)
    context = {'answer':answer, 'form':form}
    return render(request, 'pybo/answer_form.html', context)


    pass

@login_required(login_url='common:login')
def question_delete(request, question_id):
    ''' 질문 삭제 '''
    logging.info('1. question_delete')
    logging.info('2. question_id:{}'.format(question_id))
    question = get_object_or_404(Question, pk=question_id)  # question_id 로 question 데이터 조회
    if request.user != question.author:
        messages.error(request, '삭제 권한이 없습니다.')
        return redirect('pybo:detail',question_id=question.id)

    question.delete()   # 삭제
    return redirect('pybo:index')


@login_required(login_url='common:login')
def question_modify(request, question_id):
    '''질문 수정'''
    logging.info('1. question_modify')
    question = get_object_or_404(Question, pk=question_id)  # question_id 로 question 데이터 조회
    # 권한 체크
    if request.user != question.author:
        messages.error(request, '수정 권한이 없습니다.')
        return redirect('pybo:detail',question_id = question.id)

    if request.method == 'POST':
        logging.info('2. question_modify post')
        form = QuestionForm(request.POST, instance=question)

        if form.is_valid():
            logging.info('3. form is valid():{}'.format(form.is_valid()))
            question = form.save(commit=False)  # 질문 내용,
            question.modify_date = timezone.now() # 수정일시 저장
            question.save()  #수정날짜 까지 생성해서 저장 ( commit)
            return redirect("pybo:detail", question_id=question.id)
    else:
        form = QuestionForm(instance=question)
    context = {'form':form}
    return render(request, 'pybo/question_form.html', context)

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

@login_required(login_url='common:login')   # 로그인이 되어있지 않으면 login 페이지로 이동시킴
def question_create(request):
    '''질문 등록'''
    logging.info('1. request.method:{}'.format(request.method))
    if request.method == 'POST':
        logging.info('2. question_create post')
        # 저장
        form = QuestionForm(request.POST)   # request.post 로 표시를 해줘야함.(subject, content 자동 생성)
        logging.info('3. question_create post')
        logging.info('4. form is valid():{}'.format(form.is_valid()))
        if form.is_valid():  # form(질문등록) 이 유효하면
            logging.info('4. form is valid():{}'.format(form.is_valid()))
            question = form.save(commit=False)  # subject, content 만 저장(확정commit은 하지 않음)
            question.create_date = timezone.now()
            question.author = request.user # author 속성에 로그인 계정 저장

            logging.info('4. qeustion.author:{}'.format(question.author))

            question.save()  #날짜 까지 생성해서 저장 ( commit)
            return redirect('pybo:index')
    else:
        form = QuestionForm()
    context = {'form': form}
    return render(request,'pybo/question_form.html', context)

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
@login_required(login_url='common:login')
def answer_create(request, question_id):
    '''답변 등록'''
    question = get_object_or_404(Question, pk=question_id)
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        logging.info('1. request.method:{}'.format(request.method))
        if form.is_valid():
            logging.info('2. form.is_valid():{}'.format(form.is_valid()))
            answer = form.save(commit=False)
            answer.create_date = timezone.now()
            answer.question = question
            answer.author = request.user
            logging.info('3. answer.author:{}'.format(answer.author))
            answer.save()
            return redirect('pybo:detail', question_id = question.id)
    else:
        form = AnswerForm()

    # form validation
    context = {'question':question,'form':form}
    return render(request,'pybo/question_detail.html',context)

def detail(request, question_id):
    '''question 상세'''
    logging.info('1. question_id:{}'.format(question_id))
    # question = Question.objects.get(id=question_id)
    question = get_object_or_404(Question, pk=question_id)
    logging.info('2. question:{}'.format(question))
    context = {'question':question}
    return render(request, 'pybo/question_detail.html',context)

def index(request):
    '''question 목록'''
    #list order create_date desc
    logging.info('index 레벨로 출력')

    #입력인자
    page = request.GET.get('page','1') # 페이지
    logging.info('page:{}'.format(page))

    question_list = Question.objects.order_by('-create_date')  # order_by('-필드') 마이너스 표시 붙이면 DESC, 없으면 ASC

    #paging
    paginator = Paginator(question_list,10)
    page_obj = paginator.get_page(page)
    #paginator.count : 전체 게시물 수
    #paginator.per_page : 페이지당 보여줄 게시물 수
    #paginatior.page_range : 페이지 범위
    # number : 현재 페이지 번호
    # previous_page_number : 이전 페이지 번호
    # next_page_number : 다음 페이지 번호
    # has_previous : 이전 페이지 유무
    # has_next : 다음 페이지 유무
    # start_index : 현재 페이지 시작 인덱스(1부터)
    # end_index : 현재 페이지 끝 인덱스


    #question_list = Question.objects.filter(id=99)   # 없을때 잘 되는지 확인
    context = {'question_list':page_obj}
    logging.info('question_list:{}'.format(page_obj))
    return render(request,'pybo/question_list.html',context)

