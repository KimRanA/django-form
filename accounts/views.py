from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from django.contrib.auth import login as auth_login, logout as auth_logout
from .forms import CustomUserChangeForm


def signup(request):
    if request.user.is_authenticated:
        # 로그인 되어 있을 때, signup 과 login 불가 하도록 boards 로 리턴
        return redirect('boards:index')

    if request.method == 'POST':
        # 사용자 회원가입 로직
        form = UserCreationForm(request.POST)
        # 사용자가 건네주는 모든 정보를 form 에 담아서 보관하겠다.
        if form.is_valid():  # 회원가입시 바로 로그인되서 boards 페이지
            user = form.save()
            auth_login(request, user)
            return redirect('boards:index')
    else:  # GET accounts/signup/
        form = UserCreationForm()
    context = {'form': form}
    return render(request, 'accounts/signup.html', context)


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
            return redirect('boards:index')
            pass
    else:  # GET accounts/login/ ->html 페이지만 렌더링
        form = AuthenticationForm()
    context = {'form': form}
    return render(request, 'accounts/login.html', context)

def logout(request):
    # 로그아웃 로직
    auth_logout(request)
    return redirect('boards:index')

def update(request):
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