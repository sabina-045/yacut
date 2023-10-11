from flask import jsonify, request

from .models import URLMap
from . import app, db
from .error_handlers import InvalidAPIUsage
from .utils import check_errors, get_unique_short


@app.route('/api/id/', methods=['POST'])
def create_short_link():
    """Пост запрос на создание короткой ссылки"""
    data = request.get_json()
    validation_result = check_errors(data)
    if validation_result == True:
        url = URLMap()
        if 'custom_id' not in data or not data['custom_id']:
            unique_short = get_unique_short()
            url.from_dict({'custom_id':unique_short, 'url': data['url']})
            db.session.add(url)
            db.session.commit()

            return jsonify(url.to_dict()), 201

        url.from_dict(data)
        db.session.add(url)
        db.session.commit()

        return jsonify(url.to_dict()), 201


@app.route('/api/id/<path:short_id>/', methods=['GET'])
def get_original_link(short_id):
    """Гет запрос на получение длинный ссылки по короткому идент"""
    url = URLMap.query.filter_by(short=short_id).first()
    if url is None:
        raise InvalidAPIUsage('Указанный id не найден', 404)
    return jsonify({'url': url.to_dict()['url']}), 200
