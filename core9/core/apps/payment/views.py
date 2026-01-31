import json
import os

import stripe

from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render

from django.views.generic.base import TemplateView

from core.apps.basket.basket import Basket
from core.apps.orders.views import payment_confirmation

# Create your views here.
def order_placed(request):
    basket = Basket(request)
    basket.clear()

    return render(request, 'payment/orderplaced.html')

class Error(TemplateView):
    template_name = 'payment/error.html'


@login_required
def BasketView(request):

    basket = Basket(request)
    total = str(basket.get_total_price()) # returns string with decimal

    # we need to send price without the decimal
    total = total.replace('.', '')
    total = int(total)

    # As per Indian regulations, export transactions require a description.
    # More info here: https://stripe.com/docs/india-exports

    stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')
    intent = stripe.PaymentIntent.create(
        amount=total,
        currency='inr',
        description='This is for testing pupose',
        metadata={'userid': request.user.id}
    )

    return render(request, 'payment/payment_form.html', {
        'client_secret': intent.client_secret,
        'STRIPE_PUBLISHABLE_KEY': os.environ.get('STRIPE_PUBLISHABLE_KEY')
    })




# this view is for the integrating the stripe webhook cli,
@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    event = None

    try:
        event = stripe.Event.construct_from(
            json.loads(payload), stripe.api_key
        )
    except ValueError as e:
        print(e)
        return HttpResponse(status=400)

    # Handle the event
    if event.type == 'payment_intent.succeeded':
        payment_confirmation(event.data.object.client_secret)

    else:
        print('Unhandled event type {}'.format(event.type))

    return HttpResponse(status=200)

def confirm_payment(request):
    if request.method == 'POST':
        payment_data = request.POST.dict()
        if payment_data['result[paymentIntent][status]'] == 'succeeded':
            client_secret = payment_data['result[paymentIntent][client_secret]']
            payment_confirmation(client_secret)
            return HttpResponse(status=200)
        else:
            return HttpResponse(status=400)



def testing(request):


    # print(received_json_data)
    print(type(request.POST))
    data = request.POST.dict()
    print(data)
    print(data['result[paymentIntent][client_secret]'])


    print(' ')

    # print(city['first'])
    # print(recieved_json_data['csrf'])

    response = JsonResponse({'success': 'Return something'})
    return response