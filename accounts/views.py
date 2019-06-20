from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import login as auth_login, logout as auth_logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
# 이건 반드시 로그인이 필요함. login_required 로그인 필수 설정
from .forms import CustomUserChangeForm, CustomUserCreationForm
from django.views.decorators.http import require_POST, require_GET, require_http_methods


@require_http_methods(['GET', 'POST'])
def signup(request):
    if request.user.is_authenticated:
        # 로그인 되어 있을 때, signup 과 login 불가 하도록 boards 로 리턴
        return redirect('boards:index')

    if request.method == 'POST':
        # 사용자 회원가입 로직
        form = CustomUserCreationForm(request.POST)
        # 사용자가 건네주는 모든 정보를 form 에 담아서 보관하겠다.
        if form.is_valid():  # 회원가입시 바로 로그인되서 boards 페이지
            user = form.save()
            auth_login(request, user)
            return redirect('boards:index')
    else:  # GET accounts/signup/
        form = CustomUserCreationForm()
    context = {'form': form}
    return render(request, 'accounts/signup.html', context)

@require_http_methods(['GET', 'POST'])
def login(request):
    if request.user.is_authenticated:
        return redirect('boards:index')
    if request.method == 'POST':
        # 로그인 로직 실행
        form = AuthenticationForm(request, request.POST)
        # 사용자 입력 유효성 검사
        if form.is_valid():
            # 로그인
            auth_login(request, form.get_user())
            return redirect(request.GET.get('next') or 'boards:index')
    else:  # GET accounts/login/ ->html 페이지만 렌더링
        form = AuthenticationForm()
    context = {'form': form}
    return render(request, 'accounts/login.html', context)


@require_http_methods(['GET', 'POST'])
def logout(request):
    # 로그아웃 로직
    auth_logout(request)
    return redirect('boards:index')


@login_required
@require_http_methods(['GET', 'POST'])
def update(request):
    if not request.user.is_authenticated:
        # 로그인이 되어있지 않은데, update 페이지로 가려한다면 main 페이지로 보낸다.
        return redirect('boards:index')
    if request.method == 'POST':
        # 업데이트 로직 수행
        form = CustomUserChangeForm(request.POST, instance=request.user)
        # UserChangeForm 으로 사용자가 보낸 정보를 받아옴.
        # 원하는 정보만 사용할 수 있도록 forms.py를 생성하고,
        # UserChangeForm 은 CustomUserChangeForm 로 변경함.
        if form.is_valid():
            form.save()
            return redirect('boards:index')
    else:
        form = CustomUserChangeForm(instance=request.user)
        # request.user = 지금 로그인해 있는 유저 정보
        # 원하는 정보만 사용할 수 있도록 forms.py를 생성하고,
        # UserChangeForm 은 CustomUserChangeForm 로 변경함.

    context = {'form': form}
    return render(request, 'accounts/update.html', context)


@login_required
@require_http_methods(['GET', 'POST'])
def change_password(request):
    if request.method == 'POST':
        # 비밀번호 변경로직
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():  # 유효성 검사
            form.save()
            # 세션의 정보와 회원의 정보가 달라져서
            # 세션을 유지한 상태로 새롭게 업데이트
            update_session_auth_hash(request, request.user)
            return redirect('boards:index')
        pass
    else:
        form = PasswordChangeForm(request.user)
    # 왜 두줄을 땡겨? 입력했던 정보를 가져오기 위해서
    context = {'form': form}
    return render(request, 'accounts/change_password.html', context)


@require_http_methods(['POST'])
def delete(request):
    # 유저 삭제 로직
    request.user.delete()
    return redirect('boards:index')



