from django.db import models
# 프라이머리키값 따로 만들거 없이 알아서 생성해줌.
# 질문 Question 클래스 ( 테이블 ) 생성: subject, content, create_date
class Question(models.Model):
    '''질문 모델'''
    subject = models.CharField(max_length=200) # 글자수 제한
    content = models.TextField() # 글자수 제한 없는 경우
    create_date = models.DateTimeField() # 날짜 + 시간

    def __str__(self):
        return self.subject

class Answer(models.Model):
    # on_delete=models.CASCADE: 답변에 연관된 질문이 삭제되면 그 답변도 모두 삭제.
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField()  # 날짜 + 시간