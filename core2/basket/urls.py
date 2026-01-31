from django.urls import path

from . import views

app_name = 'basket'  # to connect to the <project>/urls.py namespace


urlpatterns = [
    path('', views.basket_summary, name='basket_summary'),
    path('add/', views.basket_add, name='basket_add'),
    path('delete/', views.basket_delete, name='basket_delete'),
    path('update/', views.basket_update, name='basket_update')
#    path('shop/<slug:category_slug>/', views.category_list, name='category_list')
]