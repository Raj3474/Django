from decimal import Decimal

from store.models import Product



class Basket():
    """
    A base Basket class, providing some default behaviors that
    can be inherited or overrided, as necessary
    """

    def __init__(self, request):
        self.session = request.session
        basket = self.session.get('skey')   # skey = session_key
        if 'skey' not in request.session:
            basket = self.session['skey'] = {}
        self.basket = basket

    def add(self, product, product_qty):
        """
        Adding and updating the users basket session data
        """
        product_id = str(product.id)

        if product_id not in self.basket:
            self.basket[product_id] = {'price': str(product.price), 'quantity': int(product_qty)}
        else:
            self.basket[product_id]['quantity'] += int(product_qty)

        self.save()

    def delete(self, productid):
        """
        Delete item from session data
        """
        if productid in self.basket:
            del self.basket[productid]

        self.save()


    def update(self, productid, qty):
        product_id = str(productid)

        if productid in self.basket:
            print('In update if ')
            print(type(product_id), type(qty))
            print(self.basket[product_id]['quantity'])
            self.basket[product_id]['quantity'] = int(qty)
            print(self.basket[product_id]['quantity'])

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

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.basket.values())

    def save(self):
        self.session.modified = True