from flask_wtf import FlaskForm
from wtforms import URLField, SubmitField, StringField
from wtforms.validators import DataRequired, Length, Optional, URL, Regexp

from .constants import REGEX_SHORT, SHORT_MIN_SIZE, SHORT_MAX_SIZE


class URLMapForm(FlaskForm):
    original_link = URLField(
        'Длинная ссылка',
        validators=[
            DataRequired(message='Обязательное поле'),
            URL(message='Поле для URL-адреса')]
    )
    custom_id = StringField(
        'Короткая ссылка',
        validators=[
            Optional(),
            Length(SHORT_MIN_SIZE, SHORT_MAX_SIZE,
                   message='Допускается не более 16 символов'),
            Regexp(regex=REGEX_SHORT, message='Допускаются только строчные,'
                   'прописные латинские символы и цифры')]
    )
    submit = SubmitField('Создать')
