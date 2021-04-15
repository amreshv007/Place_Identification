from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import ImgPlace, NamesPlace
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage

def index(request):
    if request.method == "POST" and request.FILES['image']:
        print("===================")
        # print(request.FILES)
        username = request.user.username
        print('user=', username)
        user1 = User.objects.get(username=username)
        print('user1=', user1)
        im = request.FILES['image']
        fs = FileSystemStorage()
        filename = fs.save(im.name, im)
        uploaded_file_url = fs.url(filename)
        name = request.POST['place_name']
        image_place = ImgPlace(user=user1, place=name, image_url=uploaded_file_url)
        image_place.save()
        all_places = NamesPlace.objects.all()
        k = 0
        for place in all_places:
            if(place.names == name):
                print(place.names)
                k = 1
                break
        if(k==0):
            places = NamesPlace(names=name)
            places.save()
            messages.info(request, "Data Saved Successfully!")
    names = NamesPlace.objects.all()
    imges = ImgPlace.objects.all()
    return render(request,"home.html", {'Places': names, 'imges': imges, 'i': 6})

def login(request):
    context = {}
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = auth.authenticate(username=username,password=password)
        print(user,"ssss")
        if user is not None:
            auth.login(request,user)
            return redirect("/persius")
        else:
            messages.info(request, "Incorrect! Username or Password!")
            return redirect("/persius/login")
    else:
        if request.user.is_authenticated:
            return redirect("/persius")
        else:
            return render(request,"login.html",context)

def signup(request):
    context = {}
    if request.method == "POST":
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        email = request.POST["email"]
        username = request.POST["username"]
        password1 = request.POST["password"]
        password2 = request.POST["re_password"]
        if password1 == password2:
            if User.objects.filter(username=username).exists():
                print("User already exist!")
                messages.info(request,"User already exist!")
                return redirect("/persius/signup")
            else:
                user = User.objects.create_user(username=username,password=password1,email=email,first_name=first_name,last_name=last_name)
                user.save()
                print("User created!")
                messages.info(request, "User created!")
                return redirect("/persius/login")
        else:
            messages.info(request, "Password Mismatched!")
            return HttpResponseRedirect(request.path_info)
    else:
        if request.user.is_authenticated:
            return redirect("/persius")
        else:
            return render(request,"signup.html",context)

@login_required(login_url='/persius/login')
def logout(request):
    auth.logout(request)
    return redirect("/persius/")

@login_required(login_url='/persius/login')
def place(request):
    if request.method == "POST":
        select_place = request.POST['agent_id']
        url = request.POST['url']
        print('url=', url)
        print('select_place=', select_place)
        print(request.user.username)
        Img_place = ImgPlace.objects.get(image_url=url)
        if Img_place.place == select_place:
            if Img_place.guess_by == "":
                Img_place.guess_by = request.user.first_name
                Img_place.save()
        print(Img_place.guess_by)
    return redirect("/persius")