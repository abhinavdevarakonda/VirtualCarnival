from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate

from account.forms import RegistrationForm, AccountAuthenticationForm
# Create your views here.


def RegisterView(request,*args,**kwargs):
    user = request.user
    if user.is_authenticated:
        return HttpResponse(f"you are already registered as a user.authenticated email: {user.email}")
    context = {}

    if request.POST:                            #POST request is when a user wishes to send data to the server (in this case, the registration form)
        form = RegistrationForm(request.POST)
        if form.is_valid():                     #is valid checks if the form has all fields filled (email,username,password1,password2)
            form.save()                         #after this line all "clean_" functions will execute to validate further
            email           = form.cleaned_data.get('email').lower()
            raw_password    = form.cleaned_data.get('password1')
            account         = authenticate(email=email,password=raw_password)   #saves the account
            login(request,account)                                              #prebuilt login function (check imports)
            destination = kwargs.get("next")
            if destination:                     #if destination is not None then it should redirect
                return redirect(destination)
            return redirect("home")             #it will look for url home in urls.py
        else:
            context['registration_form'] = form


    return render(request,'account/register.html',context)

 
def LogoutView(request):
    logout(request)             #prebuilt logout function (check imports)
    return redirect("home")


def LoginView(request, *args,**kwargs):
    context = {}

    user = request.user
    if user.is_authenticated:
        return redirect("home")
 
    if request.POST:
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            email       = request.POST['email']    #POST request is when a user wishes to send data to the server (in this case, the registration form)
            password    = request.POST['password']
            user        = authenticate(email=email,password=password)
            if user:
                login(request,user)
                destination = GetRedirectIfExists(request)
                if destination:
                    return redirect(destination)
                return redirect("home")
        else:
            context["login_form"] = form

    return render(request,"account/login.html", context)


def GetRedirectIfExists(request):
    redirect = None
    if request.GET:
        if request.GET.get("next"):
            redirect = str(request.GET.get("next"))
    return redirect