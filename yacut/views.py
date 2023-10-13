from flask import render_template, flash, redirect

from . import app, db

from .models import URLMap
from .forms import URLMapForm
from .utils import get_unique_short, check_unique_short
from .constants import LOCALHOST


@app.route('/', methods=['GET', 'POST'])
def index_view():
    """Гл. страница с формой"""
    form = URLMapForm()
    if form.validate_on_submit():
        short = form.custom_id.data
        if short:
            unique_validation = check_unique_short(short)
            if unique_validation:
                flash('Предложенный вариант короткой ссылки уже существует.',
                      'short_category')
                return render_template('index.html', form=form)
            url = URLMap(
                original=form.original_link.data,
                short=short,
            )
            db.session.add(url)
            db.session.commit()
            return render_template(
                'index.html',
                form=form,
                message='Ваша новая ссылка готова:',
                link=LOCALHOST + url.short
            ), 200
        url = URLMap(
            original=form.original_link.data,
            short=get_unique_short(),
        )
        db.session.add(url)
        db.session.commit()
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
