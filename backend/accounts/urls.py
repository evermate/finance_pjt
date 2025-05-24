from django.urls import path, include
from .views import my_page
from .views import update_user
from .views import verify_password
from .views import user_profile

urlpatterns = [
    path('', include('dj_rest_auth.urls')),  # 로그인, 로그아웃, 비밀번호 변경
    path('signup/', include('dj_rest_auth.registration.urls')),  # 회원가입
    path('mypage/', my_page, name='my_page'),
    path('mypage/update/', update_user, name='update_user'),
    path('verify-password/', verify_password, name='verify_password'),
    path('profile/<str:username>/', user_profile, name='user_profile'),
]
