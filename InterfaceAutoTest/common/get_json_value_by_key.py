# 根据key值去获取json文件中对应的value值

class GetJsonValue:
    # in_json 传入的json
    # target_key  目标key值
    # results = []    存放目标key值的value值的列表
    def get_json_value_by_key(self, in_json, target_key, results=None):
        if results is None:
            results = []
        # 通过isinstance()判断对象的变量类型
        if isinstance(in_json, dict):
            # 如果对象的变量类型为字典，则循环获取key
            for key in in_json.keys():
                # 根据key获取对应的value值
                value_data = in_json[key]
                # 回归当前key对应的value
                self.get_json_value_by_key(value_data, target_key, results=results)
                # 如果当前key与目标key相同就将当前key的value添加到输出列表
                if key == target_key:
                    results.append(value_data)
        # 通过isinstance()判断对象的变量类型是否为列表或元组
        elif isinstance(in_json, list) or isinstance(in_json, tuple):
            # 循环当前列表或元组
            for result_data in in_json:
                # 回归列表或元组的当前元素
                self.get_json_value_by_key(result_data, target_key, results=results)
        return results


if __name__ == '__main__':
    data = {
        "code": 200,
        "data": {
            "access_token": "rokLISrskUVdGwCWBPaOiwwDHVKXrkqh_7mRARadz18_1645414510",
            "expire_time": 259200,
            "info_platform": {
                "logo": "https://ztalycdn.maihuominiapps.com/images/temp/platform_logo.png",
                "title": "脉货",
                "is_agree": 1,
                "member": {
                    "id": 10000116,
                    "superior_id": "0",
                    "promo_code": "7mRARadz18",
                    "nickname": "大客户售后经理舒克"
                },
                "big_grade": 0,
                "cellphone": "18583181826",
                "created_at": 1644543218,
                "grade_at": 1645149087,
                "grade_id": 1000,
                "id": 10000116
            }
        }
    }
    result = GetJsonValue().get_json_value_by_key(data, "access_token")
    print(result)
