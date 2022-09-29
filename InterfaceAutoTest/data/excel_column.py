class ExcelColumn:
    # 该类定义常量，用于标识表头名所在列
    CASE_ID = "A"  # 用例编号
    CASE_NAME = "B"  # 用例标题
    CASE_METHOD = "C"  # 请求方法
    CASE_URL = "D"  # 请求地址
    CASE_IF_EXECUTE = "E"  # 是否执行标识
    CASE_PRECONDITION_ID = "F"  # 前置用例ID
    CASE_DEPEND_KEY = "G"  # 依赖字段
    CASE_RE = "H"  # 正则表达式
    CASE_PARAMS_KEY = "I"  # 请求参数的key
    CASE_EXPECT_KEY = "J"  # 预期结果的key
    CASE_DATA_TYPE = "K"  # 响应数据类型
