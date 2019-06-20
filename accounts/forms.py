# forms.py
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth import get_user_model


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()  # settings.AUTH_USER_MODEL -> account.user
        fields = UserCreationForm.Meta.fields


print('get_user_model() : ', get_user_model())


class CustomUserChangeForm(UserChangeForm):
    # 모델에 대한 정보가 담기는 곳
    class Meta:
        model = get_user_model()
        fields = ('email', 'first_name', 'last_name')
        # 위에 3항목만 바꿀 수 있도록 보여줌.
        # 만약에 위 코드가 없으면 잡다한 세부사항 다 뜸.

