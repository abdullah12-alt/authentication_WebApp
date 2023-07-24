from django.urls import path
from .views import *
from .views import RegisterUser



urlpatterns = [
    path('register/',RegisterUser.as_view()),
    path('login/', LoginUser.as_view()),
    path('logout/', LogoutUser.as_view()),
]

