from cgi import print_form
from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.decorators import login_required
from .forms import RegistroForm
from django.urls import reverse
from django.contrib.auth.models import User

# Create your views here.

def home(request):
    return render(request, "base/index.html")

def login(request):
    registro_form = RegistroForm

    if request.method == "POST":

        registro_form = registro_form(data=request.POST)
        print("holahola")
        print(registro_form.errors)
        if registro_form.is_valid():
            nombre_user = request.POST.get('registerFirstName', '')
            apellido_user = request.POST.get('registerLastName', '')
            username_user = request.POST.get('registerUsername', '')
            email = request.POST.get('email', '')
            password = request.POST.get('password', '')

            
            user = User.objects.create_user(username_user, email, password)
            user.first_name=nombre_user
            user.last_name=apellido_user
            user.save()

            return redirect(reverse('login'))
        
    return render(request, "base/signup.html")


@login_required(login_url='login')
def homeBanking(request):
    print(request.user)
    return render(request, "base/homeBanking.html")