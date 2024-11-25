from django.urls import path
from .views import register, login, user, activate_user

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('', user, name='user'),
    path('<int:id>/', user, name='user_id'),
    path('activate/<uidb64>/<token>/', activate_user, name='activate-user'),
]
