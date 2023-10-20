from random import choices
from string import ascii_letters, digits
import re

from . import db
from .constants import (AUTHO_SHORT_MAX_SIZE, REGEX_URL,
                        REGEX_SHORT, SHORT_MAX_SIZE)
from .models import URLMap
from .exceptions import (InvalidOriginalValueError, InvalidShortValueError,
                         UniqueValueError)


def create_unique_short(original, short):
    """Создание уникального короткого идентификатора из 6 символов
    (если его нет) и сохранение экз модели в бд"""
    check_original_errors(original)
    if short:
        check_unique_short(short)
        check_short_errors(short)
    else:
        short = (''.join(choices(
            ascii_letters + digits, k=AUTHO_SHORT_MAX_SIZE)))
        check_unique_short(short)

    url = URLMap(original=original, short=short)

    db.session.add(url)
    db.session.commit()

    return url


def check_unique_short(short):
    """Проверка уникальности short."""
    if URLMap.query.filter_by(short=short).first() is not None:
        raise UniqueValueError('Значение неуникально')


def check_original_errors(original):
    """Валидация original."""
    if not re.match(REGEX_URL, original):
        raise InvalidOriginalValueError('Введенные данные не похожи на URL')


def check_short_errors(short):
    """Валидация short."""
    if (len(short) > SHORT_MAX_SIZE or
            not re.match(REGEX_SHORT, short)):
        raise InvalidShortValueError(
            'Указано недопустимое имя для короткой ссылки'
        )
