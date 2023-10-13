import re

from flask import jsonify, request

from . import app, db
from .models import URLMap
from .utils import get_unique_short
from .constants import FIELDS
from .models import URLMap
from .constants import REGEX_URL, REGEX_SHORT, SHORT_MAX_SIZE, LOCALHOST


class InvalidAPIUsage(Exception):
    """Обработчики ошибок"""
    status_code = 400

    def __init__(self, message, status_code=None):
        super().__init__()
        self.message = message
        if status_code is not None:
            self.status_code = status_code

    def to_dict(self):

        return dict(message=self.message)


@app.errorhandler(InvalidAPIUsage)
def invalid_api_usage(error):

    return jsonify(error.to_dict()), error.status_code


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


@app.route('/api/id/', methods=['POST'])
def create_short_link():
    """POST-запрос на создание короткой ссылки"""
    data = request.get_json()
    validation_result = check_errors(data)
    if validation_result:
        url = URLMap()
        if 'custom_id' not in data or not data['custom_id']:
            unique_short = get_unique_short()
            url_from_dict(url=url, data_fields={
                'custom_id': unique_short, 'url': data['url']})
            db.session.add(url)
            db.session.commit()

            return jsonify(url_to_dict(url)), 201

        url_from_dict(url=url, data_fields=data)
        db.session.add(url)
        db.session.commit()

        return jsonify(url_to_dict(url)), 201


@app.route('/api/id/<path:short_id>/', methods=['GET'])
def get_original_link(short_id):
    """GET-запрос на получение длинной ссылки по короткому идентиф."""
    url = URLMap.query.filter_by(short=short_id).first()
    if url is None:
        raise InvalidAPIUsage('Указанный id не найден', 404)

    return jsonify({'url': url_to_dict(url)['url']}), 200
