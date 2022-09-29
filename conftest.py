# conftest.py只作用于它所在的目录及子目录

# 自定义一个固件，实例化RequestMethod类的对象
import pytest
from InterfaceAutoTest.request_method.request_method import RequestMethod


@pytest.fixture(scope="session")
def get_request():
    yield RequestMethod()
