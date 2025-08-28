from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from .forms import RegisterForm
from .models import UserData,ChatMessages
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

    return render(request, "Yoyo.html")



def save_message(request):
    """ Save chat messages (sent or received) """
    if request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))

        user_id = request.session.get("user_id")
        if not user_id:
            return JsonResponse({"error": "Not logged in"}, status=403)

        try:
            user = UserData.objects.get(id=user_id)
        except UserData.DoesNotExist:
            return JsonResponse({"error": "User not found"}, status=404)

        msg_type = data.get("message_type", "sent")
        content = data.get("content")

        message = ChatMessages.objects.create(
            user=user,
            message_type=msg_type,
            content=content
        )

        return JsonResponse({"success": True, "message_id": message.id})

    return JsonResponse({"error": "Invalid request"}, status=400)


def get_messages(request):
    """ Fetch all previous messages for logged-in user """
    user_id = request.session.get("user_id")
    if not user_id:
        return JsonResponse({"error": "Not logged in"}, status=403)

    messages = ChatMessages.objects.filter(user_id=user_id).order_by("timestamp").values("message_type", "content", "timestamp")
    return JsonResponse(list(messages), safe=False)


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