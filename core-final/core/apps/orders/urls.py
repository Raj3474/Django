from django.urls import path

from . import views

app_name = 'orders'  # to connect to the <project>/urls.py namespace


urlpatterns = [
    path('add/', views.add, name='add'),
    # path('my_orders/', views.orders, name='my_orders'),
]