'''
파일명 : question_views.py
설명 : 
생성일 : 2023/02/08
생성자 : ckair
'''
import logging

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from ..forms import QuestionForm
from ..models import Question


#큰트롤 알트 o  ; 임포트 정리

@login_required(login_url='common:login')
def question_vote(request, question_id):
    logging.info('좋아요 호출 :{}'.format(question_id))
    question = get_object_or_404(Question, pk=question_id)

    #본인 글은 추천 하지 못하게
    if request.user == question.author:
        messages.error(request, '본인이 작성한 글은 추천 할 수 없습니다.')
    else:
        question.voter.add(request.user)
    return redirect('pybo:detail', question_id=question.id)

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
