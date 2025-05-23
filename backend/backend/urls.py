from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('api/products/', include('products.urls')),
]

# ✅ 개발 중 이미지 서빙을 위한 static 설정
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
