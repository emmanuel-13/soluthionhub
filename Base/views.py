from typing import Any
from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from .forms import *
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from .mixins import MyLoginRequiredMixins

# rooms = [
#     {'id': 1, 'name': "Python"},
#     {'id': 2, 'name': "Django"},
#     {'id': 3, 'name': "Forton"},
# ]



def login_user(request):
    page = 'login'
    
    if request.user.is_authenticated:
        return redirect('home')
    
    
    
    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')
        
        try:
            
            user = User.objects.get(email=email)
        except:
            messages.info(request, "User not found")
            
        user = authenticate(request, email=email, password=password)
        print(user)
        
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, "User not found")
    context =  {'page': page}
    return render(request, 'base/login_register.html', context)


def logout_user(request):
    logout(request)
    return redirect('home')

def register_user(request):
    form = MyUserCreationForm()
    
    
    
    if request.user.is_authenticated:
        return redirect('home')
    
    
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            if user.first_name == '' and user.last_name == '':
                return redirect('edit_user')
            return redirect('edit_user')
        else:
            messages.error(request, "Error registering user")
    
    context = {
        'form': form
    }
    return render(request, 'base/login_register.html', context)


# Create your views here.
def home(request):
    
    if request.user.is_authenticated:
        if request.user.first_name == '' and request.user.last_name == '':
            return redirect('edit_user')
    else:
        pass
    
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q)| 
        Q(name__icontains=q)| Q(description__icontains=q)
        )
    room_count = rooms.count()
    topic = Topic.objects.all()[:4]
    room_topic = Room.objects.filter(topic=topic)
    message = Message.objects.filter(Q(room__topic__name__icontains=q))
    context = {
        'room': rooms, 'topic':  topic, 'room_count': room_count, 'room_messages': message, 'room_topic': room_topic
    }
    return render(request, 'base/home.html', context)


# @login_required(login_url='login')
def userprofile(request, pk):
    
    if request.user.is_authenticated:
        if request.user.first_name == '' and request.user.last_name == '':
            return redirect('edit_user')
    else:
        pass
    roomer = True
    print(roomer)
    user = User.objects.get(pk=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    context = {'user': user, 'room': rooms, 'room_messages': room_messages, 'topic': topics, 'roomer': roomer}
    return render(request, 'Base/user_profile.html', context)

def room(request, pk):
    if request.user.is_authenticated:
        if request.user.first_name == '' and request.user.last_name == '':
            return redirect('edit_user')
    else:
        pass
    room = get_object_or_404(Room, id=pk)
    room_message = room.message_set.all()
    participants = room.participants.all()
    
    if request.method == 'POST':
        message = request.POST.get('message')
        
        new_message = Message.objects.create(
            user=request.user, room=room, body=message
        )
        room.participants.add(request.user)
        return redirect('rooms', pk=room.pk)
        
    
    context = {'room': room, 'room_message': room_message, 'participants': participants}
    return render(request, 'Base/room.html', context)


@login_required(login_url='home')
def room_form(request):
    if request.user.is_authenticated:
        if request.user.first_name == '' and request.user.last_name == '':
            return redirect('edit_user')
    else:
        pass
    
    form = RoomForm()
    topic = Topic.objects.all()
    if request.method == 'POST':
        my_topic = request.POST.get('topic')
        topics, created = Topic.objects.get_or_create(name=my_topic)
        Room.objects.create(
            host = request.user,
            name=request.POST.get('name'),
            topic = topics,
            description=request.POST.get('description')
        )
        return redirect('home')
        
    context = {'form': form, 'topic': topic}
    return render(request, 'Base/room_form.html', context)


@login_required(login_url='home')
def room_update(request, name):
    if request.user.is_authenticated:
        if request.user.first_name == '' and request.user.last_name == '':
            return redirect('edit_user')
    else:
        pass
    room = Room.objects.get(name=name)
    form = RoomForm(instance=room)
    topic = Topic.objects.all()
    
    if request.user != room.host:
        messages.error(request, 'You are not allowed here')
        return redirect('home')
    
    if request.method == 'POST':
        my_topic = request.POST.get('topic')
        topics, created = Topic.objects.get_or_create(name=my_topic)
        room.name=request.POST.get('name')
        room.topic = topics
        room.description=request.POST.get('description')
        room.save()
        
        return redirect("rooms", pk=room.pk)
    
    context = {'form': form, 'room': room, 'topic': topic}
    return render(request, 'Base/room_form.html', context)


@login_required(login_url='home')
def room_delete(request, name):
    if request.user.is_authenticated:
        if request.user.first_name == '' and request.user.last_name == '':
            return redirect('edit_user')
    else:
        pass
    
    room = Room.objects.get(name=name)
    
    if request.user != room.host:
        messages.error(request, 'You are not allowed to delete here')
        return redirect('home')
    
    if request.method == 'POST':
        room.delete()
        return redirect("home")
    
    context = {'obj': room}
    return render(request, 'Base/room_form.html', context)


@login_required(login_url='home')
def room_message_delete(request, pk):
    if request.user.is_authenticated:
        if request.user.first_name == '' and request.user.last_name == '':
            return redirect('edit_user')
    else:
        pass
    
    message = Message.objects.get(id=pk)
    data = message
    
    if request.method == 'POST':
        # print(Message.objects.get(room=data.room))
        
        
        message.delete()
        
        
        new_list = []
        for items in Message.objects.filter(room=data.room.id):
            new_list.append(items.user)
            # if items.user.username == request.user:
            #     new_list.append(items.user)
                
        print(new_list)
        if request.user in new_list:
            print(f'{request.user.username} found')
        else:
            message.room.participants.remove(message.user)
        # else:
        #     print('no message found')
        
        
        
        return redirect("rooms", pk=message.room.pk)
    
    context = {'obj': message}
    return render(request, 'Base/room_form.html', context)


@login_required(login_url='login_user')
def edit_user(request):
    user = request.user
    
    form = UserForm(instance=user)
    
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile', pk=user.pk)
    context = {
        'form': form
    }
    return render(request, 'Base/edit-user.html', context)


def topics(request):
    if request.user.is_authenticated:
        if request.user.first_name == '' and request.user.last_name == '':
            return redirect('edit_user')
    else:
        pass
    
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topic = Topic.objects.filter(name__icontains=q)
    context = {'topic': topic}
    return render(request, 'Base/topics.html', context)


# def activity(request):
#     message = Message.objects.all()[:4]
#     context = {'message': message }
#     return render(request, 'base/activity.html', context)

from django.views.generic import ListView, DetailView, UpdateView, DeleteView

class ActivityView(ListView):
    model = Message
    queryset = Message.objects.all()
    template_name = "base/activity.html"
    context_object_name = "message"