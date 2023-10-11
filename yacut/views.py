from flask import render_template, flash, redirect, url_for

from . import app, db

from .models import URLMap
from .forms import URLMapForm
from .utils import get_unique_short
from .constants import LOCALHOST


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLMapForm()
    if form.validate_on_submit():
        short = form.custom_id.data
        if short:
            if URLMap.query.filter_by(short=short).first() is not None:
                flash(f'Имя {short} уже занято!')
                return render_template('index.html', form=form)
            url = URLMap(
                original=form.original_link.data,
                short=short,
            )
            db.session.add(url)
            db.session.commit()
            return render_template('index.html',
                        form = form,
                        message='Ваша новая ссылка готова:',
                        link=LOCALHOST+url.short), 200
        url = URLMap(
            original=form.original_link.data,
            short=get_unique_short(),
        )
        db.session.add(url)
        db.session.commit()
        return render_template('index.html',
                    form = form,
                    message='Ваша новая ссылка готова:',
                    link=LOCALHOST+url.short), 200
    return render_template('index.html', form=form)


@app.route('/<path:short>')
def redirect_view(short):
    url = URLMap.query.filter_by(short=short).first()
    if not url:
        return render_template('404.html'), 404
    return redirect(url.original, 302)