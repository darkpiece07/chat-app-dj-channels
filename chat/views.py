from django.shortcuts import render, redirect
from .models import Group , Chat

def index(request):
    if request.method == "POST":
        room_name = request.POST["room_name"]
        group = Group.objects.filter(name = room_name).first()

        if group is None:
            group = Group(name = room_name)
            group.save()
            print("new group created : ", group.name)

    available_rooms = Group.objects.all()
    context = {"available_rooms": available_rooms}
    return render(request, 'chat/index.html', context)


def room(request, room_name):
    group = Group.objects.filter(name = room_name).first()
    context = {}
    if group:
        chats = Chat.objects.filter(group = group)
        context = {"chats": chats}
        
    else:
        new_group = Group(name = room_name)
        new_group.save()

    available_rooms = Group.objects.all()
    context["available_rooms"] = available_rooms
    context["room_name"] = room_name

    return render(request, 'chat/chat.html', context)


# def addRoom(request):
#     print("aaya h request")
#     if request.method == "POST":
#         room_name = request.POST["room_name"]
#         print(room_name)
#         group = Group.objects.filter(name = room_name)

#         if group is None:
#             group = Group(name = room_name)
#             group.save()

#             return render(request, 'chat/chat.html', context = {"room_name": room_name})
        
#         return render(request, 'chat/chat.html', context = {"room_name": room_name})
    
#     return render(request, 'chat/index.html')
        