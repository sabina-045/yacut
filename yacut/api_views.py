from flask import jsonify, request

from . import app
from .models import URLMap
from .utils import get_unique_short
from .models import URLMap
from .api_utils import check_errors, url_to_dict, url_from_dict
from .api_exeptions import InvalidAPIUsage


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
        url_from_dict(url=url, data_fields=data)

        return jsonify(url_to_dict(url)), 201


@app.route('/api/id/<path:short_id>/', methods=['GET'])
def get_original_link(short_id):
    """GET-запрос на получение длинной ссылки по короткому идентиф."""
    url = URLMap.query.filter_by(short=short_id).first()
    if url is None:
        raise InvalidAPIUsage('Указанный id не найден', 404)

    return jsonify({'url': url_to_dict(url)['url']}), 200
