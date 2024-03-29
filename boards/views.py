from django.shortcuts import render, redirect, get_object_or_404
from .models import Board, Comment
from .forms import BoardForm, CommentForm
from django.views.decorators.http import require_POST, require_GET, require_http_methods
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model


# Board 의 리스트
@require_GET
# require 요청은 GET 으로만 보낼 수 있도록 설정한다.
def index(request):
    boards = Board.objects.order_by('-pk')
    # 역순으로 가장 처음 만든 것이 가장 최근으로 나옴.

    context = {
        'boards': boards,
        }
    return render(request, 'boards/index.html', context)


@login_required
@require_http_methods(['GET', 'POST'])
def create(request):
    if request.method == 'POST':
        form = BoardForm(request.POST)

        if form.is_valid():
            board = form.save(commit=False)
            board.user = request.user
            board.save()  # 저장한다.
            return redirect('boards:detail', board.pk)
    else:
        form = BoardForm()
    context = {'form': form}
    return render(request, 'boards/form.html', context)


# boards/3/
@require_GET
def detail(request, board_pk):
    board = get_object_or_404(Board, pk=board_pk)
#    Comment.objects.all()  # 모든 댓글이 꺼내지게 됨.
    comments = board.comment_set.order_by('-pk')
    comment_form = CommentForm()
    person = get_object_or_404(get_user_model(), pk=board.user_id)
    context = {
        'board': board,
        'comment_form': comment_form,
        'comments': comments,
        'person': person,
        }
    return render(request, 'boards/detail.html', context)


# POST boards/3/delete/
@require_POST
def delete(request, board_pk):
    # 특정 보드를 불러와서 삭제한다.
    board = get_object_or_404(Board, pk=board_pk)
    # 요청을 보낸 유저와 게시글의 작성자가 같을 때만 삭제
    if request.user == board.user:
        return redirect('boards:detail', board_pk)
    board.delete()
    return redirect('boards:index')


@login_required
@require_http_methods(['GET', 'POST'])
def update(request, board_pk):
    board = get_object_or_404(Board, pk=board_pk)
    if request.user != board.user:
        return redirect('boards:detail', board_pk)
    # POST boards/3/update/
    if request.method == 'POST':
        form = BoardForm(request.POST, instance=board)
        if form.is_valid():
            board = form.save(commit=False)  # 바로 저장하지 않고
            board.user = request.user  # 유저값을 대입한 뒤
            board = form.save()  # 저장한다.
            return redirect('boards:detail', board.pk)
    # GET boards/3/update
    else:
        form = BoardForm(instance=board)  # board 데이터 할당
    context = {
        'form': form,
        'board_pk': board_pk,
    }
    return render(request, 'boards/form.html', context)


@require_POST
def comments_create(request, board_pk):
    if not request.user.is_authenticated:
        return redirect('account')
    # 댓글 작성 로직
    comment_form = CommentForm(request.POST)
    # 유효성 검사
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.user = request.user
        comment.board_id = board_pk
        comment.save()  # 저장한다.
    return redirect('boards:detail', board_pk)


@require_POST
def comments_delete(request, board_pk, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    if comment.user == request.user:
        comment.delete()
    return redirect('boards:detail', board_pk)


@login_required()
def like(request, board_pk):
    board = get_object_or_404(Board, pk=board_pk)
    user = request.user

    # 보드를 좋아요 누른 모든 사람 중에서 user 가 없다면
    # 좋아요
    # 아니라면
    # 좋아요 취소
    # if request.user != board.like_users:
    #     user.like_boards.add(board)
    # else:
    #     user.like_boards.remove(board)

    if user in board.like_users.all():
        board.like_users.remove(user)
    else:
        user.like_boards.add(board)
    return redirect('boards:detail', board_pk)


@login_required()
def follow(request, board_pk, user_pk):
    # 팔로우 기능을 구현
    user = request.user
    person = get_object_or_404(get_user_model(), pk=user_pk)  # user_pk 유저

    # person 의 팔로워 목록에 user 가 없다면 추가하기
    # 그렇지 않고 팔로워 목록에 user 가 이미 존재한다면 제거하기
    # 만약에 user == person 이면 if문 안거치고 바로 리다이렉트
    if user != person:
        if user in person.followers.all():
            person.followers.remove(user)
        else:
            person.followers.add(user)
    return redirect('boards:detail', board_pk)
