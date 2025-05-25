from django.urls import path, include
from .views import (
    my_page, update_user, verify_password, user_profile, join_product
)

urlpatterns = [
    path('', include('dj_rest_auth.urls')),  # 로그인, 로그아웃, 비밀번호 변경
    path('signup/', include('dj_rest_auth.registration.urls')),  # 회원가입
    path('mypage/', my_page, name='my_page'),
    path('mypage/update/', update_user, name='update_user'),
    path('verify-password/', verify_password, name='verify_password'),
    path('profile/<str:username>/', user_profile, name='user_profile'),
    path('join-product/', join_product, name='join_product'),
]
