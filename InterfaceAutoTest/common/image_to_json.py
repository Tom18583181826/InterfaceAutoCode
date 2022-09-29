# 将图片转换成json数据
from json import dumps
from base64 import b64encode


class ImageToJson:
    def image_to_json(self, img_file_path, json_file_path):
        # rb---二进制模式读取图片文件，获取原始字节码
        with open(img_file_path, "rb") as img_file:
            byte_content = img_file.read()

        # 将原始字节码编码成base64字节码
        base64_bytes = b64encode(byte_content)

        # 将base64字节码解码成utf-8格式的字符串
        base64_string = base64_bytes.decode("utf-8")

        # 用字典保存数据
        img_dict = {"image_base64_string": base64_string}
        # 将字典转换成json格式，设置缩进为2个空格
        json_data = dumps(img_dict, indent=2)

        # 将json格式的数据保存在文件中
        with open(json_file_path, "w") as json_file:
            json_file.write(json_data)
