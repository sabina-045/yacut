from .constants import LOCALHOST


def url_to_dict(url):
    """Сериализация"""
    return dict(
        url=url.original,
        short_link=LOCALHOST + url.short,
    )
