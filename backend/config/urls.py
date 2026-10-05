from django.conf import settings
from django.contrib import admin
from django.urls import path

# Админка только по секретному пути из ADMIN_URL; стандартный /admin/ не подключён и отдаёт 404.
urlpatterns = [
    path(settings.ADMIN_URL, admin.site.urls),
]
