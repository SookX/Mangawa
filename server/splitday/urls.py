from django.urls import path
from .views import splitDay, exercise, kgandreps

urlpatterns = [
    path('', splitDay, name='splitDay_model_based'),
    path('exercise/<int:id>/', exercise, name = 'exercise_add'),
    path('kgandreps/', kgandreps, name='kgandreps'),
    path('kgandreps/<int:id>/', kgandreps, name='kgandreps_with_id'),
]
