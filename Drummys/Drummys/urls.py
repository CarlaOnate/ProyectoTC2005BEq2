from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('game/', include('unity.urls')),
    path('', include('web.urls'))
]
