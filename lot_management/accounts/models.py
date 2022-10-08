from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser): # AbstractUser: 抽象クラス
    pass
