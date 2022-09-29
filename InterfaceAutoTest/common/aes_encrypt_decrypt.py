import base64
from Crypto.Cipher import AES


# pycrypto,pycryptodome和crypto是一个东西，crypto在python上面的名字是pycrypto，它是一个第三方库，但是已经停止更新，所以不建议安装这个库
# pycryptodome是pycrypto的延伸版本，用法和pycrypto一样
# 建议直接在python的安装目录的Lib\site-packages\安装pycryptodome
class CbcModel:
    def __init__(self, key, iv):
        # 初始化密钥key
        self.key = self.check_key_and_iv(key)
        # 初始化加密模式
        self.model = AES.MODE_CBC
        # 初始化偏移量iv
        self.iv = self.check_key_and_iv(iv)
        # 实例化aes对象，用于加解密
        self.aes = AES.new(self.key, self.model, self.iv)

    # 检查密钥key和偏移量iv的长度和数据类型
    def check_key_and_iv(self, key_or_iv_value):
        try:
            if isinstance(key_or_iv_value, bytes):
                # isinstance()函数用于判断一个对象是否是一个已知的类型，类似type()
                # isinstance()与type()区别：
                #         type()不会认为子类是一种父类类型，不考虑继承关系
                #         isinstance()会认为子类是一种父类类型，考虑继承关系
                assert len(key_or_iv_value) in [16, 24, 32]
                return key_or_iv_value
            elif isinstance(key_or_iv_value, str):
                assert len(key_or_iv_value.encode()) in [16, 24, 32]
                # encode()已指定的编码格式编码字符串，默认使用UTF-8
                return key_or_iv_value.encode()
            else:
                raise Exception("输入的密钥key或偏移量iv的值必须为bytes或str，不能为{}".format(type(key_or_iv_value)))
        except AssertionError:
            print("输入的密钥key或偏移量iv的长度不正确!")

    # 检查参数par的长度和数据类型
    def check_par(self, par):
        if isinstance(par, dict):
            par_str = str(par)
            par_byt = par_str.encode()
            while len(par_byt) % 16 != 0:
                par_byt += b"\x00"
            return par_byt

    # CBC模式加密
    def cbc_encrypt(self, par_data):
        encrypt_data = self.check_par(par_data)
        # 加密数据
        encrypt_text = self.aes.encrypt(encrypt_data)
        # 使用b64encode编码字符串
        base64_text = base64.b64encode(encrypt_text)
        # 返回解码后的字符串
        return base64_text.decode()

    # CBC模式解密
    def cbc_decrypt(self, decrypt_data):
        # 使用b64decode解码字符串
        base64_text = base64.b64decode(decrypt_data.encode())
        # 解密数据
        decrypt_text = self.aes.decrypt(base64_text)
        # 去掉填充的字符
        par_data = decrypt_text.strip(b"\x00")
        # 返回解码后的字符串
        return par_data.decode()


class EcbModel:
    def __init__(self, key):
        # 初始化密钥
        self.key = key.encode()
        # 初始化加密模式
        self.model = AES.MODE_ECB
        # 实例化aes对象，用于加解密
        self.aes = AES.new(self.key, self.model)

    # 检查加密参数是否满足16的倍数，不满足就填充
    def check_par(self, par):
        # 将加密字符串转为字节，并计算字节长度
        par_len = len(par.encode())
        # 初始化数据大小，固定为16位
        data_size = AES.block_size
        # 计算加密字节长度与16相差多少个字节
        check_par = data_size - (par_len % data_size)
        encrypt_data = par + (chr(check_par) * check_par)
        # chr():用一个范围在range(256)内的整数作为参数，返回一个对应的字符，超出范围将引发ValueError异常。返回值是当前整数对应的ASCII字符。
        # chr(check_par)*check_par:复制check_par位当前整数对应的ASCII字符。
        return encrypt_data

    # ECB模式加密
    def ecb_encrypt(self, encrypt_data):
        encrypt_text = self.aes.encrypt(self.check_par(encrypt_data).encode())
        base64_text = str(base64.b64encode(encrypt_text), encoding="utf8")
        return base64_text

    # ECB模式解密
    def ecb_decrypt(self, decrypt_data):
        base64_text = base64.decodebytes(decrypt_data.encode())
        encrypt_text = self.aes.decrypt(base64_text).decode()
        # 去除填充字符
        unpad = lambda data: data[0:-ord(data[-1])]
        # data[-1]:取encrypt_text文本的最后一位字符
        # ord(data[-1]):返回该字符的ASCII值
        # data[0:-ord(data[-1])]:从第一位开始取值（包含），截取到倒数第“-ord(data[-1])”位（不包含）
        #
        # lambda函数（匿名函数）介绍：是指一类无需定义标识符（函数名）的函数或子程序。
        #           lambda函数可以接收任意多个参数（包括可选参数）并返回单个表达式（只能有一个）的值。
        #           多个参数使用逗号分隔
        #           参数和表达式使用冒号分隔
        #           lamdba返回值是一个函数的地址也就是一个函数对象
        # ord():与chr()对应，参数为ASCII字符表中的字符，返回字符的ASCII值（0-255)
        return unpad(encrypt_text)


if __name__ == '__main__':
    cbc_data = {"cate_id": "", "sort": "-created_at", "page": 1, "per-page": 8, "timestamp": 1644917912961}
    test_en = CbcModel("c5FCFq49McM2XOjE", "c5FCFq49McM2XOjE").cbc_encrypt(cbc_data)
    test_de = CbcModel("c5FCFq49McM2XOjE", "c5FCFq49McM2XOjE").cbc_decrypt(test_en)
    print("CBC加密：" + test_en)
    print("CBC解密：" + test_de)

    ecb_data = '{"type_name":"homepage","template_id":"","apply_version":1,"timestamp":1645414514959}'
    test1_en = EcbModel("rokLISrskUVdGwCW").ecb_encrypt(ecb_data)
    test1_de = EcbModel("rokLISrskUVdGwCW").ecb_decrypt(test1_en)
    print("ECB加密：" + test1_en)
    print("ECB解密:" + test1_de)
