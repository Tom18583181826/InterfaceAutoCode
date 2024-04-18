# 用pytest框架来组织用例：
# 1）创建对象，通过自定义固件实现，在conftest.py文件中自定义固件；
# 2）要从excel + json中读取数据，通过参数化的装饰器传进去；
# 2-1）可以通过声明一个函数来实现读取数据，返回装饰器需要的结构
# 3）写一个统一的方法，对它进行参数化，传入每个接口的信息，实现跑每一个接口；
# 4）参数化通过装饰器pytest.mark.parametrize来实现。
import pytest
# pytest标识符命名规范：
# 1.模块的命名以"test_"开头或"_test.py"结尾；
# 2.类的命名以"Test"开头；
# 3.测试用例的命名以"test"开头
from InterfaceAutoTest.common.read_excel import ReadExcel
from InterfaceAutoTest.common.get_json_value_by_key import GetJsonValue


# 从excel表中获取测试数据,返回 @pytest.mark.parametrize装饰器需要的结构（列表）
def get_data():
    read_excel = ReadExcel()  # 实例化读取Excel列表对象
    data_list = []  # 存放数据列表
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
        data_type = read_excel.get_data_type(row)  # 获取响应数据的类型
        if if_execute == "Y":
            # 当是否执行用例标识的值为：Y 时，将从Excel表格中读取的数据添加到data_list列表中
            data_list.append(
                (case_id, case_name, method, url, if_execute, precondition_id, depend_key, pattern, expect, data_type,
                 row))
    return data_list


class TestCasesWithPytest:
    # 参数化通过装饰器pytest.mark.parametrize来实现。
    @pytest.mark.parametrize(
        "case_id, case_name, method, url, if_execute, precondition_id, depend_key, pattern, expect, data_type, row",
        get_data())
    # @pytest.mark.parametrize("参数名", list, ids=None)
    # 第一个参数为字符串，多个参数中间使用逗号隔开，参数名要与用例函数或方法中的形参名保持一致
    # 第二个参数为列表，多组数据用元组类型。list的每个元素都是一个元组，元组里的每一个元素按参数顺序一一对应
    # ids参数默认为空，用于定义测试用例的名称，例如：ids=["case1", "case2", "case3"]
    # ----------------------------------------------------
    # 对该方法进行参数化，传入每个接口的信息，实现跑每个接口
    def test_all(self, get_request, case_id, case_name, method, url, if_execute, precondition_id, depend_key, pattern,
                 expect,
                 data_type, row):
        if if_execute == "Y":
            # 当是否执行用例标识的值为：Y 时，执行当前用例
            print("现在开始执行第%d行的用例" % row)
            if precondition_id:
                # 当存在前置用例ID时，获取前置用例的关联参数更新到当前请求参数中
                print("前置用例是：%s" % precondition_id)
                params = get_request.get_updated_case_params(row)
            else:
                # 当不存在前置用例ID时，获取当前用例的参数
                params = get_request.read_excel.get_case_params_value(row)
            actual = get_request.get_actual_result(method, url, data_type, params)
            # 传入参数发起请求，获得请求的实际响应结果
            print(case_id, case_name, method, url, params)

            # 断言：如果响应数据类型是JSON，就判断预期结果与实际结果是否相等，
            #      如果响应数据类型是XML，就判断预期结果是否包含在实际结果中。
            if expect:
                # 存在预期结果执行断言
                if data_type == "JSON":
                    actual = GetJsonValue().get_json_value_by_key(actual, list(expect.keys())[0])
                    try:
                        assert list(expect.values())[0] in actual
                    except AssertionError:
                        # print("预期结果是：%s" % dict(set(expect.items()) - set(actual.items())))
                        # print("实际结果是：%s" % dict(set(actual.items()) - set(expect.items())))
                        raise AssertionError
                elif data_type == "XML":
                    try:
                        assert expect in actual
                    except AssertionError:
                        raise AssertionError


if __name__ == '__main__':
    pytest.main()
    # 运行全部测试用例

    # pytest.main(['-s', '-v', './test_dir'])
    # 运行测试常用参数：
    # -s:用于关闭捕捉，从而输出打印信息(pytest -s ---.py   注：切换到文件所在目录执行pytest命令，下面参数同理)
    # -v:用于增加测试用例冗长(pytest -v ---.py)
    # -k 字符串:运行名称中包含某字符串的测试用例(pytest -k abc ---.py)
    # -q(--quiet):减少测试运行的冗长(pytest -q ---.py)
    # -x:如果出现一条测试用例失败，则退出测试(pytest -x ---.py)
    # --maxfail=num:表示遇到num个用例执行失败或错误就停止
    # pytest 测试目录（可以是相对路径也可以是绝对路径）：运行测试目录（pytest ./test_dir）
    # pytest 测试模块::测试类::测试方法:指定特定类或方法执行(文件名，类名，方法名之间用::符号分隔)

    # 生成测试报告：
    # 1.生成JUnitXML文件
    #     pytest 测试目录 --junit-xml=文件路径(pytest ./test_dir --junit-xml=./report/log.xml)
    # 2.生成在线测试报告
    #     pytest 测试目录 --pastebin=all(pytest ./test_dir --pastebin=all)
    #     上行代码会生成一个session-log链接，复制链接，通过浏览器打开会得到一张HTML格式的测试报告

    # pytest拓展插件：
    # 1.pytest-rerunfailures:可以在测试用例失败时进行重试
    #         通过“--reruns”参数设置测试用例运行失败后的重试次数
    #         例如：pytest ---.py --reruns 3
    # 2.pytest-parallel:实现测试用例的并行运行
    #         例如：pytest ---.py --tests-per-worker auto
    #         --tests-per-worker:用于指定线程数
    #         auto:表示自动分配
    #         注：并行运行测试很可能相互产生干扰，从而导致测试用力失败，因此建议谨慎使用
