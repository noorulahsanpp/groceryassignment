from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from .models import grocery
from django.contrib.auth import login, logout, authenticate


# Create your views here.
from mainapp.models import grocery


def home(request):
    if request.method == 'GET':
        return render(request, 'mainapp/loginuser.html', {'form': AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'mainapp/loginuser.html',
                          {'form': AuthenticationForm(), 'error': 'Username and password did not match'})
        else:
            login(request, user)
            return redirect('index')

    

@login_required
def index(request):
    if request.method == 'GET':
        items = grocery.objects.filter(user=request.user).order_by('date').reverse()
        return render(request, 'mainapp/index.html', {'items': items})
    else:
        date = request.POST['date']
        items = grocery.objects.filter(user=request.user, date=date)
        return render(request, 'mainapp/index.html', {'items': items})


@login_required
def add(request):
    return render(request, 'mainapp/add.html')

@login_required
def update(request):
    return render(request, 'mainapp/update.html')

def loginuser(request):
    if request.method == 'GET':
        return render(request, 'mainapp/loginuser.html', {'form': AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'mainapp/loginuser.html',
                          {'form': AuthenticationForm(), 'error': 'Username and password did not match'})
        else:
            login(request, user)
            return redirect('index')

def signupuser(request):
    if request.method == 'GET':
        return render(request, 'mainapp/signupuser.html', {'form': UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('index')
            except IntegrityError:
                return render(request, 'mainapp/signupuser.html',
                              {'form': UserCreationForm(), 'error': 'Username already taken'})
        else:
            return render(request, 'mainapp/signupuser.html',
                          {'form': UserCreationForm(), 'error': 'Password does not match'})

@login_required
def logoutuser(request):
    # POST is used here because browsers load all the anchor tags in the website background to load pages faster
    if request.method == 'POST':
        logout(request)
        return redirect('loginuser')

@login_required
def deleteitem(request, item_pk):
    gr = get_object_or_404(grocery, pk=item_pk, user=request.user)
    if request.method == 'POST':
        gr.delete()
        return redirect('index')

@login_required
def viewitem(request, item_pk):
    import dateutil.parser
    item = get_object_or_404(grocery, pk=item_pk, user=request.user)
    if request.method == 'GET':
        i = str(item.date)
        d = dateutil.parser.parse(i).date()
        return render(request, 'mainapp/update.html', {'item': item, 'd': str(d)})
    else:
        if request.POST['name'] and request.POST['status'] and request.POST['quantity'] and request.POST['date'] :
            item.name = request.POST['name']
            item.status = request.POST['status']
            item.quantity = request.POST['quantity']
            item.date = request.POST['date']
            item.user = request.user
            item.save()
            return redirect('index')


@login_required
def additem(request):
    if request.method == 'POST':
        if request.POST['name'] and request.POST['status'] and request.POST['quantity'] and request.POST['date'] :
            gr = grocery()
            gr.name = request.POST['name']
            gr.status = request.POST['status']
            gr.quantity = request.POST['quantity']
            gr.date = request.POST['date']
            gr.user = request.user
            gr.save()
            return redirect('index')

    else:
        return render(request, 'mainapp/add.html', {'error': 'All fields are required'})