from django import forms
from .models import Board, Comment


class BoardForm(forms.ModelForm):
    class Meta:
        model = Board
        fields = ('title', 'content', )


class CommentForm(forms.ModelForm):
    class Meta:  # 메타데이터 : 데이터를 위한 데이터
        model = Comment
        fields = ('content', )