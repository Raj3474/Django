from decimal import Decimal
from django.conf import settings
from django.db import models


from core.apps.catalogue.models import Product
# Create your models here.


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='order_user')

    is_store_pickup = models.BooleanField(default=False)
    is_bill_add_equals_deli_add = models.BooleanField(default=False)

    """
    Billing Address
    """
    bill_full_name = models.CharField(max_length=50)
    bill_email = models.EmailField(max_length=254, blank=True)
    bill_phone = models.CharField(max_length=100)

    bill_address_line1 = models.CharField(max_length=250)
    bill_address_line2 = models.CharField(max_length=250)
    bill_landmark = models.CharField(max_length=255, blank=True)
    bill_city = models.CharField(max_length=100)
    bill_state = models.CharField(max_length=64)
    bill_pincode = models.CharField(max_length=20)
    bill_country = models.CharField(max_length=64)

    """
    Delivery Address
    """
    deli_full_name = models.CharField(max_length=50, blank=True)
    deli_email = models.EmailField(max_length=254, blank=True)
    deli_phone = models.CharField(max_length=100, blank=True)

    deli_address_line1 = models.CharField(max_length=250, blank=True)
    deli_address_line2 = models.CharField(max_length=250, blank=True)
    deli_landmark = models.CharField(max_length=255, blank=True)
    deli_city = models.CharField(max_length=100, blank=True)
    deli_state = models.CharField(max_length=64, blank=True)
    deli_pincode = models.CharField(max_length=20, blank=True)
    deli_country = models.CharField(max_length=64, blank=True)


    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    total_paid = models.DecimalField(max_digits=5, decimal_places=2)
    order_key = models.CharField(max_length=200)
    payment_option = models.CharField(max_length=200, blank=True)
    billing_status = models.BooleanField(default=False)

    def copy_billing_address_to_delivery(self):
        self.deli_full_name = self.bill_full_name
        self.deli_email = self.bill_email
        self.deli_phone = self.bill_phone

        self.deli_address_line1 = self.bill_address_line1
        self.deli_address_line2 = self.bill_address_line2
        self.deli_landmark = self.bill_landmark
        self.deli_city = self.bill_city
        self.deli_state = self.bill_state
        self.deli_pincode = self.bill_pincode
        self.deli_country = self.bill_country

    class Meta:
        ordering = ('-created',)

    def save(self, *args, **kwargs):
        if self.is_bill_add_equals_deli_add and not self.is_store_pickup:
            self.copy_billing_address_to_delivery()
        super(Order, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.created)


class OrderItem(models.Model):
    order = models.ForeignKey(Order,
                              related_name='items',
                              on_delete=models.CASCADE)
    product = models.ForeignKey(Product,
                                related_name='order_items',
                                on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)


    def __str__(self):
        return str(self.id)



class OrderStatus(models.Model):
    """
    Order Status related to Order
    """
    ORDER_STATUS = [
        ("101", "Order Placed"),
        ("102", "Order Cancelled"),
        ("103", "Order Accepted"),
        ("104", "Order Dispatched"),
        ("105", "Order Delivered"),

        ("201", "Refund Initiated"),
        ("202", "Refund Received"),

        ("301", "Return Requested"),
        ("302", "Return Accepted"),
        ("303", "Return Rejected by the Owner"),
        ("304", "Return Received")
    ]

    orderitem = models.ForeignKey(OrderItem, on_delete=models.CASCADE)