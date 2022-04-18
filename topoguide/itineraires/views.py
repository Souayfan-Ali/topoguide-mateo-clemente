from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login

# Create your views here.


def auth(request):
  render(request,'itineraires/auth.html')

def my_view(request):
    username = request.POST['username']
    password = request.POST['pswd']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        print("Authenticated - WORKING")
        redirect('admin/')
    else:
        # Return an 'invalid login' error message.
        ...
