from flask import render_template, flash, redirect

from . import app
from .models import URLMap
from .forms import URLMapForm
from .service_views import create_unique_short
from .constants import LOCALHOST
from .exceptions import UniqueValueError


@app.route('/', methods=['GET', 'POST'])
def index_view():
    """Гл. страница с формой"""
    form = URLMapForm()
    if form.validate_on_submit():
        try:
            url = create_unique_short(original=form.original_link.data,
                                      short=form.custom_id.data)
        except UniqueValueError:
            flash('Предложенный вариант короткой ссылки уже существует.',
                  'short_category')

            return render_template('index.html', form=form)

        return render_template(
            'index.html',
            form=form,
            message='Ваша новая ссылка готова:',
            link=LOCALHOST + url.short
        ), 200

    return render_template('index.html', form=form)


@app.route('/<path:short>')
def redirect_view(short):
    """Переадресация короткой ссылки на основной URL"""
    url = URLMap.query.filter_by(short=short).first()
    if not url:

        return render_template('404.html'), 404

    return redirect(url.original, 302)
