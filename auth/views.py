from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect

# Create your views here.


def user_register(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password != password2:
            return render(request, 'registration/registration.html', {'error': 'Пароли не совпадают'})

        if User.objects.filter(username=username).exists():
            return render(request, 'registration/registration.html', {'error': 'Пользователь с таким именем уже существует'})

        if User.objects.filter(email=email).exists():
            return render(request, 'registration/registration.html', {'error': 'Email уже зарегистрирован'})

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()

        user = authenticate(request, username=username, password=password)
        login(request, user)
        return redirect('index')

    return render(request, 'registration/registration.html')
