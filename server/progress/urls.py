from django.urls import path
from .views import progress

urlpatterns = [
    path('', progress, name='progress-list'),
    path('<int:id>/', progress, name='progress-detail'),
]
