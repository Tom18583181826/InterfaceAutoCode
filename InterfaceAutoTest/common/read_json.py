import json

from InterfaceAutoTest.common.read_ini import ReadIni


# 定义该方法读取--请求参数文件--和--预期结果文件--中的值
def read_json(file_path):
    with open(file_path, encoding="utf-8") as file:
        return json.loads(file.read())
        # 使用read()将file文件对象转换成字符串类型
        # loads()方法的参数为字符串，可将参数转换成json对象；在使用loads的时候json字符串必须要用双引号，否则会报错；
        # load()方法的参数为文件对象


if __name__ == '__main__':
    read_ini = ReadIni()
    expect_file_path = read_ini.get_expect_file_path()
    expect_data = read_json(expect_file_path)
    params_file_path = read_ini.get_params_file_path()
    params_data = read_json(params_file_path)
    print(expect_data)
    print(params_data)
