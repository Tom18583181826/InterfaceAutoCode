# 用unittest框架来组织测试用例
# 1）要从excel+json中读取数据，通过参数化的装饰器传进去；
# 1-1）可以通过声明一个函数来实现读取数据，返回装饰器需要的结构；
# 2）写一个统一的方法，对它进行参数化，传入每个接口的信息，实现跑每一个接口；
import unittest
import warnings

# from ddt import ddt, data, file_data, unpack
# DDT同样支持数据文件的参数化。
# @file_data("文件路径及文件名")-----在测试方法前使用装饰器装饰
# 注：数据文件需要放在使用的.py文件的同一目录下，否则需要指定文件路径
from parameterized import parameterized
# parameterized是Python的一个参数化库，同时支持unittest,Nose,pytest单元测试框架
from InterfaceAutoTest.common.get_json_value_by_key import GetJsonValue
from InterfaceAutoTest.common.read_excel import ReadExcel
from InterfaceAutoTest.request_method.request_method import RequestMethod


# 从excel表中获取测试数据,返回 @parameterized.expand装饰器需要的结构（列表）
def get_data():
    read_excel = ReadExcel()  # 实例化读取Excel列表对象
    data_list = []  # 存放数据表格
    for row in range(2, read_excel.get_row_count() + 1):
        # 从第二行开始读取Excel表格直至读取完数据
        case_id = read_excel.get_case_id(row)  # 获取用例ID
        case_name = read_excel.get_case_name(row)  # 获取用例标题
        method = read_excel.get_case_method(row)  # 获取请求方法
        url = read_excel.get_case_url(row)  # 获取请求地址
        if_execute = read_excel.get_if_execute(row)  # 获取是否执行用例标识
        precondition_id = read_excel.get_case_precondition_id(row)  # 获取前置用例ID
        depend_key = read_excel.get_case_depend_key(row)  # 获取依赖字段
        pattern = read_excel.get_case_re(row)  # 获取正则表达式
        expect = read_excel.get_case_expect_value(row)  # 获取预期结果的value
        data_type = read_excel.get_data_type(row)  # 获取响应的数据类型
        if if_execute == "Y":
            # 当是否执行用例标识的值为：Y 时，将从Excel表格中读取的数据添加到data_list列表中
            data_list.append(
                (case_id, case_name, method, url, if_execute, precondition_id, depend_key, pattern, expect, data_type,
                 row))
    return data_list


# @ddt
# DDT是针对unittest单元测试框架设计的扩展库。允许使用不同的测试数据来运行一个测试用例，并将其展示为多个测试用例
# 使用DDT时，测试类需要通过@ddt装饰器装饰
# 测试方法使用@data,@unpack传入参数
class TestCasesWithUnittest(unittest.TestCase):
    #           注：setUpClass/tearDownClass为类方法，需要通过@classmethod进行装饰。
    #               另外，方法的参数为cls.其实cls与self并没有什么本质区别，都只表示方法的第一个参数
    @classmethod
    # 修饰符对应的函数不需要实例化，不需要self参数，但第一个参数需要是表示自身类的cls参数，可以来调用类的属性，类的方法，实例化对象等。
    def setUpClass(cls):
        # 在每个测试类执行之前执行，使用必须要加@classmethod内置装饰器，
        # 否则会报“TypeError: setUpClass() missing 1 required positional argument: 'cls'”的错误，
        # --------TypeError: setUpClass()缺少一个必需的位置参数：“cls"-----------------------------
        # ---------对于类方法，第一个参数必须是类对象，一般以"cls"作为第一个参数---------
        # 使用类方法执行所有测试用例时里面的方法只会执行一次，不会重复执行
        warnings.simplefilter("ignore", ResourceWarning)
        # 屏蔽未关闭资源警告
        # simplefilter(action, category = Waring)---简单易用的过滤器
        # 参数说明：action---处理方式
        #         category = Waring---警告类别
        cls.request_method = RequestMethod()

    # @data([], [], [])   参数化方式一：传入列表
    # @data((),(),())     参数化方式二：传入元组
    # @data({},{},{})     参数化方式三：传入字典(注：字典的key与测试方法的参数要保持一致)
    # @unpack
    @parameterized.expand(get_data())
    # parameterized模块提供了expand和parameterized_class两个装饰器,
    # 前者实现对方法的参数化后者实现对测试类的参数化
    def test_all(self, case_id, case_name, method, url, if_execute, precondition_id, depend_key, pattern, expect,
                 data_type, row):
        """测试所有接口"""
        # Python的注释分两种：comment(普通注释)和doc string(用于描述函数，类，方法)
        # 在类或方法下方通过三引号(""""""或'''''')添加doc string类型的注释。可以被HTMLTestRunner读取显示在测试报告中
        if if_execute == "Y":
            # 当是否执行用例标识的值为：Y 时，执行当前用例
            print("现在开始执行第%d行的用例" % row)
            if precondition_id:
                # 当存在前置用例ID时，获取前置用例的关联参数更新到当前请求参数中
                print("前置用例是：%s" % precondition_id)
                params = self.request_method.get_updated_case_params(row)
            else:
                params = self.request_method.read_excel.get_case_params_value(row)
            actual = self.request_method.get_actual_result(method, url, data_type, params)
            # 传入参数发起请求，获得请求的实际响应结果
            print(case_id, case_name, method, url, params)

            # 断言：如果响应数据类型是JSON，就判断预期结果与实际结果是否相等，
            #      如果响应数据类型是XML，就判断预期结果是否包含在实际结果中
            if expect:
                # 存在预期结果执行断言
                if data_type == "JSON":
                    actual = GetJsonValue().get_json_value_by_key(actual, list(expect.keys())[0])
                    expect = list(expect.values())
                    try:
                        self.assertEqual(expect, actual, msg="实际与预期不一致！")
                    except AssertionError:
                        # print("预期结果是：%s" % dict(set(expect.items()) - set(actual.items())))
                        # print("实际结果是：%s" % dict(set(actual.items()) - set(expect.items())))
                        raise AssertionError
                elif data_type == "XML":
                    try:
                        self.assertIn(expect, actual, msg="预期不在实际中！")
                    except AssertionError:
                        raise AssertionError


if __name__ == '__main__':
    # # 执行测试用例方法一
    # unittest.main()
    # # 运行全部测试用例

    # # 执行测试用例方法二
    # suiteTest = unittest.TestSuite()
    # # 创建测试套
    # suiteTest.addTest(TestCasesWithUnittest("test_all"))
    # # 在测试套中添加测试用例
    # runner = unittest.TextTestRunner()
    # # 实例化TextTestRunner()类
    # runner.run(suiteTest)
    # # 使用TextTestRunner()类下的run()方法运行测试套件

    # 执行测试用例方法三
    test_dir = "./case"
    discover = unittest.defaultTestLoader.discover(test_dir, pattern="unittest.py$")
    # 通过unittest.defaultTestLoader类下面的discover()方法可自动根据测试目录test_dir
    # 匹配查找测试用例文件(test*.py),并将查找到的测试用例组装到测试套件中，
    # 因此可以直接通过run()方法执行discover.
    runner = unittest.TextTestRunner()
    runner.run(discover)
