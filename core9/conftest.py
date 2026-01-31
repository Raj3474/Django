"""
conftest.py: file is used for making the fixtures for our
tests.
"""

import pytest
from pytest_factoryboy import register

from tests.factories import CategoryFactory

# @pytest.fixture(scope=<"module", "session", "test"), default is function
# running this fixture once in every scope added above
# @pytest.fixture(scope="session")
# def test_fixture1():
#     print("Run once")
#     return 1


register(CategoryFactory)

@pytest.fixture
def product_category(db, category_factory):
    category = category_factory.create()
    return category