from django.shortcuts import render
from .models import Bookmark, Personal_BookMark
from .forms import BookmarkForm, LoginForm
from django.http import HttpResponseRedirect
from django.contrib.auth import logout

def index(request):
    username = None
    if request.user.is_authenticated:
        username = request.user.username
    else :
        username = "Nope"

    if request.method == 'POST':
        form = BookmarkForm(request.POST)
        if form.is_valid(): 
            form.save()

    context = {}

    pbidlist = Personal_BookMark.objects.values_list('id')
    context['bookmarks'] = Bookmark.objects.exclude(id__in=pbidlist)

    if request.user.is_anonymous: 
	    context['personal_bookmarks'] = Personal_BookMark.objects.none()
    else: 
        context['personal_bookmarks'] = Personal_BookMark.objects.filter(user=request.user)

    context['form'] = BookmarkForm
    if username != None:
        context['user'] = username
    context['logout'] = logout(request)

    return render(request, 'bookmarks/index.html', context)

from django.contrib.auth import authenticate, login

def login_user(request):

    if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect("http://127.0.0.1:8000/bookmarks/")

    context = {}
    context['form'] = LoginForm

    return render(request, 'registration/login.html', context)