from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('authentication.urls')),
    path('teacher/', include('teacher.urls')),
    path('accounts/', include('django.contrib.auth.urls'))
]
