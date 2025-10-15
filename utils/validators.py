import re
from typing import Optional
from PIL import Image
import io

def validate_wallet_address(wallet: str) -> bool:
    if not wallet:
        return False

    wallet = wallet.strip()

    if len(wallet) < 10 or len(wallet) > 100:
        return False

    if not re.match(r'^[a-zA-Z0-9]+$', wallet):
        return False

    return True

def validate_image(file_data: bytes) -> tuple[bool, Optional[str]]:
    try:
        image = Image.open(io.BytesIO(file_data))

        if image.format not in ['JPEG', 'PNG', 'WEBP']:
            return False, "Неподдерживаемый формат изображения"

        if len(file_data) > 10 * 1024 * 1024:
            return False, "Размер изображения слишком большой"

        width, height = image.size
        if width < 100 or height < 100:
            return False, "Изображение слишком маленькое"

        if width > 4096 or height > 4096:
            return False, "Изображение слишком большое"

        return True, None

    except Exception as e:
        return False, f"Ошибка обработки изображения: {str(e)}"

def validate_price(price_str: str) -> tuple[bool, Optional[float]]:
    try:
        price = float(price_str.replace(',', '.'))
        if price <= 0:
            return False, None

        if price > 1000000:
            return False, None

        return True, price

    except (ValueError, TypeError):
        return False, None

def validate_order_id(order_id_str: str) -> tuple[bool, Optional[int]]:
    try:
        order_id = int(order_id_str)
        if order_id <= 0:
            return False, None

        return True, order_id

    except (ValueError, TypeError):
        return False, None

def validate_telegram_id(telegram_id: int) -> bool:
    return isinstance(telegram_id, int) and telegram_id > 0

def sanitize_text(text: str, max_length: int = 1000) -> str:
    if not text:
        return ""

    text = str(text).strip()

    text = re.sub(r'[<>&]', lambda m: {'<': '&lt;', '>': '&gt;', '&': '&amp;'}[m.group()], text)

    if len(text) > max_length:
        text = text[:max_length] + "..."

    return text

def validate_username(username: str) -> bool:
    if not username:
        return True

    username = username.strip().lstrip('@')

    if len(username) > 32:
        return False

    if not re.match(r'^[a-zA-Z0-9_]+$', username):
        return False

    return True