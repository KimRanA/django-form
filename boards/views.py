from django.shortcuts import render
from .models import Board


# Board 의 리스트
def index(request):
    boards = Board.objects.order_by('-pk')
    # 역순으로 가장 처음 만든 것이 가장 최근으로 나옴.
    context = {'boards' : boards}
    return render(request, 'boards/index.html')
