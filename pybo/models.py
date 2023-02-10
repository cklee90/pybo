from django.db import models
from django.contrib.auth.models import User
# 프라이머리키값 따로 만들거 없이 알아서 생성해줌.
# 질문 Question 클래스 ( 테이블 ) 생성: subject, content, create_date
class Question(models.Model):
    '''질문 모델'''
    subject = models.CharField(max_length=200) # 글자수 제한
    content = models.TextField() # 글자수 제한 없는 경우
    create_date = models.DateTimeField() # 날짜 + 시간

    #author 필드 추가: 글쓴이
    author = models.ForeignKey(User, on_delete=models.CASCADE,related_name='author_question')   # 회원테이블에 사용자 정보가 삭제 되면 Question 테이블의 질문도 모두 삭제

    #수정일시 추가
    modify_date = models.DateTimeField(null=True, blank=True)
    # null=True: 데이터베이스에서 null 허용, blank=True: form.is_valid() 를 통한 입력값 검증시 값이 없어도 된다.

    # 추천인
    voter = models.ManyToManyField(User, related_name='voter_question')

    def __str__(self):
        return self.subject

class Answer(models.Model):
    # on_delete=models.CASCADE: 답변에 연관된 질문이 삭제되면 그 답변도 모두 삭제.
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField()  # 날짜 + 시간

    #author 필드 추가 : 글쓴이
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    # 입력 필드에 null 허용하기
    # author = models.ForeignKey(User, on_dnelete=models.CASCADE, null=True)

    # 수정일시 추가
    modify_date = models.DateTimeField(null=True, blank=True)

    # 추천인
    voter = models.ManyToManyField(User, related_name='voter_answer')
