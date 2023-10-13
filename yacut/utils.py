from random import choices
from string import ascii_letters, digits

from .constants import AUTHO_SHORT_MAX_SIZE
from .models import URLMap


def get_unique_short():
    """Создание уникального короткого идентификатора из 6 символов"""

    return (''.join(choices(
            ascii_letters + digits, k=AUTHO_SHORT_MAX_SIZE)))


def check_unique_short(short):
    """Проверка уникальности короткого идентиф."""
    if URLMap.query.filter_by(short=short).first() is not None:

        return True
