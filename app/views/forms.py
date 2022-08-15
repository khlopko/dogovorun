from wtforms import Form, StringField, validators


class JoinForm(Form):
    name = StringField('Имя', [validators.Length(min=3, max=25)])
    code = StringField('Код Игры', [validators.Length(min=10, max=10)])
