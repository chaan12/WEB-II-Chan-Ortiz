from django.shortcuts import get_object_or_404, render, redirect
from .models import User, UserAddress

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

            user = User.objects.create(name=name, email=email, age=age, rfc=rfc, photo=photo)
            
            UserAddress.objects.create(user=user, street="", zip_code="", city="", country="")
            
            return redirect('users:index')
    
    except Exception as e:
        return render(request, "users/create.html", {"message": f"Error: {str(e)}", "status": "error"})
    
    return render(request, "users/create.html")

def userDetail(request, id):
    user = get_object_or_404(User, id=id)
    user_address = UserAddress.objects.filter(user=user).first()
    return render(request, "users/detail.html", {"user": user, "user_address": user_address})

def edit_user(request, id):
    user = get_object_or_404(User, id=id)
    user_address = UserAddress.objects.filter(user=user).first()
    
    if request.method == 'POST':
        try:
            user.name = request.POST.get('name', user.name)
            user.email = request.POST.get('email', user.email)
            user.age = request.POST.get('age', user.age)
            user.photo = request.POST.get('photo', user.photo)
            user.save()

            if user_address:
                user_address.street = request.POST.get('street', user_address.street)
                user_address.zip_code = request.POST.get('zip_code', user_address.zip_code)
                user_address.city = request.POST.get('city', user_address.city)
                user_address.country = request.POST.get('country', user_address.country)
                user_address.save()
            else:
                # Si no tiene dirección, se crea una nueva
                user_address = UserAddress.objects.create(
                    user=user,
                    street=request.POST.get('street', ""),
                    zip_code=request.POST.get('zip_code', ""),
                    city=request.POST.get('city', ""),
                    country=request.POST.get('country', "")
                )

            return redirect('users:index')

        except Exception as e:
            return render(request, 'users/edit.html', {'user': user, 'user_address': user_address, 'error': str(e)})

    return render(request, 'users/edit.html', {'user': user, 'user_address': user_address})