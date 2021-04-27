from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone

from django.apps import apps

#Rest Framework
from rest_framework.response import Response
from rest_framework.decorators import api_view

#Rest
from webapp.forms import RegisterForm, CoffeeRecipeForm
from webapp.models import CoffeeRecipe, CoffeeOrder


# Create your views here.
from django.views.decorators.csrf import csrf_exempt

#apps.get_app_config('webapp').receive.put("Hello World")

def index(request):
    return render(request, 'index.html')

def register(request):
    if request.method == 'POST':

        form = RegisterForm(request.POST)
        # Check if the form is valid:
        if form.is_valid():
            newUser = User.objects.create_user(form.cleaned_data['username'], 
                                            form.cleaned_data['email'], 
                                            form.cleaned_data['password1'], 
                                            first_name = form.cleaned_data['first_name'], 
                                            last_name = form.cleaned_data['last_name'])
            login(request, newUser)
            return HttpResponseRedirect(reverse('index'))

    # If this is a GET (or any other method) create the default form.
    else:
        form = RegisterForm()

    context = {
        'form': form,
        }

    return render(request, 'registration/register.html', context)

@login_required
def recipeRegister(request):
    if not request.user.is_superuser:
        return HttpResponseRedirect(reverse('index'))

    if request.method == 'POST':
        form = CoffeeRecipeForm(request.POST, request.FILES)
        print(form.errors)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('recipes'))

    else:
        form = CoffeeRecipeForm()

    context = {
        'form': form,
        }

    return render(request, 'recipes/register.html', context)


@login_required
def order(request):

    if request.method == 'POST':
        pass

    else:
        coffee = CoffeeRecipe.objects.all()

    context = {
        'coffee': coffee,
        }

    return render(request, 'order.html', context)

@api_view(["POST"])
def orderDrink(request):
    answer = {'success':False, 'credits':0}
    try:
        recipe = CoffeeRecipe.objects.get(pk=request.data['pk'])
        if(request.user.coffeeuser.credits < recipe.cost):
            return Response(answer)
        
        #
        # Code to place Order goes here
        #
        id = request.user.coffeeuser.pk
        order_try = {'user':id, 
                    'chocolate':recipe.chocolate, 
                    'coffee':recipe.coffee, 
                    'milk':recipe.milk}
        print("sending order")
        apps.get_app_config('webapp').receive.put(order_try)
        result = None
        while 1:
            result = apps.get_app_config('webapp').send.get()
            if result['user'] == id:
                break
            else:
                apps.get_app_config('webapp').send.put(result)
        if not result['status']:
            answer['success'] = False
            answer['credits'] = 0
            return Response(answer)


        # Assuming success
        order = CoffeeOrder(user=request.user.coffeeuser, recipe=recipe, time=timezone.now())
        order.save()
        answer['success'] = True
        answer['credits'] = recipe.cost

        request.user.coffeeuser.credits -= recipe.cost
        request.user.coffeeuser.save()
    except CoffeeRecipe.DoesNotExist:
        answer['success'] = False
        answer['credits'] = 0

    return Response(answer)

@login_required
def history(request):
    if request.user.is_superuser:
        orders = CoffeeOrder.objects.all()
        context = {
            'orders': orders
        }
        return render(request, 'historyAdmin.html', context)

    orders = CoffeeOrder.objects.filter(user=request.user.coffeeuser)
    context = {
        'orders': orders
    }
    return render(request, 'history.html', context)

@login_required
def status(request):
    # Code to request status from machine
    # Goes here
    context = {'status':0}
    return render(request, 'status.html', context)

@login_required
def recipes(request):
    if not request.user.is_superuser:
        return HttpResponseRedirect(reverse('index'))
    
    recipes = CoffeeRecipe.objects.all()
    
    context = {
        'recipes': recipes,
    }

    return render(request, 'recipes/main.html', context)

@login_required
def recipeDelete(request, id):
    if not request.user.is_superuser:
        return HttpResponseRedirect(reverse('index'))

    CoffeeRecipe.objects.get(pk=id).delete()

    return HttpResponseRedirect(reverse('recipes'))