'''
파일명 : answer_views.py
설명 : 
생성일 : 2023/02/08
생성자 : ckair
'''

import logging

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect, resolve_url
from django.utils import timezone

from ..forms import AnswerForm
from ..models import Question, Answer

@login_required(login_url='common:login')
def answer_vote(request, answer_id):
    '''답변 좋아요'''
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user == answer.author:
        messages.error(request, '본인이 작성한 댓글에 좋아요 할수 없습니다.')
    else:
        answer.voter.add(request.user)

    # http://127.0.0.1:8000/pybo/543/#answer_46
    return redirect('{}#answer_{}'.
                    format(resolve_url('pybo:detail', question_id=answer.question.id), answer.id))

@login_required(login_url='common:login')
def answer_delete(request, answer_id):
    '''답변 삭제'''
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:
        messages.error(request, '삭제 권한이 없습니다')
    else:
        answer.delete()
    return redirect('pybo:detail', question_id = answer.question.id)

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
            #http://127.0.0.1:8000/pybo/543/#answer_46
            return redirect('{}#answer_{}'.
                            format(resolve_url('pybo:detail',question_id = answer.question.id),answer.id))


    else:                          # 수정 form 의 template 을 띄워줌
        form = AnswerForm(instance=answer)
    context = {'answer':answer, 'form':form}
    return render(request, 'pybo/answer_form.html', context)

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
            #http://127.0.0.1:8000/pybo/543/#answer_46
            return redirect('{}#answer_{}'.
                            format(resolve_url('pybo:detail',question_id = question.id),answer.id))
    else:
        form = AnswerForm()


    # form validation
    context = {'question':question,'form':form}
    return render(request,'pybo/question_detail.html',context)

