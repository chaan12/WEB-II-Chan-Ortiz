from django.shortcuts import render, get_object_or_404
from .models import User, UserAddress

def usersIndex(request):
    users = User.objects.all()
    return render(request, 'users/index.html', {'users': users})

def userDetail(request, user_id):
    user = get_object_or_404(User, id=user_id)
    address = UserAddress.objects.filter(user=user).first()

    return render(request, 'users/detail.html', {'user': user, 'address': address})
