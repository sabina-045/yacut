from datetime import datetime
import re

from . import db
from .constants import REGEX_URL, REGEX_SHORT
from .exceptions import InvalidValueError


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(), nullable=False)
    short = db.Column(db.String(16), nullable=False, unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def _check_regex_short(self, short):
        if not re.match(REGEX_SHORT, short):
            raise InvalidValueError(
                'Допускаются только строчные,'
                'прописные латинские символы и цифры')
        return short

    def _check_regex_original(self, original):
        if not re.match(REGEX_URL, original):
            raise InvalidValueError('Введенные данные не похожи на URL')
