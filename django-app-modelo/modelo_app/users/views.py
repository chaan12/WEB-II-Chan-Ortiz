from django.shortcuts import get_object_or_404, render, redirect
from .models import User

def usersIndex(request):
    users = User.objects.all()
    return render(request, 'users/index.html', {'users': users})

def createUsersView(request):
    return render(request, "users/create.html")

def createUser(request):
    try:
        if request.method == "POST":
            name = request.POST.get("name")
            email = request.POST.get("email")
            age = request.POST.get("age")
            rfc = request.POST.get("rfc")
            photo = request.POST.get("photo")

            User.objects.create(name=name, email=email, age=age, rfc=rfc, photo=photo)
            return redirect('users:index')
    
    except Exception as e:
        return render(request, "users/create.html", {"message": f"Error: {str(e)}", "status": "error"})
    
    return render(request, "users/create.html")

def userDetail(request, id):
    user = get_object_or_404(User, id=id)
    return render(request, "users/detail.html", {"user": user})

def edit_user(request, id):
    user = get_object_or_404(User, id=id)
    
    if request.method == 'POST':
        try:
            user.name = request.POST.get('name', user.name)
            user.email = request.POST.get('email', user.email)
            user.age = request.POST.get('age', user.age)
            user.photo = request.POST.get('photo', user.photo)
            user.save()
            return redirect('users:index')
        except Exception as e:
            return render(request, 'users/edit.html', {'user': user, 'error': str(e)})
    
    return render(request, 'users/edit.html', {'user': user})
