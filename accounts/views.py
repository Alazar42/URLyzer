from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

def user_register(request):
    error = None
    
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        
        if username == "" or password == "" or email == "":
            error = "Input all the required fields are required."
        else:
            try:
                user = User.objects.create_user(username=username, password=password, email=email)
                login(request, user)
                return redirect('home')  # Replace 'home' with the name of your homepage URL
            except Exception as e:
                error = f"Error: {str(e)}"

    return render(request, 'signup.html', {'error': error})  # Replace 'register.html' with your register template path

def user_login(request):
    error = None
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        if username == "" or password == "":
            error = "Input all the required fields."
        else:
            user = authenticate(username=username, password=password)
        
            if user is not None:
                login(request, user)
                return redirect('home')  # Replace 'home' with the name of your homepage URL
            else:
                error = "Invalid username or password."

    return render(request, 'signin.html', {'error': error})  # Replace 'login.html' with your login template path

def user_logout(request):
    logout(request)
    return redirect('login')  # Replace 'login' with the name of your login URL
