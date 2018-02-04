from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Post
from .forms import PostForm
from .forms import UserSignup, UserLogin, UserForm, ProfileForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# Create your views here.
def usersignup(request):
    context = {}
    form = UserSignup()
    context['form'] = form

    if request.method == 'POST':
        form = UserSignup(request.POST)
        if form.is_valid():
            user = form.save()
            x = user.username
            y = user.password

            user.set_password(y)
            user.save()

            auth = authenticate(username=x, password=y)
            login(request, auth)

            return redirect("profile")
        messages.warning(request, form.errors)
        return redirect("signup")
    return render(request, 'signup.html', context)


def userlogin(request):
    context = {}
    form = UserLogin()
    context['form'] = form

    if request.method == 'POST':
        form = UserLogin(request.POST)
        if form.is_valid():
            user_user = form.cleaned_data['username']
            user_pass = form.cleaned_data['password']

            auth = authenticate(username=user_user, password=user_pass)
            if auth is not None:
                login(request, auth)
                return redirect("home")
            messages.warning(request, 'Incorrect user/pass...')
            return redirect("login")
        messages.warning(request, form.errors)
        return redirect("login")
    return render(request, 'login.html', context)


def userlogout(request):
    logout(request)
    return redirect("login")

def home(request, post_id):
    if not request.user.is_authenticated:
        return redirect("login")

    objects = Post.objects.filter(author=request.user)
    return render(request,'home.html',{'list': objects, 'user': request.user})


def create(request):
    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect("home")
    context = {
    "form": form,
    }
    return render(request, 'create.html', context)

def updateprofile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST or None, request.FILES or None, instance=request.user)
        profile_form = ProfileForm(request.POST or None, request.FILES or None, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('home')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'profile.html', { 'user_form': user_form,'profile_form': profile_form})