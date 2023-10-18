from .constants import LOCALHOST, FIELDS


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
