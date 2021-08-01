from django.shortcuts import render

# Create your views here.
def HomeScreenView(request,*args,**kwargs):
    context = {}
    return render(request, "misc/home.html", context)