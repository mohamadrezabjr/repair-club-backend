from django.core.exceptions import ObjectDoesNotExist
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.exceptions import InvalidToken


class SafeTokenRefreshView(TokenRefreshView):
    """
    مثل TokenRefreshView استاندارد است، با این تفاوت که اگر توکن به کاربری
    اشاره کند که دیگر وجود ندارد (حذف شده یا دیتابیس ریست شده)، به‌جای خطای ۵۰۰
    یک پاسخ تمیز ۴۰۱ (توکن نامعتبر) برمی‌گرداند تا فرانت بتواند کاربر را
    به صفحه‌ی ورود هدایت کند.
    """

    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except ObjectDoesNotExist:
            raise InvalidToken("کاربر این توکن دیگر وجود ندارد")
