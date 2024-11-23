from django.urls import path
from .views import register, login, user

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('', user, name='user'),
    path('<int:id>/', user, name='user_id')
]
