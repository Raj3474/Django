from unittest import skip

from django.test import Client, RequestFactory, TestCase
from django.http import HttpRequest
from django.contrib.auth.models import User
from django.urls import reverse

from catalogue.views import product_all, product_detail
from catalogue.models import Category, Product


# @skip("Testing done previously")
class TestCategoriesModel(TestCase):

    def setUp(self):
        self.data1 = Category.objects.create(name='django', slug='django')

    def test_category_model_entry(self):
        """
        Test Category model data insertion/types/field attributes
        """
        data = self.data1
        self.assertTrue(isinstance(data, Category))

    def test_category_model_entry(self):
        """
        Test Category model default name
        """
        data = self.data1
        self.assertEqual(str(data), 'django')


# @skip("Testing done previously")
class TestProductsModel(TestCase):

    def setUp(self):
        Category.objects.create(name='django', slug='django')  # as it is foreign key for the product table
        User.objects.create(username='admin')  # this is a foreign key in the product table
        self.data1 = Product.objects.create(category_id=1, title='django beginners', created_by_id=1,
                                            slug='django-beginners', price='20.00', image='django')

    def test_products_model_entry(self):
        """
        Test product model data insertion/types/field attributes
        """
        data = self.data1
        self.assertTrue(isinstance(data, Product))
        self.assertEqual(str(data), 'django beginners')


@skip("demonstrating skipping")  # this is a demo that we can also skip test
class TestSkip(TestCase):
    def test_skip_example(self):
        pass


# @skip("testing done previously")
class TestViewResponse(TestCase):
    def setUp(self):
        self.c = Client()
        self.factory = RequestFactory()
        Category.objects.create(name='django', slug='django')  # as it is foreign key for the product table
        User.objects.create(username='admin')  # this is a foreign key in the product table
        self.data1 = Product.objects.create(category_id=1, title='django beginners', created_by_id=1,
                                            slug='django-beginners', price='20.00', image='django')

    def test_url_allowed_hosts(self):
        """
        Test allowed hosts
        """
        response = self.c.get('/')
        self.assertEqual(response.status_code, 200)

    def test_product_detail_url(self):
        """
        Test Product response status
        """
        response = self.c.get(reverse('catalogue:product_detail', args=['django-beginners']))
        self.assertEqual(response.status_code, 200)

    def test_category_detail_url(self):
        """
        Test Category response status
        """
        response = self.c.get(reverse('catalogue:category_list', args=['django']))
        self.assertEqual(response.status_code, 200)

    def test_homepage_html(self):
        request = HttpRequest()
        response = product_all(request)
        html = response.content.decode('utf8')
        print(html)
        self.assertIn('<title>Bookcatalogue</title>', html)
        self.assertTrue(html.startswith('\n<!DOCTYPE html>\n'))
        self.assertEqual(response.status_code, 200)

    # using request_factory instead of Client

    def test_view_function(self):
        request = self.factory.get('/book/django-beginners')
        response = product_detail(request, self.data1.slug)
        html = response.content.decode('utf8')
        # print(html)

        print(f'<title>{self.data1.title}</title>')
        self.assertIn(f'<title>{self.data1.title}</title>', html)
        self.assertTrue(html.startswith('\n<!DOCTYPE html>\n'))
        self.assertEqual(response.status_code, 200)


class TestSettingsResponse(TestCase):
    def setUp(self):
        self.c = Client()
        self.factory = RequestFactory()
        Category.objects.create(name='django', slug='django')  # as it is foreign key for the product table
        User.objects.create(username='admin')  # this is a foreign key in the product table
        self.data1 = Product.objects.create(category_id=1, title='django beginners', created_by_id=1,
                                            slug='django-beginners', price='20.00', image='django')

    def test_url_allowed_hosts(self):
        """
        Test allowed hosts in the settings.py
        """
        response = self.c.get('/', HTTP_HOST='noaddress.com')
        self.assertEqual(response.status_code, 400)

        response = self.c.get('/', HTTP_HOST='yourdomain.com')
        self.assertEqual(response.status_code, 200)

