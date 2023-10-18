import re

from flask import jsonify, request

from . import app
from .service_views import create_unique_short, check_unique_short
from .models import URLMap
from .api_utils import url_to_dict, url_from_dict
from .api_exeptions import InvalidAPIUsage
from .constants import REGEX_URL, REGEX_SHORT, SHORT_MAX_SIZE


@app.route('/api/id/', methods=['POST'])
def create_short_link():
    """POST-запрос на создание короткой ссылки"""
    data = request.get_json()

    if data is None:
        raise InvalidAPIUsage('Отсутствует тело запроса')
    if 'url' not in data:
        raise InvalidAPIUsage('"url" является обязательным полем!')
    if not re.match(REGEX_URL, data['url']):
        raise InvalidAPIUsage('Введенные данные не похожи на URL', 404)
    if 'custom_id' in data and data['custom_id']:
        if (len(data['custom_id']) > SHORT_MAX_SIZE or
                not re.match(REGEX_SHORT, data['custom_id'])):
            raise InvalidAPIUsage('Указано недопустимое имя для короткой ссылки')
        unique_validation = check_unique_short(data['custom_id'])
        if unique_validation:
            raise InvalidAPIUsage('Предложенный вариант короткой ссылки уже существует.')

    url = URLMap()
    url_from_dict(url=url, data_fields=data)
    url = create_unique_short(url)

    return jsonify(url_to_dict(url)), 201


@app.route('/api/id/<path:short_id>/', methods=['GET'])
def get_original_link(short_id):
    """GET-запрос на получение длинной ссылки по короткому идентиф."""
    url = URLMap.query.filter_by(short=short_id).first()
    if url is None:
        raise InvalidAPIUsage('Указанный id не найден', 404)

    return jsonify({'url': url_to_dict(url)['url']}), 200
