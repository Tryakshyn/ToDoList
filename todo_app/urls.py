from django.contrib import admin
from django.urls import path,include

# Определяем список URL-шаблонов для приложения

urlpatterns = [
    # Путь по умолчанию '' будет направляться в приложение
    path('', include('todo.urls')),
    # Путь 'admin/' будет направляться в административную панель Django
    path('admin/', admin.site.urls),
]
