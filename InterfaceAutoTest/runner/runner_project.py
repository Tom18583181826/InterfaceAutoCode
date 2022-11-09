import os.path
import time
# import pytest
import unittest
# from HTMLTestRunner import HTMLTestRunner
from BeautifulReport import BeautifulReport
from InterfaceAutoCode.InterfaceAutoTest.common.read_ini import ReadIni

# from InterfaceAutoTest.common.send_mail import SendMail

if __name__ == '__main__':
    # 获取当前系统的时间，生成字符串
    now = time.strftime("%Y_%m_%d_%H_%M_%S")

    # 获取测试报告路径
    read = ReadIni()
    report_path = read.get_report_file_path()

    # # --------------------------------------------------------------------------------------
    # # 使用pytest单元测试框架生成pytest_html测试报告(需要安装pytest拓展插件pytest_html)
    # pytest.main([r"E:\Python\InterfaceAutoCode\InterfaceAutoTest\case\test_cases_pytest.py",
    #              r"--html=E:\Python\InterfaceAutoCode\InterfaceAutoTest\result\pytest_html_report\report{}.html".format(
    #                  now),
    #              "--self-contained-html"])
    # # --------------------------------------------------------------------------------------

    # #  --------------------------------------------------------------------------------------
    # # 使用pytest单元测试框架生成Allure测试报告
    # pytest.main([r"J:\代码示例\InterfaceAutoCode\InterfaceAutoTest\case\test_cases_pytest.py",
    #              "--alluredir",
    #              r"J:\代码示例\InterfaceAutoCode\InterfaceAutoTest\result\allure_report\xml_file"])
    # # 使用pytest单元测试框架生成Allure测试报告：
    # #     1.因为Allure基于java所以需要有jdk1.8+环境
    # #     2.下载Allure包，解压到指定目录下，将bin目录配置到环境变量中
    # #     3.在命令行工具中，输入(allure --version)，输出版本信息表示成功
    # #     4.在Pycharm中安装allure-pytest库
    # #     5.在命令行工具/Pycharm的Terminal(需进入用例目录)/代码中，输入命令生成XML文件
    # #     ---pytest 用例模块 --alluredir XML格式文件目录
    # #     6.在命令行中输入命令，将XML格式文件转换成HTML格式文件
    # #     ---allure generate XML格式文件目录 -o HTML格式文件目录(不需要指定文件名)
    # #     提示：Report successfully generated to HTML报告路径---成功
    # #     7.（按需求执行）---在命令行输入命令后会自动启动你的默认浏览器，打开测试报告
    # #     ---allure serve HTML文件路径---命令行退出按Ctrl+C输入Y可退出
    # #     注：直接使用谷歌浏览器打开报告，可能会显示空白
    # #     解决办法：1.在Pycharm中右击报告文件选择open in Browser方式打开
    # #             2.使用火狐浏览器可直接打开
    # # ------------------------------------------------------------------------

    # # ------------------------------------------------------------------------
    # # 使用unittest单元测试框架生成HTMLTestRunner测试报告
    # # 测试用例目录
    # test_dir = r"J:\代码示例\InterfaceAutoCode\InterfaceAutoTest\case"
    # # 加载测试用例
    # discover = unittest.defaultTestLoader.discover(test_dir, "test*.py")
    # # 测试报告路径
    # report_path = r"J:\代码示例\InterfaceAutoCode\InterfaceAutoTest\result\HTMLTestRunner_report\report{}.html".format(
    #     now)
    # with open(report_path, "wb") as report:
    #     runner = HTMLTestRunner(stream=report,
    #                             title="测试报告",
    #                             description="执行unittest单元测试框架生成测试报告")
    #     runner.run(discover)
    # # HTMLTestRunner模块不能通过pip安装，必须先百度下载后右键另存到Python安装目录的Lib文件夹下，
    # # 因为HTMLTestRunner模块是基于Python2开发的，目前停止更新，在Python3上运行会报错，
    # # 为了使其支持Python3环境，需要对其中的部分内容进行修改(实际改动行数会有差异需要百度解决)
    # # -----------------------------------------------------------------------------------

    # -----------------------------------------------------------------------------
    # 使用unittest单元测试框架生成BeautifulReport测试报告
    base_path = os.path.dirname(os.getcwd())
    # os.getcwd():得到当前工作目录，即当前python脚本工作的目录路径
    # os.path.dirname():获取当前文件的父目录名称
    # 测试用例目录
    test_dir = os.path.join(base_path, r"case")
    # 加载测试用例,匹配以unittest.py结尾的脚本文件
    discover = unittest.defaultTestLoader.discover(test_dir, "*unittest.py")
    # 实例化BeautifulReport模块
    report = BeautifulReport(discover)
    report.report(filename="report{}".format(now),
                  description="使用BeautifulReport模板生成测试报告",
                  report_dir=report_path,
                  theme="theme_memories")
    # Report API简介：
    # BeautifulReport_report.report(filename="测试报告名称，如果不指定默认文件名为report.html",
    #                        description="测试报告用例名称展示",
    #                        report_dir="报告文件写入路径",
    #                        theme="报告主题样式(theme_default, theme_cyan, theme_candy, theme_memories)")
    # ---------------------------------------------------------------------------------

    # # ---------------------------------------------------------------------------------------
    # # 发送邮件
    # sendmail = SendMail()
    # sendmail.send_mail(report_path + "report{}.html".format(now))
    # # -----------------------------------------------------------------------------
