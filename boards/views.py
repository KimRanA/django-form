from django.shortcuts import render, redirect, get_object_or_404
from .models import Board


# Board 의 리스트
def index(request):
    boards = Board.objects.order_by('-pk')
    # 역순으로 가장 처음 만든 것이 가장 최근으로 나옴.
    context = {'boards': boards}
    return render(request, 'boards/index.html', context)


def create(request):
    if request.method == 'GET':
        return render(request, 'boards/create.html')
    else:
        # Board 정보를 받아서 데이터베이스에 저장하는 로직
        title = request.POST.get('title')
        content = request.POST.get('content')
        board = Board(title=title, content=content)
        board.save()
        return redirect('boards:index')


# boards/3/
def detail(request, board_pk):
    board = get_object_or_404(Board, pk=board_pk)
    context = {'board': board}
    return render(request, 'boards/detail.html', context)
