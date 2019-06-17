from django.shortcuts import render, redirect, get_object_or_404
from .models import Board
from .forms import BoardForm
from django.views.decorators.http import require_POST, require_GET, require_http_methods

# Board 의 리스트
@require_GET
# require 요청은 GET 으로만 보낼 수 있도록 설정한다.
def index(request):
    boards = Board.objects.order_by('-pk')
    # 역순으로 가장 처음 만든 것이 가장 최근으로 나옴.
    context = {'boards': boards}
    return render(request, 'boards/index.html', context)

@require_http_methods(['GET','POST'])
def create(request):
    if request.method == 'POST':
        form = BoardForm(request.POST)
        if form.is_valid():
            board = form.save()
            return redirect('boards:detail', board.pk)
    else:
        form = BoardForm()
    context = {'form': form}
    return render(request, 'boards/form.html', context)


# boards/3/
@require_GET
def detail(request, board_pk):
    board = get_object_or_404(Board, pk=board_pk)
    context = {'board': board}
    return render(request, 'boards/detail.html', context)

# GET boards/3/delete/
@require_POST
def delete(request, board_pk):
    # 특정 보드를 불러와서 삭제한다.
    board = get_object_or_404(Board, pk=board_pk)
    board.id()
    return redirect('boards:index')


@require_http_methods(['GET','POST'])
def update(request, board_pk):
    board = get_object_or_404(Board, pk=board_pk)
    # POST boards/3/update/
    if request.method == 'POST':
        form = BoardForm(request.POST, instance=board)
        if form.is_valid():
            board = form.save()
            return redirect('boards:detail', board.pk)
    # GET boards/3/update
    else:
        form = BoardForm(instance=board)  # board 데이터 할당
    context = {
        'form': form,
        'board_pk': board_pk,
    }
    return render(request, 'boards/form.html', context)