from django.urls import path
from . import views

app_name = 'store'  # to connect to the <project>/urls.py namespace


urlpatterns = [
    path('', views.all_products, name='all_products'),
    path('book/<slug:slug>/', views.product_detail, name='product_detail'),
    path('search/<slug:category_slug>/', views.category_list, name='category_list')
]