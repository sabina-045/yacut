from random import choices
from string import ascii_letters, digits
from .error_handlers import InvalidAPIUsage
import re
from .models import URLMap


def get_unique_short():

    return (''.join(choices(ascii_letters + digits, k = 6)))


def check_errors(data):
    if data is None:
        raise InvalidAPIUsage('Отсутствует тело запроса')
    if 'url' not in data:
        raise InvalidAPIUsage('"url" является обязательным полем!')
    if not re.match(r'^(http:|https:)+[^\s]+[\w]', data['url']):
            raise InvalidAPIUsage('Введенные данные не похожи на URL')
    if 'custom_id' in data and data['custom_id']:
        if URLMap.query.filter_by(short=data['custom_id']).first() is not None:
            raise InvalidAPIUsage('Предложенный вариант короткой ссылки уже существует.')
        if len(data['custom_id']) > 16:
            raise InvalidAPIUsage('Указано недопустимое имя для короткой ссылки')
        if not re.match(r'^[a-zA-Z0-9]+$', data['custom_id']):
            raise InvalidAPIUsage('Указано недопустимое имя для короткой ссылки')

    return True
