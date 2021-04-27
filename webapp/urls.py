from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),

    path('accounts/register/', views.register, name="register"),
    path('order/', views.order, name="order"),
    path('order/drink/', views.orderDrink, name="orderDrink"),
    path('history/', views.history, name="history"),
    path('status/', views.status, name="status"),
    path('recipe/', views.recipes, name="recipes"),
    path('recipe/register', views.recipeRegister, name="recipeRegister"),
    path('recipe/<int:id>/delete', views.recipeDelete, name='recipeDelete'),
]