from django.urls import path
from .views import usersIndex, userDetail

urlpatterns = [
    path('', usersIndex, name='users-index'),
    path('<int:user_id>/', userDetail, name='user-detail'),
]
