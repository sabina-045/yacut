from flask_wtf import FlaskForm
from wtforms import URLField, SubmitField, StringField
from wtforms.validators import DataRequired, Length, Optional, URL, Regexp


class URLMapForm(FlaskForm):
    original_link = URLField(
        'Длинная ссылка',
        validators=[
            DataRequired(message='Обязательное поле'),
            URL(message='Поле для URL-адреса'),
            ]
    )
    custom_id = StringField(
        'Короткая ссылка',
         validators=[
            Optional(),
            Length(1, 16, message='Допускается не более 16 символов'),
            Regexp(regex=r'^[a-zA-Z0-9]+$', message='Допускаются только строчные, прописные латинские символы и цифры')
            ]
    )
    submit = SubmitField('Создать')
