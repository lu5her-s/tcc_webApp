from django import template

register = template.Library()

@register.filter(name='has_group')
def has_group(user, group_name):
    group = user.groups.filter(name=group_name).exists()
    return group

@register.filter(name='in_status')
def in_status(obj, status):
    qs = obj.filter(status=status)
    return qs

@register.filter(name='obj_counter')
def obj_counter(obj):
    count = obj.count()
    return count

@register.filter(name='in_type')
def in_type(obj, type):
    qs = obj.filter(type=type)
    return qs

@register.filter
def thaidate(var):
	n = ['มกราคม', 'กุมภาพันธ์', 'มีนาคม', 'เมษายน', 'พฤษภาคม', 'มิถุนายน', 'กรกฎาคม', 'สิงหาคม', 'กันยายน', 'ตุลาคม', 'พฤษศจิกายน', 'ธันวาคม']
	d = var.day
	m = n[var.month - 1 ]
	y = var.year + 543
	return f'{d} {m} {y}'

@register.filter
def thaiyear(var):
	#n = ['มกราคม', 'กุมภาพันธ์', 'มีนาคม', 'เมษายน', 'พฤษภาคม', 'มิถุนายน', 'กรกฎาคม', 'สิงหาคม', 'กันยายน', 'ตุลาคม', 'พฤษศจิกายน', 'ธันวาคม']
	#d = var.day
	#m = n[var.month - 1 ]
	y = var + 543
	return f'{y}'


def number_format(num, places=0):
    return '{:20,.2f}'.format(num)
# fork by http://justmindthought.blogspot.com/2012/12/code-php.html

@register.filter
def ThaiBahtConversion(amount_number):
    amount_number = number_format(amount_number, 2).replace(" ", "")
    pt = amount_number.find(".")
    number, fraction = "", ""
    amount_number1 = amount_number.split('.')
    if (pt == False):
        number = amount_number
    else:
        amount_number = amount_number.split('.')
        number = amount_number[0]
        fraction = int(amount_number1[1])
    ret = ""
    number = eval(number.replace(",", ""))
    baht = ReadNumber(number)
    if (baht != ""):
        ret += baht + "บาท"
    satang = ReadNumber(fraction)
    if (satang != ""):
        ret += satang + "สตางค์"
    else:
        ret += "ถ้วน"
    return ret

# อ่านจำนวนตัวเลขภาษาไทย


def ReadNumber(number):
    """อ่านจำนวนตัวเลขภาษาไทย รับค่าเป็น ''float'' คืนค่าเป็น  ''str''"""
    position_call = ["แสน", "หมื่น", "พัน", "ร้อย", "สิบ", ""]
    number_call = [
        "",
        "หนึ่ง",
        "สอง",
        "สาม",
        "สี่",
        "ห้า",
        "หก",
        "เจ็ด",
        "แปด",
        "เก้า"]
    number = number
    ret = ""
    if (number == 0):
        return ret
    if (number > 1000000):
        ret += ReadNumber(int(number / 1000000)) + "ล้าน"
        number = int(math.fmod(number, 1000000))
    divider = 100000
    pos = 0
    while(number > 0):
        d = int(number / divider)
        if (divider == 10) and (d == 2):
            ret += "ยี่"
        elif (divider == 10) and (d == 1):
            ret += ""
        elif ((divider == 1) and (d == 1) and (ret != "")):
            ret += "เอ็ด"
        else:
            ret += number_call[d]
        if(d):
            ret += position_call[pos]
        else:
            ret += ""
        number = number % divider
        divider = divider / 10
        pos += 1
    return ret