# 该模块需要实现：
# 1）发送请求，获取响应；
# 2）对于有前置用例的场景，首先执行前置用例，从响应中使用正则表达式提取value；
# 3）把提取到的value更新到请求参数中。
import re
import requests
import requests.packages.urllib3
from InterfaceAutoCode.InterfaceAutoTest.common.read_excel import ReadExcel
from InterfaceAutoCode.InterfaceAutoTest.common.get_json_value_by_key import GetJsonValue


class RequestMethod:
    def __init__(self):
        self.session = requests.session()
        # 实例化一个session对象的作用:
        # 1.用同一个session对象发送请求,可以自动处理cookie关联
        # 2.可以设置整个会话的全局配置,比如:统一headers等
        self.read_excel = ReadExcel()

    # 封装一个统一的方法，发送get和post请求，返回一个response对象
    def get_or_post(self, method, url, params=None):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"}
        # 定义请求头数据
        if method == "GET":
            # 发送一个get请求，get请求的参数通过params参数传入，传入字典或元组的列表
            requests.packages.urllib3.disable_warnings()
            # 忽略不安全的请求警告信息---urllib3.disable_warnings() ---（屏蔽https证书警告）
            return self.session.get(url=url, params=params, verify=False, headers=headers)
            # verify参数：控制是否校验CA证书，如果不想校验CA证书传入verify=False
            # -------------------------------------------------------------
            # 当verify=False时，运行代码会报（不安全请求警告：正在向主机发送未经验证的HTTPS请求，强烈建议添加证书验证
            # ---报错信息为：InsecureRequestWarning: Unverified HTTPS request is being made to host
            # Adding certificate verification is strongly advised）
        elif method == "POST":
            # 发送一个post请求，post请求的参数通过data参数传入，传入字典或元组的列表
            return self.session.post(url=url, data=params, verify=True, headers=headers)
        # request函数中的参数说明
        # 1.json参数:接受post请求的传参,传入json序列(注:Content-Type:application/json)
        # 2.files参数:接受form-data中的file参数,实现文件上传的场景,接受文件流对象的键值对(注:Content-Type:multipart/form-data)
        # 代码示例:filepath = r"文件路径"
        #         myfile = {"file":open(filepath, "rb")}
        #         reponse = requests.request("POST", url, data=data, file= myfile)
        # 3.headers参数:设置请求头,传入字典
        # 4.cookies参数:实现在请求中添加cookie信息

    # 请求接口，获取接口响应的body，可以用于正则表达式提取或者断言，如果响应的是json就返回字典，如果响应的是XML就返回字符串
    def get_actual_result(self, method, url, data_type, params=None):
        response = self.get_or_post(method, url, params)
        if data_type == "JSON":
            return response.json()
        else:
            return response.text
        # Response类:
        # 1.json():当响应的数据为json格式时,将响应的正文以json格式编码返回,返回的是字典
        # 2.text:当响应的数据为xml或json格式时,将响应的正文以字符串返回
        # 3.headers:获取响应的信息头,以字典返回
        # 4.status_code:获取响应的状态码
        # reason:获取响应的状态消息
        # cookies:获取响应的cookies信息
        # url:获取请求的url地址
        # elapsed:获取响应的时间
        # encoding:获取响应的编码格式

    # 根据前置用例id获取前置用例的行号,传入参数为前置用例的id
    def get_precondition_row(self, precondition_id):
        for row in range(2, self.read_excel.get_row_count() + 1):
            case_id = self.read_excel.get_case_id(row)
            # 获取用例ID
            if precondition_id == case_id:
                # 当获取到的用例ID等于前置用例ID时返回前置用例行号
                return row

    # 执行前置用例，获取前置用例的响应
    def get_precondition_result(self, precondition_row):
        method = self.read_excel.get_case_method(precondition_row)
        # 获取前置用例请求方法
        url = self.read_excel.get_case_url(precondition_row)
        # 获取前置用例请求地址
        params = self.read_excel.get_case_params_value(precondition_row)
        # 获取前置用例请求参数
        return self.get_actual_result(method, url, params)

    # 从前置用例的响应中根据正则表达式提取value,与依赖字段组成键值对返回
    def get_depend_key_value(self, row):
        precondition_id = self.read_excel.get_case_precondition_id(row)
        precondition_row = self.get_precondition_row(precondition_id)
        depend_key = self.read_excel.get_case_depend_key(precondition_row)
        # 获取依赖字段的键
        pattern = self.read_excel.get_case_re(precondition_row)
        # 获取正则表达式
        precondition_result = self.get_precondition_result(precondition_row)
        # 获取前置用例的执行结果
        depend_value = re.findall(pattern, precondition_result)[0]
        # 获取依赖字段的值
        # re.findall(pattern, string):根据正则表达式从左往右扫描字符串，
        # 把匹配到的内容以字典返回
        return {depend_key: depend_value}

    # 把正则表达式提取到的键值对，更新到请求参数中
    def get_updated_case_params(self, row):
        dict1 = self.read_excel.get_case_params_value(row)
        dict2 = self.get_depend_key_value(row)
        dict1.update(dict2)
        return dict1


if __name__ == '__main__':
    request_method = RequestMethod()
    for row in range(2, request_method.read_excel.get_row_count() + 1):
        if request_method.read_excel.get_if_execute(row) == "Y":
            # 当执行标识值为Y时
            print("现在开始执行第%d行的用例" % row)
            method = request_method.read_excel.get_case_method(row)
            # 获取请求方法
            url = request_method.read_excel.get_case_url(row)
            # 获取请求地址
            data_type = request_method.read_excel.get_data_type(row)
            # 获取响应结果数据类型
            precondition_case_id = request_method.read_excel.get_case_precondition_id(row)
            if precondition_case_id:
                # 如果前置用例id存在
                params = request_method.get_updated_case_params(row)
                # 更新键值对到请求参数中
            else:
                params = request_method.read_excel.get_case_params_value(row)
            actual_result = request_method.get_actual_result(method, url, data_type, params)
            # 获取接口响应实际结果
            print(method, url, params)
            expect_result = request_method.read_excel.get_case_expect_value(row)
            # 获取预期结果的value值

            # 断言：如果响应数据类型是JSON，就判断预期结果与实际结果是否相等，
            #      如果响应数据类型是XML，就判断预期结果是否包含在实际结果中
            if expect_result:
                if data_type == "JSON":
                    actual_result = GetJsonValue().get_json_value_by_key(actual_result, list(expect_result.keys())[0])
                    expect_result = list(expect_result.values())
                    if expect_result == actual_result:
                        print("断言成功！")
                    else:
                        print("断言失败！")
                        # print("预期结果是：%s" % dict(set(expect_result.items()) - set(actual_result.items())))
                        # print("实际结果是：%s" % dict(set(actual_result.items()) - set(expect_result.items())))
                elif data_type == "XML":
                    if expect_result in actual_result:
                        print("断言成功！")
                    else:
                        print("断言失败！")
