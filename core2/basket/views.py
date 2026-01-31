from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from store.models import Product

from .basket import Basket

# Create your views here.

def basket_summary(request):
    basket = Basket(request)
    return render(request, 'basket/summary.html', {'basket': basket})

def basket_add(request):
    basket = Basket(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('productid'))
        product_qty = int(request.POST.get('productqty'))
        product = get_object_or_404(Product, id=product_id)
        basket.add(product=product, product_qty=product_qty)

        basketqty = basket.__len__()
        response = JsonResponse({'qty': basketqty})
        # response = JsonResponse({'test': 'data'})
        return response

def basket_delete(request):
    basket = Basket(request)
    if request.POST.get('action') == 'post':
        print(request.POST.get('productid'))
        product_id = int(request.POST.get('productid'))
        basket.delete(productid=str(product_id))


        basketqty = basket.__len__()
        baskettotal = basket.get_total_price()
        response = JsonResponse({'qty': basketqty, 'total': baskettotal})

        return response

def basket_update(request):
    basket = Basket(request)
    if request.POST.get('action') == 'post':
        print('in update if')
        product_id = int(request.POST.get('productid'))
        product_qty = int(request.POST.get('productqty'))

        print(product_id)
        print(product_qty)
        basket.update(productid=str(product_id), qty=str(product_qty))

        basketqty = basket.__len__()
        print(basketqty)
        baskettotal = basket.get_total_price()
        response = JsonResponse({'qty': basketqty, 'total': baskettotal})
        return response
