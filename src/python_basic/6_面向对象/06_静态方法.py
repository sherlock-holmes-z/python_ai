from datetime import datetime


class PersonUtils:
    # 静态方法
    # 不需要实例self或cls参数，接受到的参数都是自定义参数
    # 由于没有接收self和cla，所以内部不会访问任何类或实例的相关内容
    # 通常定义与类相关的工具方法
    @staticmethod
    def is_adult(year):
        now_year = datetime.now().year
        return now_year - year >= 18

    @staticmethod
    def mask_idcard(idcard):
        return idcard[:6] + "********" + idcard[-4:]


if __name__ == "__main__":
    print(PersonUtils.is_adult(1996))
    print(PersonUtils.mask_idcard("340421199601204010"))

    # 注意：通过实例也能调用静态方法，但不推荐
    person_utils = PersonUtils()
    print(person_utils.is_adult(2018))
