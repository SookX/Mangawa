from django.urls import path
from .views import register, login
from graphene_django.views import GraphQLView
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    
    path("graphql/", csrf_exempt(GraphQLView.as_view(graphiql=True))),
]
