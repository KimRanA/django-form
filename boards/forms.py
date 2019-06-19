from django import forms
from .models import Board, Comment


class BoardForm(forms.ModelForm):
    class Meta:
        model = Board
        fields = ('title', 'content', )


class CommentForm(forms.ModelForm):
    content = forms.CharField(label=False)  # 앞을 라벨 작업시 content 에 대한 라벨은 작업 안함.
    class Meta:  # 메타데이터 : 데이터를 위한 데이터
        model = Comment
        fields = ('content', )