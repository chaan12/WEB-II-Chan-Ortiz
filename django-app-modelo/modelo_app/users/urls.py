from django.urls import path
from .views import usersIndex, userDetail, createUsersView, createUser, edit_user

app_name = 'users'

urlpatterns = [
    path('', usersIndex, name='index'),
    path('create/', createUsersView, name='createUsersView'),
    path('create-user/', createUser, name='createUser'),
    path('detail/<int:id>/', userDetail, name='userDetail'),
    path('edit/<int:id>/', edit_user, name='edit_user'),
    path("updateUser", edit_user, name="updateUser")
    
]
