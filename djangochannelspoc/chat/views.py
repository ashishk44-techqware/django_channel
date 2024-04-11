from django.shortcuts import *
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from chat.models import *
from chat.forms import *
# Create your views here.


def logins(request):
    if request.user.is_authenticated:
        return redirect('home')
    print('check')
    form = AuthenticationForm(data=request.POST or None)
    if request.method=='POST':
        if form.is_valid():
            print('form')
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            print(user,'user')
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                print('error')
                messages.error(request, "Username or password incorrect!")
                return redirect('login')
        else:
            messages.error(request, form.errors)
            return redirect('login')
    data = {
        'form': form
    }
    return render(request,'login.html',data)


def signup(request):
    if request.user.is_authenticated:
        return redirect('home')
    form = RegisterForm(request.POST or None)
    if request.method=='POST':
        if form.is_valid():
            form.save()
            messages.success(request, "Register Successfully!")
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
            if user is not None:
                login(request, user)
                return redirect('home')
        else:
            messages.error(request,form.errors)
            return redirect('signup')
    data = {
        'form':form
    }
    return render(request,'signup.html',data)


@login_required(login_url='login')
def logouts(r):
    logout(r)
    return redirect('login')


@login_required(login_url='login')
def home(request):
    return render(request,'home.html')


@login_required(login_url='login')
def autosuggest(request):
    user = User.objects.get(username=request.user.username)
    search = request.GET.get('search', None)
    results = []
    if search is not None:
        results = User.objects.filter(Q(username__istartswith=search)|Q(first_name__istartswith=search)).exclude(id=user.id).values('id','username','first_name','last_name')
    return JsonResponse(list(results), safe=False)


@login_required(login_url='login')
def chat(request,to_user_id):
    try:
        sender = User.objects.get(username=request.user.username)
        receiver = User.objects.get(id=to_user_id)

        room = ChatRoom.objects.filter(Q(sender=sender,receiver=receiver)|Q(sender=receiver,receiver=sender))
        if room.exists():
            print("room inside")
            message = Message.objects.filter(room=room.first()).order_by('doc')
            return render(request, 'chat.html', {'room_name': room.first().room_name,'message':message,'sender':sender,'receiver':receiver})
        else:
            message = Message.objects.none()
            print(message,"message")
            room = ChatRoom.objects.create(room_name=f"room-{sender.id}-{to_user_id}",sender=sender,receiver=receiver)
            print(room,"room")
            return render(request, 'chat.html', {'room_name': room.room_name,'message':message,'sender':sender,'receiver':receiver})
    except Exception as e:
        print(e)
        messages.success(request, e)
        return redirect('home')
