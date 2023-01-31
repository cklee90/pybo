from django.shortcuts import render,get_object_or_404, redirect
from django.http import HttpResponse
from django.utils import timezone
from .models import  Question

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

def answer_create(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    question.answer_set.create(content=request.POST.get('content'),create_date=timezone.now())
    return redirect('pybo:detail',question_id=question.id)

def detail(request, question_id):
    '''question 상세'''
    print('1. question_id:{}'.format(question_id))
    # question = Question.objects.get(id=question_id)
    question = get_object_or_404(Question, pk=question_id)
    print('2. question:{}'.format(question))
    context = {'question':question}
    return render(request, 'pybo/question_detail.html',context)

def index(request):
    '''question 목록'''
    #list order create_date desc
    question_list = Question.objects.order_by('-create_date')  # order_by('-필드') 마이너스 표시 붙이면 DESC, 없으면 ASC
    #question_list = Question.objects.filter(id=99)   # 없을때 잘 되는지 확인
    context = {'question_list':question_list}
    print('question_list:{}'.format(question_list))
    return render(request,'pybo/question_list.html',context)

