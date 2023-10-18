from random import choices
from string import ascii_letters, digits

from . import db
from .constants import AUTHO_SHORT_MAX_SIZE
from .models import URLMap
from .exceptions import InvalidValueError


def create_unique_short(url):
    """Создание уникального короткого идентификатора из 6 символов
    (если его нет) и сохранение экз модели в бд"""
    short = url.short
    if short:
        unique_validation = check_unique_short(short)
        if unique_validation:
            raise InvalidValueError('Значение неуникально')
        db.session.add(url)
        db.session.commit()

        return url
    else:
        new_short = (''.join(choices(
            ascii_letters + digits, k=AUTHO_SHORT_MAX_SIZE)))
        url = URLMap(original=url.original, short=new_short)
        db.session.add(url)
        db.session.commit()

        return url


def check_unique_short(short):
    """Проверка уникальности короткого идентиф."""
    if URLMap.query.filter_by(short=short).first() is not None:

        return True
