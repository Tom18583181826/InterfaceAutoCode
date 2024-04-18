# conftest.py只作用于它所在的目录及子目录

# 自定义一个固件，实例化RequestMethod类的对象
import pytest
from InterfaceAutoTest.request_method.request_method import RequestMethod


@pytest.fixture(scope="session")
def get_request():
    yield RequestMethod()

# 通过pytest.fixture装饰器去装饰一个函数，这个函数就变成了一个固件
# pytest.fixture装饰器的参数：
#               scope:定义固件的级别
#                       scope="function":默认值
#                       scope="class"
#                       scope="module"
#                       scope="session":在整个会话执行之前执行，相比于setup_module来讲可以实现跨模块
#               autouse:实现固件的自动调用，传入autouse=True表示自动调用，默认autouse=False

# 调用自定义固件的三种方法：
# 1.把固件对象作为参数传入到测试用例的函数或方法中
# 2.在pytest.fixture装饰器中，通过传入参数autouse=True来实现自动调用自定义固件
# 3.在装饰器pytest.mark.usefixtures("固件名称")来装饰测试用例实现自定义固件的调用

# 自定义固件中teardown代码的实现：
#     在自定义固件中，使用yield来代替return语句，yield语句之前的代码作为setup的代码执行，yield语句之后的代码作为teardown的代码执行

# 固件的参数化：
#       通过在装饰器pytest.fixture()中传入参数params来实现参数化
#       params可以传列表或元组，在固件函数中声明一个形参request，在固件中返回request.param来实现返回params中传入的一组值
#       从而实现对固件的参数化
