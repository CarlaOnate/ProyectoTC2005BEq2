from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('unity.urls')),
    path('web/', include('web.urls'))
]
