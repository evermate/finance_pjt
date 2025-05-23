from django.urls import path, include
from .views import my_page
from .views import update_user

urlpatterns = [
    path('', include('dj_rest_auth.urls')),  # 로그인, 로그아웃, 비밀번호 변경
    path('signup/', include('dj_rest_auth.registration.urls')),  # 회원가입
    path('mypage/', my_page, name='my_page'),
    path('mypage/update/', update_user, name='update_user'),
]
