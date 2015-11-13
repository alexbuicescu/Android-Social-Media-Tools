from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.files.uploadedfile import SimpleUploadedFile
from django.http import HttpResponseForbidden

from fb.models import User, UserPost, UserPostComment, UserProfile
from fb.forms import (
    UserAddForm, UserPostForm, UserPostCommentForm, UserLogin, UserProfileForm,
)

from django.core.cache import cache

def add_user(request):
    if request.method == 'GET':
        login_form = UserAddForm()
        context = {
            'form': login_form,
        }
        return render(request, 'adduser.html', context)
    elif request.method == 'POST':
        form = UserAddForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            firstName = request.POST['firstName']
            lastName = request.POST['lastName']
            user = User(firstName=firstName, lastName=lastName)
            user.save()
            return redirect('/users/')


def show_users(request):

    users = User.objects.all()
    if request.method == 'GET':
        context = {
            'users': users,
            'infoGoogle': verify_google_token(),
            'infoFacebook': verify_facebook_token(),
        }
        return render(request, 'users.html', context)


@login_required
def index(request):
    posts = UserPost.objects.all()
    if request.method == 'GET':
        form = UserPostForm()
    elif request.method == 'POST':
        form = UserPostForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['text']
            post = UserPost(text=text, author=request.user)
            post.save()

    context = {
        'posts': posts,
        'form': form,
    }
    return render(request, 'index.html', context)


@login_required
def post_details(request, pk):
    post = UserPost.objects.get(pk=pk)

    if request.method == 'GET':
        form = UserPostCommentForm()
    elif request.method == 'POST':
        form = UserPostCommentForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            comment = UserPostComment(text=cleaned_data['text'],
                                      post=post,
                                      author=request.user)
            comment.save()

    comments = UserPostComment.objects.filter(post=post)

    context = {
        'post': post,
        'comments': comments,
        'form': form,
    }

    return render(request, 'post_details.html', context)


def login_view(request):
    if request.method == 'GET':
        login_form = UserLogin()
        context = {
            'form': login_form,
        }
        return render(request, 'login.html', context)
    if request.method == 'POST':
        login_form = UserLogin(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            context = {
                'form': login_form,
                'message': 'Wrong user and/or password!',
            }
            return render(request, 'login.html', context)


@login_required
def logout_view(request):
    logout(request)
    return redirect(reverse('login'))


@login_required
def profile_view(request, user):
    profile = UserProfile.objects.get(user__username=user)
    context = {
        'profile': profile,
    }
    return render(request, 'profile.html', context)


@login_required
def edit_profile_view(request, user):
    profile = UserProfile.objects.get(user__username=user)
    if not request.user == profile.user:
        return HttpResponseForbidden()
    if request.method == 'GET':
        data = {
            'first_name': profile.user.first_name,
            'last_name': profile.user.last_name,
            'gender': profile.gender,
            'date_of_birth': profile.date_of_birth,
        }
        avatar = SimpleUploadedFile(
            profile.avatar.name, profile.avatar.file.read()) \
            if profile.avatar else None
        file_data = {'avatar': avatar}
        form = UserProfileForm(data, file_data)
    elif request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile.user.first_name = form.cleaned_data['first_name']
            profile.user.last_name = form.cleaned_data['last_name']
            profile.user.save()

            profile.gender = form.cleaned_data['gender']
            profile.date_of_birth = form.cleaned_data['date_of_birth']
            if form.cleaned_data['avatar']:
                profile.avatar = form.cleaned_data['avatar']
            profile.save()

            return redirect(reverse('profile', args=[profile.user.username]))
    context = {
        'form': form,
        'profile': profile,
    }
    return render(request, 'edit_profile.html', context)


@login_required
def like_view(request, pk):
    post = UserPost.objects.get(pk=pk)
    post.likers.add(request.user)
    post.save()
    return redirect(reverse('post_details', args=[post.pk]))

from oauth2client import client, crypt
import time

def verify_google_token():

    token = 'eyJhbGciOiJSUzI1NiIsImtpZCI6IjgwNDhmNDQ3YzVjNmRiZGI4ODIwOTYyOTJmYTFiNzk2ZWUzZGMyMTUifQ.eyJpc3MiOiJodHRwczovL2FjY291bnRzLmdvb2dsZS5jb20iLCJhdWQiOiI4OTIzMTQ4NjIzMzQtcDA4OHVzNnNmY2NvNjhtdWQ1dmJsMnRnODY2dDRxZDAuYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJzdWIiOiIxMDA2NDQzODQzNTIzNTk4MzMyNDIiLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwiYXpwIjoiODkyMzE0ODYyMzM0LW1uazBqZm9ydnFzMGhyYXVsOWE0bTJtdXBhNDdvZGZqLmFwcHMuZ29vZ2xldXNlcmNvbnRlbnQuY29tIiwiZW1haWwiOiJhbGV4YnVpY2VzY3VAZ21haWwuY29tIiwiaWF0IjoxNDQ3MjU0NzE0LCJleHAiOjE0NDcyNTgzMTQsInBpY3R1cmUiOiJodHRwczovL2xoNC5nb29nbGV1c2VyY29udGVudC5jb20vLUItUGptaXlDZWs0L0FBQUFBQUFBQUFJL0FBQUFBQUFBRjRjL21nYk1ndlJfbFhFL3M5Ni1jL3Bob3RvLmpwZyIsImxvY2FsZSI6ImVuIiwibmFtZSI6IkFsZXhhbmRydSBCdWljZXNjdSIsImdpdmVuX25hbWUiOiJBbGV4YW5kcnUiLCJmYW1pbHlfbmFtZSI6IkJ1aWNlc2N1In0.hVMhMMvLcmMRVrVaG0-zuqJhq_bm6VZ-YVe8ygK1p0Z4Wb46yzhSKu7HFDuGJ6dIbS5yM88LH9yaK-3AUCGdElVSjV3bochZR302xYSNjtT2UC70F_tRLaY5KJiA-6e7bPHfEdljgBhrwaspXxV-sVeCUj6nBW5j2UoJZD2tMWHZzfUlXs8_42UEQ_yqzNQ5BEiGZ2LzW61-6gHIOVuazNAh6Pyly4A6-jycHoMthk2d-wwOdJ6ITMcTdPTDiR52SsQbDMJIDz330yYAp_ct5dFYZsvrwqimy1uibysQw7iQuO7MVEt6p1IY2IYkNtJd1N5J9oQx42-9wBJMGXmtQw'

    CLIENT_ID = 'insert_client_id_here.apps.googleusercontent.com'
    ANDROID_CLIENT_ID = 'insert_android_client_id_here.apps.googleusercontent.com'
    WEB_CLIENT_ID = 'insert_web_client_id_here.apps.googleusercontent.com'

    if cache.get(token) != None:
        print 'From cache:', cache.get(token)
        # print 'time:', cache.get(token)['exp'], current_milli_time()
        return 'From cache:\n ' + ', '.join("%s=%r" % (key,val) for (key,val) in cache.get(token).iteritems())
    else:
        # (Receive token by HTTPS POST)
        try:
            idinfo = client.verify_id_token(token, CLIENT_ID)
            # If multiple clients access the backend server:
            if idinfo['aud'] not in [ANDROID_CLIENT_ID, WEB_CLIENT_ID]:
                raise crypt.AppIdentityError("Unrecognized client.")
            if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
                raise crypt.AppIdentityError("Wrong issuer.")
            userid = idinfo['sub']
            cache.set(token, idinfo, idinfo['exp'] - current_milli_time())
            print 'Not from cache', idinfo
            return 'Not from cache:\n ' + ', '.join("%s=%r" % (key,val) for (key,val) in idinfo.iteritems())
        except crypt.AppIdentityError:
            # Invalid token
            print 'Invalid Token'
            return 'Invalid Token'

def verify_facebook_token():
    import requests

    APP_ID_FACEBOOK = 'insert_app_id_here'

    access_token = 'CAAXpaL9lZAecBADqpFnSNwxXuhGhAhSDvTppWE4vp5tilxpIES9RYW91d9ZCliwVjZBHj3CzZADr3UML804XykS4Da3UdMD9cwFNfLdnDA7lZCj58eql6FuAtGO7LXhy3mtKrPEQMyu83lCRiDBPmTT5QMHRzLLc4LyzrlHUhukuZAukuzbxeWCcMyOthaQvHhL0RZAbZBeEtiIQfTi7EPedjqKbNsEPL7xPlEgw5Hb17wZDZD'


    # import simplejson
    params = {'fields': 'id,email', 'access_token': access_token}
    # text = requests.get("https://graph.facebook.com/me", params=params).json()

    params2 = {'fields': 'id', 'access_token': access_token}
    # text2 = requests.get("https://graph.facebook.com/app", params=params2).json()

          # '"body":"fields=id,email",' \
          # '"body":{"fields":"id"},' \
    req = 'batch=[' \
          '{"method":"GET",' \
          '"relative_url":"me?fields=id,email"},' \
          '{"method":"GET",' \
          '"relative_url":"app?fields=id"}' \
          ']&access_token=' + access_token
    text3 = requests.post("https://graph.facebook.com", params=req).json()

    # json = simplejson.loads(text)
    # response_id = json["id"]
    print text3[0]['body']
    print text3[1]['body']
    return "yo facebook"#', '.join("%s=%r" % (key,val) for (key,val) in text3.iteritems())

    # return response_id == id

current_milli_time = lambda: int(round(time.time()))
