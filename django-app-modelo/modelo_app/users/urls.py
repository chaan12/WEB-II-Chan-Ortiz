from django.urls import path
from .views import usersIndex, userDetail, createUsersView, createUser

urlpatterns = [
    path('', usersIndex, name='users-index'),
    path('create/', createUsersView, name='createUserView'),
    path('create-user/', createUser, name='createUser'),
    path('details/<int:id>/', userDetail, name='user-detail'),
]
