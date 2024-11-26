from django.urls import path
from .views import splitDay, exercise

urlpatterns = [
    path('', splitDay, name='splitDay_model_based'),
    path('<int:id>/', exercise, name = 'exercise_add')
]
