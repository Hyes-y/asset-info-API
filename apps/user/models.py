from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    # 기본 필드 중 사용하지 않는 필드 제외
    first_name = None
    last_name = None

    name = models.CharField(verbose_name='이름', max_length=30)
