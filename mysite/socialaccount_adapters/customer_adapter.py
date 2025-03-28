from allauth.socialaccount.adapter import DefaultSocialAccountAdapter

class CustomAdapter(DefaultSocialAccountAdapter):
    def populate_user(self, request, sociallogin, data):
        user = super().populate_user(request, sociallogin, data)
        user.username = sociallogin.account.extra_data.get('email')  # 使用邮箱作为用户名
        return user