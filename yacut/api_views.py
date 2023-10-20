from flask import jsonify, request

from . import app
from .service_views import create_unique_short
from .models import URLMap
from .api_utils import url_to_dict
from .api_exeptions import InvalidAPIUsage
from .exceptions import (InvalidShortValueError, UniqueValueError,
                         InvalidOriginalValueError)


@app.route('/api/id/', methods=['POST'])
def create_short_link():
    """POST-запрос на создание короткой ссылки"""
    data = request.get_json()
    if data is None:
        raise InvalidAPIUsage('Отсутствует тело запроса')
    if 'url' not in data:
        raise InvalidAPIUsage('"url" является обязательным полем!')

    try:
        url = create_unique_short(
            original=data['url'], short=data.get('custom_id'))
    except InvalidOriginalValueError:
        raise InvalidAPIUsage('Введенные данные не похожи на URL')
    except InvalidShortValueError:
        raise InvalidAPIUsage('Указано недопустимое имя для короткой ссылки')
    except UniqueValueError:
        raise InvalidAPIUsage(
            'Предложенный вариант короткой ссылки уже существует.'
        )
    else:
        return jsonify(url_to_dict(url)), 201


@app.route('/api/id/<path:short_id>/', methods=['GET'])
def get_original_link(short_id):
    """GET-запрос на получение длинной ссылки по короткому идентиф."""
    url = URLMap.query.filter_by(short=short_id).first()
    if url is None:
        raise InvalidAPIUsage('Указанный id не найден', 404)

    return jsonify({'url': url_to_dict(url)['url']}), 200
