from django.shortcuts import render, redirect, get_object_or_404
from django.template import loader

# Create your views here.
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.forms.models import model_to_dict
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.utils import timezone
from django.contrib.auth.hashers import make_password


from .models import ToDoItem, Event
from .forms import LoginForm, AddTaskForm, UpdateTaskForm, RegisterForm, AddEventForm, UpdateEventForm, UpdateUserForm

def index(request):
    # todoitem_list = ToDoItem.objects.all()
    todoitem_list = ToDoItem.objects.filter(user_id=request.user.id)
    event_list = Event.objects.filter(user_id=request.user.id)

    context={
        'todoitem_list': todoitem_list,
        'event_list': event_list,
        "user":request.user
    }
    return render(request, "todolist/index.html", context)

    # todoitem_obj = ToDoItem.objects.get(pk=todoitem_id)
    # context = {"todoitem": model_to_dict(todoitem_obj)}
    # return render(request, "todolist/todoitem.html", context)

    #response= "You are viewing the details of %s"
    #return HttpResponse(response % todoitem_id)

def update_user(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')

        if request.user.check_password(current_password):
            request.user.first_name = first_name
            request.user.last_name = last_name
            if new_password:
                request.user.set_password(new_password)
            request.user.save()
            update_session_auth_hash(request, request.user)  # Keeps user logged in
            messages.success(request, "Profile updated successfully.")
            # return redirect("todolist:index")  # Redirect to profile page or dashboard
        else:
            messages.error(request, "Current password is incorrect.")

    return render(request, "todolist/update_user.html")

# @login_required
# def change_password(request):
#     is_user_authenticated = False  # Track if the password was changed

#     if request.method == 'POST':
#         current_password = request.POST.get('current_password')
#         new_password = request.POST.get('new_password')

#         if request.user.check_password(current_password):
#             request.user.set_password(new_password)
#             request.user.save()
#             update_session_auth_hash(request, request.user)  # Keeps user logged in
#             is_user_authenticated = True
#             messages.success(request, "Password changed successfully.")
#         else:
#             messages.error(request, "Current password is incorrect.")

#     context = {
#         "is_user_authenticated": is_user_authenticated
#     }
#     return render(request, "todolist/change_password.html", context)

def login_view(request):
    context={}
    if request.method=="POST":
        form = LoginForm(request.POST)
        if form.is_valid() == False:
            form = LoginForm()
        else:
            username=form.cleaned_data['username']
            password=form.cleaned_data['password']
            user=authenticate(username=username, password=password)
            context = {
                "username": username,
                "password": password,
            }
            if user is not None:
                login(request, user)
                return redirect("todolist:index")
            else:
                context={
                "error": True
                }
    return render(request, "todolist/login.html", context)


def logout_view(request):
    logout(request)
    return redirect("todolist:index")  # Changed to match login URL name

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.password = make_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, "Registration successful.")
            return redirect("todolist:login")
        else:
            messages.error(request, "Registration failed. Please check the form.")
    else:
        form = RegisterForm()
    
    return render(request, "todolist/register.html", {"form": form})

def todoitem(request, todoitem_id):
    todoitem=get_object_or_404(ToDoItem, pk=todoitem_id)
    return render(request, "todolist/todoitem.html", model_to_dict(todoitem))

def add_task(request):
    context = {}
    
    if request.method == "POST":
        form = AddTaskForm(request.POST)
        if form.is_valid() == False:
            form = AddTaskForm()
        else:
            task_name = form.cleaned_data["task_name"]
            description = form.cleaned_data["description"]
            
            if not ToDoItem.objects.filter(task_name=task_name).exists():
                ToDoItem.objects.create(
                    task_name=task_name,
                    description=description,
                    date_created=timezone.now(), 
                    user_id=request.user.id
                )
                return redirect("todolist:index")
            else:
                context = {"error": True}
    
    return render(request, "todolist/add_task.html", context)



def update_task(request):
    todoitem:ToDoItem.objects.filter(pk=todoitem_id)

    context={
        'user' : request.user,
        'todoitem_id' : todoitem_id,
        'task_name' : todoitem[0].task_name,
        'description' : todoitem[0].description,
        'status' : todoitem[0].status,

    }

    if request.method== 'POST':
        form=UpdateTaskForm(request.POST)

        if form.is_valid()==False:
            form = UpdateTaskForm()

        else:
            task_name=form.cleaned_data["task_name"]
            description=form.cleaned_data["description"]
            status=form.cleaned_data["status"]

            if todoitem:
                todoitem[0].task_name = task_name
                todoitem[0].description = description
                todoitem[0].status = status
                todoitem[0].save()
                return redirect('todolist:index')
            else:
                context = {
                    "error" :True
                }
    return render(request, 'todolist/update_task.html', context)

def delete_task(request):
    todoitem:ToDoItem.objects.filter(pk=todoitem_id).delete()
    return redirect("todolist:index")

def event(request, event_id):
    event=get_object_or_404(Event, pk=event_id)
    return render(request, "todolist/event.html", model_to_dict(event))

def add_event(request):
    context = {}
    
    if request.method == "POST":
        form = AddEventForm(request.POST)
        if form.is_valid() == False:
            context["form"] = form
            return render(request, "todolist/add_event.html", context)
        else:
            event_name = form.cleaned_data["event_name"]
            description = form.cleaned_data["description"]
            event_date = form.cleaned_data["event_date"]
            
            if not Event.objects.filter(event_name=event_name).exists():
                Event.objects.create(
                    event_name=event_name,
                    description=description,
                    event_date=event_date, 
                    user_id=request.user.id
                )
                return redirect("todolist:index")
            else:
                context = {"error": True}
    
    return render(request, "todolist/add_event.html", context)


# temporary update event
def update_event(request):
    event:Event.objects.filter(pk=event_id).delete()
    return redirect("todolist:index")


def delete_event(request):
    event:Event.objects.filter(pk=event_id).delete()
    return redirect("todolist:index")

