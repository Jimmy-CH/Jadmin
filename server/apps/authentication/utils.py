
import base64
import random
import string
from io import BytesIO
from captcha.image import ImageCaptcha


def generate_captcha():
    # 生成 4 位随机字符
    chars = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
    image = ImageCaptcha(width=160, height=60)
    data = image.generate(chars)
    buffer = BytesIO()
    buffer.write(data.read())
    buffer.seek(0)
    img_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    return chars, img_base64
