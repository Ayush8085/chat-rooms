from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .models import Room, Message

# Create your views here.

@login_required
def rooms(request):
    rooms = Room.objects.all()

    context = {'rooms': rooms}
    return render(request, 'rooms/rooms.html', context)

@login_required
def room(request, pk):
    room = Room.objects.get(id=pk)
    messages = Message.objects.filter(room=room)

    context = {'room': room, 'messages': messages}
    return render(request, 'rooms/room.html', context)

@login_required
def createRoom(request):

    if request.method == "POST":
        Room.objects.create(
            name = request.POST['roomname']
        )
        return redirect('rooms')
    
    return render(request, 'rooms/create-room.html')