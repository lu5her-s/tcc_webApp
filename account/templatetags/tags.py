import math
from django import template
from django.db.models import Q
from textwrap import wrap
from asset.models import StockItem

register = template.Library()


@register.filter(name="has_group")
def has_group(user, group_name):
    group = user.groups.filter(name=group_name).exists()
    return group


@register.filter(name="in_status")
def in_status(obj, status):
    qs = obj.filter(status=status)
    return qs


@register.filter(name="obj_counter")
def obj_counter(obj):
    count = obj.count()
    return count


@register.filter(name="in_type")
def in_type(obj, type):
    qs = obj.filter(type=type)
    return qs


@register.filter
def thaidate(var):
    try:
        n = [
            "มกราคม",
            "กุมภาพันธ์",
            "มีนาคม",
            "เมษายน",
            "พฤษภาคม",
            "มิถุนายน",
            "กรกฎาคม",
            "สิงหาคม",
            "กันยายน",
            "ตุลาคม",
            "พฤษศจิกายน",
            "ธันวาคม",
        ]
        d = var.day
        m = n[var.month - 1]
        y = var.year + 543
        return f"{d} {m} {y}"
    except:
        return "-"


@register.filter
def thaiyear(var):
    # n = ['มกราคม', 'กุมภาพันธ์', 'มีนาคม', 'เมษายน', 'พฤษภาคม', 'มิถุนายน', 'กรกฎาคม', 'สิงหาคม', 'กันยายน', 'ตุลาคม', 'พฤษศจิกายน', 'ธันวาคม']
    # d = var.day
    # m = n[var.month - 1 ]
    try:
        y = var + 543
        return f"{y}"
    except:
        return "-"


@register.filter
def thaidate_short(var):
    try:
        if var:
            n = [
                "ม.ค.",
                "ก.พ",
                "มี.ค.",
                "เม.ย",
                "พ.ค.",
                "มิ.ย",
                "ก.ค.",
                "ส.ค.",
                "ก.ย",
                "ต.ค.",
                "พ.ย.",
                "ธ.ค.",
            ]
            d = var.day
            m = n[var.month - 1]
            y = var.year + 543
            return f"{d} {m} {y}"
        else:
            return "___/___/___"
    except:
        return "___/___/___"
    # if var:
    #     n = [
    #         "ม.ค.",
    #         "ก.พ",
    #         "มี.ค.",
    #         "เม.ย",
    #         "พ.ค.",
    #         "มิ.ย",
    #         "ก.ค.",
    #         "ส.ค.",
    #         "ก.ย",
    #         "ต.ค.",
    #         "พ.ย.",
    #         "ธ.ค.",
    #     ]
    #     d = var.day
    #     m = n[var.month - 1]
    #     y = var.year + 543
    #     return f"{d} {m} {y}"
    # else:
    #     return f"___/___/___"


def number_format(num, places=0):
    return "{:20,.2f}".format(num)


# fork by http://justmindthought.blogspot.com/2012/12/code-php.html


@register.filter(name="read_baht")
def ThaiBahtConversion(amount_number):
    amount_number = number_format(amount_number, 2).replace(" ", "")
    pt = amount_number.find(".")
    number, fraction = "", ""
    amount_number1 = amount_number.split(".")
    if pt == False:
        number = amount_number
    else:
        amount_number = amount_number.split(".")
        number = amount_number[0]
        fraction = int(amount_number1[1])
    ret = ""
    number = eval(number.replace(",", ""))
    baht = ReadNumber(number)
    if baht != "":
        ret += baht + "บาท"
    satang = ReadNumber(fraction)
    if satang != "":
        ret += satang + "สตางค์"
    else:
        ret += "ถ้วน"
    return ret


# อ่านจำนวนตัวเลขภาษาไทย


def ReadNumber(number):
    """อ่านจำนวนตัวเลขภาษาไทย รับค่าเป็น ''float'' คืนค่าเป็น  ''str''"""
    position_call = ["แสน", "หมื่น", "พัน", "ร้อย", "สิบ", ""]
    number_call = ["", "หนึ่ง", "สอง", "สาม", "สี่", "ห้า", "หก", "เจ็ด", "แปด", "เก้า"]
    number = number
    ret = ""
    if number == 0:
        return ret
    if number > 1000000:
        ret += ReadNumber(int(number / 1000000)) + "ล้าน"
        number = int(math.fmod(number, 1000000))
    divider = 100000
    pos = 0
    while number > 0:
        d = int(number / divider)
        if (divider == 10) and (d == 2):
            ret += "ยี่"
        elif (divider == 10) and (d == 1):
            ret += ""
        elif (divider == 1) and (d == 1) and (ret != ""):
            ret += "เอ็ด"
        else:
            ret += number_call[d]
        if d:
            ret += position_call[pos]
        else:
            ret += ""
        number = number % divider
        divider = divider / 10
        pos += 1
    return ret


@register.filter(name="split")
def split(value, key):
    return value.split(key)


@register.filter
def text_wrap(text, width=25):
    return " ".join(wrap(text, width))


@register.filter(name="fuel")
def get_fuel(fuel_now, fuel_max):
    current = (fuel_now / fuel_max) * 100
    return current


@register.filter(name="available")
def available(obj):
    qs = obj.filter(
        Q(status=StockItem.Status.AVAILABLE) | Q(status=StockItem.Status.HOLD)
    )
    return qs


@register.filter(name="count")
def count(obj):
    count = obj.count()
    return count
