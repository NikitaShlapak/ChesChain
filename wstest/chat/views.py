from django.shortcuts import render, redirect

from chat.forms import CustomUserCreationForm
from chat.models import BoardRoom, CustomUser
from django.contrib.auth import logout as django_logout

def logout(request):
    django_logout(request)
    return redirect('index')

def index(request):
    board = [str(a) + str(b) for a in reversed(range(1, 9)) for b in range(1, 9)]
    rooms = BoardRoom.objects.all()
    data = {
        'rooms':rooms,
        'board':board
    }
    return render(request, "chat/index.html",context=data)

def room(request, board_name):
    board = [str(a)+str(b) for a in reversed(range(1,9)) for b in range(1,9)]
    print(board)
    return render(request, "chat/room.html", {"room_name": board_name})

def board(request, board_name):
    board = [str(a) + str(b) for a in reversed(range(1, 9)) for b in range(1, 9)]
    room = BoardRoom.objects.get(name=board_name)
    print(BoardRoom)
    data={
        'board':board,
        'board_name':board_name,
        'room': room,
    }
    return render(request, "chat/board.html", context=data)

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(data=request.POST)
        if form.is_valid():
            #user = form.cleaned_data
            user = {
                'username':form.cleaned_data['username'],
                'email':form.cleaned_data['email'],
                'password': form.cleaned_data['password1'],
            }
            print(user)
            try:
                new_user = CustomUser.objects.create(**user)

                print(new_user)
                new_user.set_password(new_user.password)
                new_user.save()

                return redirect('index')
            except:
                form.add_error(None, 'Error')
    else:
        form = CustomUserCreationForm
    data ={
        'form':form
    }

    return render(request, 'chat/register.html', context=data)
