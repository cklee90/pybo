'''
파일명 : pybo_filter.py
설명 :  빼기 필터
생성일 : 2023/02/03
생성자 : ckair
'''

from django import template

register = template.Library()

@register.filter
def sub(value, arg):
    ''' @register.filter : 템플릿에서 필터로 사용 할수 있게 된다. 빼기 필터 '''
    return value - arg