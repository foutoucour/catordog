"""
Entrypoint of the flask webapp.
"""
import datetime
import logging
import logging.handlers
import json
import os
from flask import (
    Flask, render_template, request, flash,
)
from flask_wtf.csrf import CSRFProtect

from models import db, MyForm, Result

POSTGRES = {
    'user': os.environ.get('DB_USER', 'postgres'),
    'pw': os.environ.get('DB_PASSWORD', 'postgres'),
    'db': os.environ.get('DB_NAME', 'catordog'),
    'host': os.environ.get('DB_HOST', 'localhost'),
    'port': os.environ.get('DB_PORT', '5432')
}
log_folder = "/var/log/catordog"
if not os.path.exists(log_folder):
    os.makedirs(log_folder)

app = Flask(__name__)
app.logger.setLevel(logging.DEBUG)
handler = logging.handlers.TimedRotatingFileHandler(os.path.join(log_folder, 'webapp.log'))
app.logger.addHandler(handler)
app.secret_key = 'OrmucoOrNothing'
app.config['SQLALCHEMY_DATABASE_URI'] = (
    'postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.logger.debug(
    json.dumps({
        "datetime": datetime.datetime.utcnow().isoformat(),
        "POSTGRES": POSTGRES,
        "app.config[SQLALCHEMY_DATABASE_URI]": app.config['SQLALCHEMY_DATABASE_URI'],
        "app.config[SQLALCHEMY_TRACK_MODIFICATIONS]": app.config['SQLALCHEMY_TRACK_MODIFICATIONS']
    })
)
db.init_app(app)
csrf = CSRFProtect(app)
csrf.init_app(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    """routing for index page."""
    return render_index(MyForm(request.form))


def render_index(form):
    """Condering the form, render the index or the added page.

    :param FlaskForm form: form used in index page.
    """
    if request.method == 'POST' and form.validate():
        app.logger.debug(
            json.dumps({
                "datetime": datetime.datetime.utcnow().isoformat(),
                "name": form.name.data,
                "color": form.color.data,
                "cat_or_dog": form.cat_or_dog.data
            })
        )
        result = Result(
            form.name.data,
            form.color.data,
            form.cat_or_dog.data
        )
        db.session.add(result)
        db.session.commit()
        app.logger.info(json.dumps({
            "datetime": datetime.datetime.utcnow().isoformat(),
            "result.id": result.id
        }))
        return render_template('added.html', result=result)
    return render_template('index.html', form=form)


if __name__ == '__main__':
    app.run(host="0.0.0.0")
