from django.urls import path
from . import views


# User Authentication related routes

urlpatterns = [
    path("user/profile/", views.User.as_view()),
    path("register/", views.UserRegister.as_view()),
    path("login/", views.UserAuth.as_view()),
    path("user/delete/", views.UserDelete.as_view()),
    path("user/list/", views.UserList.as_view()),

]
