from django.shortcuts import render, redirect ,get_object_or_404
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from .forms import RegisterForm
from .models import UserData,Message,Chat
from django.contrib.auth.hashers import check_password
import json
from django.http import JsonResponse


def register_yoyo(request):
    # If already logged in → go to home
    if request.session.get("user_id"):
        return redirect("home")

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.password = make_password(form.cleaned_data["password"])  # hash password
            user.save()
            messages.success(request, "Registration successful! Please login.")
            return redirect("login")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = RegisterForm()
    return render(request, "Register.html", {"form": form})


def login_yoyo(request):
    # If already logged in → go to home
    if request.session.get("user_id"):
        return redirect("home")

    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user = UserData.objects.get(email=email)
            if check_password(password, user.password):
                # Set session to log the user in
                request.session["user_id"] = user.id
                request.session["user_name"] = user.name
                messages.success(request, f"Welcome back, {user.name}!")
                return redirect("home")
            else:
                messages.error(request, "Incorrect password.")
        except UserData.DoesNotExist:
            messages.error(request, "Email not registered.")

    return render(request, "Login.html")


def logout_yoyo(request):
    request.session.flush()  
    return redirect("login")  


def home_yoyo(request):
    # If not logged in → redirect to login
    if not request.session.get("user_id"):
        return redirect("login")

    user = get_object_or_404(UserData, id=request.session["user_id"])
    chats = Chat.objects.filter(user=user).order_by("-created_at")

    return render(request, "Yoyo.html", {
        "user": user,
        "chats": chats,
    })
    
def new_chat(request):
    if not request.session.get("user_id"):
        return redirect("login")

    user = get_object_or_404(UserData, id=request.session["user_id"])
    chat = Chat.objects.create(user=user, title="New Chat")

    return redirect("chat_detail", chat_id=chat.id)


def chat_detail(request, chat_id):
    if not request.session.get("user_id"):
        return redirect("login")

    user = get_object_or_404(UserData, id=request.session["user_id"])
    chat = get_object_or_404(Chat, id=chat_id, user=user)  # only this user’s chats

    if request.method == "POST":
        text = request.POST.get("message")
        if text:
            # Save user’s message
            Message.objects.create(chat=chat, sender="user", text=text)
            # Dummy bot reply
            Message.objects.create(chat=chat, sender="bot", text="🤖 YOYO: " + text[::-1])
        return redirect("chat_detail", chat_id=chat.id)

    return render(request, "Yoyo.html", {
        "user": user,
        "chats": user.chats.order_by("-created_at"),
        "current_chat": chat,
        "messages": chat.messages.all(),
    })



def brain_yoyo(request):
    return render(request,"Brainstormer.html")

def Career_guide_yoyo(request):
    return render(request,"Career_guide.html")

def Chess_champ_yoyo(request):
    return render(request,"Chess_champ.html")

def Coding_partner_yoyo(request):
    return render(request,"Coding_partner.html")

def Explore_Gem_yoyo(request):
    return render(request,"Explore_Gem.html")

def ForgotPassword_yoyo(request):
    return render(request,"ForgotPassword.html")

def Learning_coach_yoyo(request):
    return render(request,"Learning_coach.html")

def NewGem_yoyo(request):
    return render(request,"Learning_coach.html")

def Public_Links_yoyo(request):
    return render(request,"Public_Links.html")

def SavedInfo_yoyo(request):
    return render(request,"SavedInfo.html")

def Search_yoyo(request):
    return render(request,"Search.html")

def Upgrad_yoyo(request):
    return render(request,"Upgrad.html")

def Writing_editor_yoyo(request):
    return render(request,"Writing_editor.html")

def Explore_Gem_yoyo(request):
    return render(request,"Explore_Gem.html")