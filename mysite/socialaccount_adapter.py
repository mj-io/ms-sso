import logging

from allauth.socialaccount.adapter import DefaultSocialAccountAdapter

logger = logging.getLogger(__name__)
class CustomAdapter(DefaultSocialAccountAdapter):
    def populate_user(self, request, sociallogin, data):
        logger.info("populate_user", data)
        user = super().populate_user(request, sociallogin, data)
        user.username = sociallogin.account.extra_data.get('email')  # 使用邮箱作为用户名
        return user