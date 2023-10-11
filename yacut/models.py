from datetime import datetime

from . import db
from .constants import FIELDS, LOCALHOST


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(), nullable=False)
    short = db.Column(db.String(16), nullable=False, unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def to_dict(self):
        """Сериализация"""
        return dict(
            url=self.original,
            short_link=LOCALHOST + self.short,
        )

    def from_dict(self, data_fields):
        """Десериализация"""
        for field in FIELDS:
            if FIELDS[field] in data_fields:
                data_field = FIELDS[field]
                setattr(self, field, data_fields[data_field])
