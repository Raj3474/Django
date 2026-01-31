import factory
from core.apps.catalogue.models import Category
from faker import Faker

fake = Faker() # faker helps to create data

"""
Category
"""

class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    # name = fake.name()
    name = "django"
    slug = "django"