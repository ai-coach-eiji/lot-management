from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser # 連携したいモデル
        fields = ('username', 'email', 'password1', 'password2')