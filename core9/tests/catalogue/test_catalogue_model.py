import pytest
from django.urls import reverse

def test_category_str(product_category):
    assert product_category.__str__() == "django"



# client helps to make request (a get request)
def test_category_reverse(client, product_category):
    category = product_category
    url = reverse("catalogue:category_list", args=[category])
    response = client.get(url)
    assert response.status_code == 200