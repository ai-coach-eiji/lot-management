from django.shortcuts import render
from django.views.generic import CreateView, TemplateView # CreateView, TemplateView: 作成, 表示に特化したテンプレート
from .forms import CustomUserCreationForm
from django.urls import reverse_lazy

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

class SignUpView(CreateView):
    form_class = CustomUserCreationForm # 使用するユーザーモデル
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('accounts:signup_success')

    def form_valid(self, form):
        # CreateViewクラスのform_validをオーバーライド
        user = form.save()
        self.object = user
        return super().form_valid(form) # HttpResponseRedirectオブジェクト

class SignUpSuccessView(TemplateView):
    template_name = 'accounts/signup_success.html'

@method_decorator(login_required, name='dispatch')
class MyPageView(TemplateView):
    template_name = 'accounts/mypage.html'

