from django.test import TestCase


class TestClass(TestCase):
    def test_hello_world(self):
        self.assertEqual("hello", "hello")


# ----  this is similar but with less code ------
import pytest


def test_hello_world():
    assert "hello" == "hello"


# @pytest.fixture(scope=<"module", "session", "test"), default is function
# running this fixture once in every scope added above
# we can the fixtures here or in the conftest.py file
# @pytest.fixture(scope="module")
# def test_fixture1():
#     print("Run each test")
#     return 1


@pytest.mark.skip
def test_hello_world1(test_fixture1):
    print("function_fixture1")
    assert test_fixture1 == 1

@pytest.mark.skip
def test_hello_world2(test_fixture1):
    print("function_fixture2")
    assert test_fixture1 == 1
