from django.shortcuts import get_object_or_404, render
from .models import User

def usersIndex(request):
    users = User.objects.all()
    return render(request, 'users/index.html', {'users': users})

def createUsersView(request):
    return render(request, "users/create.html")

def createUser(request):
    data = {}
    try:
        if request.method == "POST":
            name = request.POST.get("name")
            email = request.POST.get("email")
            age = request.POST.get("age")
            rfc = request.POST.get("rfc")
            photo = request.POST.get("photo")

            user = User(name=name, email=email, age=age, rfc=rfc, photo=photo)
            user.save()

            data["user"] = user
            data["message"] = "User created"
            data["status"] = "success"

    except Exception as e:
        data["message"] = str(e)
        data["status"] = "error"

    return render(request, "users/create.html", data)

def userDetail(request, id):
    user = get_object_or_404(User, id=id)
    return render(request, "users/detail.html", {"user": user})
