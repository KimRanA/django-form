from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
# AbstractUser : 여러개를 제공함.
# AbstractBaseUser : 상세하지만 필드가 2개 밖에 안됨.


class User(AbstractUser):  # 나는 User 를 만들것인데 AbstractUser 를 상속해서 만들 것이다.
    # User 관의 관계, 팔로워하는 팔로잉하는
    followers = models.ManyToManyField(
        settings.AUTH_USER_MODEL,  # 이 유저와 ManyToManyField 를 갖겠다.
        related_name='followings',

    )