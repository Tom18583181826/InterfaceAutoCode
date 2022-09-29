import os
from configparser import ConfigParser
# configparser:是用来读取配置文件的包


class ReadIni:
    def __init__(self):
        self.base_path = os.path.dirname(os.getcwd())
        # os.getcwd():得到当前工作目录，即当前python脚本工作的目录路径
        # os.path.dirname():获取当前文件的父目录名称
        self.config = ConfigParser()
        # 生成一个config对象，以后可以使用config对象去读取配置文件
        ini_file_path = os.path.join(self.base_path, r"data\path.ini")
        # os.path.join():将多个路径组合后返回
        self.config.read(ini_file_path, encoding="utf-8")
        # 通过config对象使用read()方法直接读取ini文件内容

    # 获取excel文件路径
    def get_excel_path(self):
        return os.path.join(self.base_path, self.config.get("Path", "excel_path"))
        # get(section,option):获取section(节点)中option（选项）的值。返回为string类型

    # 获取参数文件路径
    def get_params_file_path(self):
        return os.path.join(self.base_path, self.config.get("Path", "params_file_path"))

    # 获取预期结果文件路径
    def get_expect_file_path(self):
        return os.path.join(self.base_path, self.config.get("Path", "expect_file_path"))

    # 获取测试报告路径
    def get_report_file_path(self):
        return os.path.join(self.base_path, self.config.get("Path", "report_file_path"))

    # 获取sheet页名称
    def get_sheet_name(self):
        return self.config.get("Path", "sheet_name")

    # 获取指定节点下指定选项的值
    def get_option(self, section=None, option=None):
        # 检查section(节点)是否存在
        if self.config.has_section(section=section):
            # 检查option(选项)是否存在
            if self.config.has_option(section=section, option=option):
                # 获取指定节点下指定选项的值
                return self.config.get(section=section, option=option)
            else:
                print("请检查选项的值是否存在！")
        else:
            print("请检查节点的值是否存在！")


if __name__ == '__main__':
    read = ReadIni()
    print(read.get_excel_path())
    print(read.get_params_file_path())
    print(read.get_expect_file_path())
    print(read.get_sheet_name())
    print(read.get_report_file_path())
