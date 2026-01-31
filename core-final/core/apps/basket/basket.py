from decimal import Decimal

from django.conf import settings

from core.apps.checkout.models import DeliveryOptions
from core.apps.catalogue.models import Product


class Basket():
    """
    A base Basket class, providing some default behaviors
    that can be inherited or overrided, as necessary
    """

    def __init__(self, request):
        self.session = request.session
        basket = self.session.get(settings.BASKET_SESSION_ID)   # skey = session_key
        if settings.BASKET_SESSION_ID not in request.session:
            basket = self.session[settings.BASKET_SESSION_ID] = {}
        self.basket = basket

    def add(self, product, product_qty):
        """
        Adding and updating the users basket session data
        """
        product_id = str(product.id)

        if product_id not in self.basket:
            self.basket[product_id] = {'price': str(product.regular_price), 'quantity': int(product_qty)}
        else:
            self.basket[product_id]['quantity'] += int(product_qty)

        self.save()

    def delete(self, productid):
        """
        Delete item from session data
        """
        product_id = str(productid)

        if productid in self.basket:
            del self.basket[productid]

        self.save()


    def update(self, productid, qty):
        product_id = str(productid)

        if productid in self.basket:
            self.basket[product_id]['quantity'] = int(qty)

        self.save()

    def __iter__(self):
        """
        Collect the product_id in the session data t query the databse
        and return products
        """
        product_ids = self.basket.keys()
        # print(product_ids)
        products = Product.products.filter(id__in=product_ids)
        # print(products)
        basket = self.basket.copy()
        # print(basket)

        for product in products:
            basket[str(product.id)]['product'] = product

        # print(basket)
        # print(basket.values())

        for item in basket.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            # print(item)
            yield item
        # print(basket.values())

    def __len__(self):
        """
        Get the basket data count hte qty of items
        """
        return sum(item['quantity']  for item in self.basket.values())

    def get_subtotal_price(self):
        subtotal = sum(Decimal(item['price']) * item['quantity'] for item in self.basket.values())

        return subtotal

    def get_delivery_price(self):
        shipping = 0.00
        if "purchase" in self.session:
            shipping = DeliveryOptions.objects.get(id=self.session["purchase"]["delivery_id"]).delivery_price
        return shipping

    def get_total_price(self):
        subtotal = self.get_subtotal_price()
        shipping = self.get_delivery_price()

        total = subtotal + Decimal(shipping)
        return total

    def basket_update_delivery(self, deliveryprice=0):
        subtotal = self.get_subtotal_price()
        total = subtotal + Decimal(deliveryprice)
        return total


    def clear(self):
        # Remove basket from session
        del self.session[settings.BASKET_SESSION_ID]

        if "address" in self.session:
            del self.session["address"]

        if "purchase" in self.session:
            del self.session["purchase"]
        self.save()


    def save(self):
        self.session.modified = True



# 1:55