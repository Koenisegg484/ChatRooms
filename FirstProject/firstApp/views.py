from .forms import RoomForm
from django.db.models import Q
from .models import Room, Topic, Message
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout



# This creates a login form for the incoming users also logs them in
def user_login_register(request):
    # If the user is already logged in, they are redirected to the home page
    # helps in not accessing the login page bu using the url in browser
    if request.user.is_authenticated:
        return redirect('home')
    
    page = 'login'
    
    if (request.method == 'POST'):
        username = request.POST.get('username').lower()
        pwd = request.POST.get('password')

        # Checks if the user exists in the database
        try :
            user = User.objects.get(username = username)
        except :
            messages.error(request, "The user does not exist.")

        # Authenticates the user
        user = authenticate(request, username=username, password=pwd)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "The Username or Password do not match.")
    context = {'page':page}
    return render (request, 'firstApp/login_registration.html', context)


# This is for registering the user
def register_user(request):
    form = UserCreationForm()

    # Validating the form data then committing it in the database
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Sorry, some error occured at our side.")
    context = {'form':form}
    return render(request, 'firstApp/login_registration.html', context)

# This logs out the user from the application
def logoutuser(request):
    logout(request)
    return redirect('home')

# This is the home page of the website
def home(req):
    return render(req, 'firstApp/home.html')


# This is the page where all the current rooms are listed
def room(req):
    q = req.GET.get('q') if req.GET.get('q') != None else ''
    q = q.strip().lower()
    topics = Topic.objects.all()
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) | 
        Q(name__icontains=q) |
        Q(description__icontains=q) 
        # | Q(host__icontains=q)
    )
    room_count = Room.objects.count()
    context =  {'rooms':rooms, 'topics':topics, 'counts':room_count}
    # print(f"\n\n{room_count}\n\n")
    return render(req, 'firstApp/room.html',context)


# This is for creating pages to show details of a particular room
def particularRooms(request, pk):
    room = Room.objects.get(id=pk)
    participants = room.participants.all()
    commentmessages = room.message_set.all().order_by('-created')

    if request.method == "POST":
        message = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('msg')
        )
        return redirect('/room/'+pk)
    context = {'room' : room, 'pk' : pk, 'comments':commentmessages, 'participants' : participants}

    return render(request, 'firstApp/partRoom.html', context)



# Adding decorator here, allowing only logged in users to access this page
# @login_required(login_url='login')
@login_required(login_url='login_registration')
# This is for creating a room
def createRoom(request):
    form = RoomForm()

    if request.method == 'POST':
        form = RoomForm(request.POST)
        name = request.POST.get('name')
        if form.is_valid():
            form.save()
            print("\n\nA room has been created of the name : {0}".format(name))
            return redirect('room')

    context = {'form' : form}
    return render(request, 'firstApp/createRoom.html', context)


# Adding decorator here, allowing only logged in users to access this page
@login_required(login_url='login_registration')
# This is for updating an existing room
def updateRoom(request, pk):
    room = Room.objects.get(id = pk)

    if request.user != room.host:
        nallowed = """<center><h1>You are nt ot allowed to Update the current room's details.</h1></center>"""
        return HttpResponse(nallowed)

    form = RoomForm(instance=room)

    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        name = request.POST.get('name')
        if form.is_valid():
            form.save()
            print("\n\nThe room has been editted of the name : {0}".format(name))
            return redirect('room')

    context = {'form' : form}
    return render(request, 'firstApp/createRoom.html', context)


# Adding decorator here, allowing only logged in users to access this page
@login_required(login_url='login_registration')
# This is for deleting an existing room from the database
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        nallowed = """<center><h1>You are nt ot allowed to delete the current room.</h1></center>"""
        return HttpResponse(nallowed)
    
    if request.method == 'POST':
        room.delete()
        return redirect('room')
    return render(request, 'firstApp/delete.html', {'obj':room})