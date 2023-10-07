from django.shortcuts import render,redirect
from .models import *
from django.http import HttpResponse
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.contrib import messages

from django.contrib.auth.models import User


# Create your views here.
def recipes(request):
    if request.method == "POST":
        
        data = request.POST
        recipe_name = data.get('recipe_name')
        recipe_desp = data.get('recipe_desp')
        recipe_image = request.FILES.get('recipe_image')
        print(recipe_name)
        print(recipe_desp)
        print(recipe_image)

        Recipe.objects.create(
            recipe_name = recipe_name,
            recipe_desp = recipe_desp,
            recipe_image = recipe_image,
        ) 

        return redirect('/recipes/')

    queryset = Recipe.objects.all()

    if request.GET.get('search'):
        # print(request.GET.get('search'))
        queryset =queryset.filter(recipe_name__icontains = request.GET.get('search'))

        
    context= {'recipes': queryset}

    return render(request, 'recipes.html', context)
    
def delete_recipe(request, id):
    # print(id)
    queryset = Recipe.objects.get(id=id)
    queryset.delete()

    return redirect('/recipes/')

def update_recipe(request, id):
    # print(id)
    queryset = Recipe.objects.get(id=id)

    if request.method == "POST":
        data = request.POST

        recipe_name = data.get('recipe_name')
        recipe_desp = data.get('recipe_desp')
        recipe_image = request.FILES.get('recipe_image')

        queryset.recipe_name= recipe_name
        queryset.recipe_desp= recipe_desp

        if recipe_image:
            queryset.recipe_image=recipe_image
        queryset.save()
        return redirect('/recipes/')

    context = {'recipe': queryset}

    return render(request, "update_recipes.html", context)

def login_page(request):

    return render(request, "login.html")

from django.contrib import messages

def register(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            # Check if the username already exists
            existing_user = User.objects.get(username=username)
            messages.error(request, "User Already Exists")

        except User.DoesNotExist:
            # If the username doesn't exist, create a new user
            user = User.objects.create(
                first_name=first_name,
                last_name=last_name,
                username=username,
            )
            user.set_password(password)
            user.save()
            messages.success(request, "Account Created Successfully")

        return redirect("/register/")

    return render(request, "register.html")
