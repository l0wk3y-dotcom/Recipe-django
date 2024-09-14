from django.contrib.auth.middleware import auser
from django.shortcuts import render, redirect
from .models import Recipe
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

@login_required(login_url="/login")
def add_recipe(request):
    if request.method=="POST":
        data=request.POST
        recipe_name=data.get("recipe_name")
        recipe_description = data.get("recipe_description")
        image=request.FILES.get("image")
        Recipe.objects.create(recipe_name=recipe_name,
                               recipe_description=recipe_description,
                               image=image)
        return redirect("/add_recipe/")

    return render(request,"add_recipe.html")


@login_required(login_url="/login")
def recipe_home(request):
    recipies=Recipe.objects.all()
    search_term=request.GET.get('search_term')
    if search_term:
        recipies=Recipe.objects.filter(Q(recipe_name__icontains=search_term) | Q(recipe_description__icontains=search_term))
    context={"recipies":recipies}
    return render(request,'recipe_home.html',context)

def delete_recipe(request,id):
    recipe=Recipe.objects.get(id=id)
    recipe.delete()
    return redirect('/')

def update_recipe(request,id):
    recipe=Recipe.objects.get(id=id)
    context={"recipe":recipe}
    if request.method=='POST':
        data=request.POST
        recipe.recipe_name=data.get("recipe_name")
        recipe.recipe_description = data.get("recipe_description")
        image = request.FILES.get('image')
        if image:
            recipe.image=image
        recipe.save()
        return redirect(f'/update_recipe/{id}')
    return render(request,'update_recipe.html',context)


def login_page(request):
    if request.method == 'POST':
        data = request.POST
        username = data.get('username')
        password = data.get('password')

        # Check if the username exists
        if not User.objects.filter(username=username).exists():
            messages.add_message(request, messages.ERROR, "Username not found!")
            return redirect('/login')

        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)  # Correct this line
            return redirect('/')
        else:
            messages.add_message(request,messages.ERROR,f"credentials are incorrect {username} | {password}")
            return redirect('/login')
            # Log the user in
    return render(request, 'login.html')

def register(request):
    if request.method=='POST':
        data=request.POST
        username=data.get('username')
        user_exists=User.objects.filter(username=username)
        if user_exists:
            messages.add_message(request, messages.ERROR, "username already exists")
            return redirect('/register')
        password = data.get('password')
        fname=data.get('fname')
        lname=data.get('lname')
        my_user=User(username=username,
                                 first_name=fname,
                                 last_name=lname)
        my_user.set_password(password)
        my_user.save()
        messages.add_message(request, messages.INFO, "User created succesfully!")
    return render(request,'register.html')

def logout_page(request):
    logout(request)
    return redirect('/login')