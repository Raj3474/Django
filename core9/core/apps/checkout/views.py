import json
import os

import stripe

from core.apps.basket.basket import Basket
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect

from .models import DeliveryOptions
from core.apps.account.models import Address
from core.apps.orders.views import payment_confirmation

# Create your views here.
@login_required
def deliverychoices(request):
    deliveryoptions = DeliveryOptions.objects.filter(is_active=True).order_by('order')

    return render(request, "checkout/delivery_choices.html", {
        "deliveryoptions": deliveryoptions
    })


@login_required
def basket_update_delivery(request):
    basket = Basket(request)

    if request.POST.get("action") == "post":
        delivery_option = int(request.POST.get("deliveryoption"))
        delivery_type = DeliveryOptions.objects.get(id=delivery_option)

        updated_total_price = basket.basket_update_delivery(delivery_type.delivery_price)


        session = request.session
        if "purchase" not in session:
            session["purchase"] = {
                "delivery_id": delivery_type.id,
            }
        else:
            session["purchase"]["delivery_id"] = delivery_type.id
            session.save()

    response = JsonResponse({
        "total": updated_total_price, "delivery_price": delivery_type.delivery_price
    })
    return response


@login_required
def delivery_address(request):

    session = request.session
    if "purchase" not in request.session:
        messages.success(request, "Please select a delivery option")
        return HttpResponseRedirect(request.META["HTTP_REFERER"])

    addresses = Address.objects.filter(customer=request.user).order_by("-default")

    print(len(addresses))
    if len(addresses) != 0:
        if "address" not in request.session:
            session["address"] = {"address_id": str(addresses[0].id)}
        else:
            session["address"]["address_id"] = str(addresses[0].id)
            session.modified = True

    return render(request, "checkout/delivery_address.html", {
        "addresses": addresses
    })


@login_required
def payment_selection(request):

    session = request.session
    if "address" not in request.session:
        messages.success(request, "Please select address option")
        return HttpResponseRedirect(request.META["HTTP_REFERER"])

    basket = Basket(request)

    total = str(basket.get_total_price()) # returns string with decimal

    # we need to send price without the decimal
    total = total.replace('.', '')
    total = int(total)

    stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')
    intent = stripe.PaymentIntent.create(
        amount=total,
        currency='inr',
        description='This is for testing pupose',
        metadata={'userid': request.user.id}
    )

    address_id = session["address"]["address_id"]
    address = Address.objects.get(id=address_id)

    print(address)

    return render(request, "checkout/payment_selection.html", {
        'address': address,
        'client_secret': intent.client_secret,
        'STRIPE_PUBLISHABLE_KEY': os.environ.get('STRIPE_PUBLISHABLE_KEY')
    })


@login_required
def payment_complete(request):

    if request.method == 'POST':
        payment_data = request.POST.dict()
        if payment_data['result[paymentIntent][status]'] == 'succeeded':
            client_secret = payment_data['result[paymentIntent][client_secret]']
            payment_confirmation(client_secret)
            return HttpResponse(status=200)
        else:
            return HttpResponse(status=400)

@login_required
def payment_successful(request):
    basket = Basket(request)
    basket.clear()
    return render(request, 'checkout/payment_successful.html')
