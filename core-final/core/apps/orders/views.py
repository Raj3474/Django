from django.shortcuts import render
from django.http.response import JsonResponse

from core.apps.basket.basket import Basket
from .models import Order, OrderItem
from core.apps.account.models import Customer, Address
from core.apps.checkout.models import DeliveryOptions



# Create your views here.
def add(request):
    basket = Basket(request)
    if request.method:

        """
        before adding into order table, do the sanity checking
        if all the fields are avaiable
        """

        order_key = request.POST.get('order_key')
        user_id = request.user.id
        baskettotal = basket.get_total_price()

        if Order.objects.filter(order_key=order_key).exists():
            pass
        else:
            customer = Customer.objects.get(pk=user_id)

            address_id = request.session["address"]["address_id"]
            address = Address.objects.get(pk=address_id)

            delivery_option = request.session["purchase"]["delivery_id"]
            delivery = DeliveryOptions.objects.get(id=delivery_option)

            print(delivery.delivery_method)


            order = Order.objects.create(
                user_id=user_id,

                is_store_pickup = False,
                is_bill_add_equals_deli_add = True,

                bill_full_name=address.full_name,
                bill_email=customer.email,
                bill_phone=address.phone,

                bill_address_line1=address.address_line1,
                bill_address_line2=address.address_line2,
                bill_landmark=address.landmark,
                bill_city=address.city,
                bill_state=address.state,
                bill_pincode=address.pincode,
                bill_country=address.country,

                total_paid=baskettotal, order_key=order_key
            )
            order_id = order.pk


            for item in basket:
                OrderItem.objects.create(order_id=order_id, product=item['product'],
                                        price=item['price'], quantity=item['quantity'])

        response = JsonResponse({'success': 'Return something'})
        return response


def payment_confirmation(data):
    Order.objects.filter(order_key=data).update(billing_status=True)


def user_orders(request):
    user_id = request.user.id
    orders = Order.objects.filter(user_id=user_id).filter(billing_status=True)
    return orders