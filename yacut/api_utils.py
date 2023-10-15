import re

from . import db
from .api_exeptions import InvalidAPIUsage
from .models import URLMap
from .constants import REGEX_URL, REGEX_SHORT, SHORT_MAX_SIZE, FIELDS, LOCALHOST


def check_errors(data):
    """Проверка наличия ошибок при создании короткой ссылки"""
    if data is None:
        raise InvalidAPIUsage('Отсутствует тело запроса')
    if 'url' not in data:
        raise InvalidAPIUsage('"url" является обязательным полем!')
    if not re.match(REGEX_URL, data['url']):
        raise InvalidAPIUsage('Введенные данные не похожи на URL', 404)
    if 'custom_id' in data and data['custom_id']:
        if URLMap.query.filter_by(short=data['custom_id']).first() is not None:
            raise InvalidAPIUsage('Предложенный вариант короткой ссылки уже существует.')
        if len(data['custom_id']) > SHORT_MAX_SIZE:
            raise InvalidAPIUsage('Указано недопустимое имя для короткой ссылки')
        if not re.match(REGEX_SHORT, data['custom_id']):
            raise InvalidAPIUsage('Указано недопустимое имя для короткой ссылки')

    return True


def url_to_dict(url):
    """Сериализация"""
    return dict(
        url=url.original,
        short_link=LOCALHOST + url.short,
    )


def url_from_dict(url, data_fields):
    """Десериализация"""
    for field in FIELDS:
        if FIELDS[field] in data_fields:
            data_field = FIELDS[field]
            setattr(url, field, data_fields[data_field])
    db.session.add(url)
    db.session.commit()
