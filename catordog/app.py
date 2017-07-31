import logging
from flask import (
    Flask,
    render_template,
    redirect,
    url_for,
    request,
    flash,

)
from flask_wtf.csrf import CSRFProtect

from models import db, MyForm, Result

POSTGRES = {
        'user': 'postgres',
        'pw': 'postgres',
        'db': 'catordog',
        'host': 'localhost',
        'port': '5432',
}

app = Flask(__name__)
app.logger.setLevel(logging.DEBUG)
app.secret_key = 'OrmucoOrNothing'
app.config['SQLALCHEMY_DATABASE_URI'] = (
    'postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
csrf = CSRFProtect(app)
csrf.init_app(app)


@app.route('/', methods=['GET', 'POST'])
def main():
    form = MyForm(request.form)
    if request.method == 'POST' and form.validate():
        result = Result(
            form.name.data,
            form.color.data,
            form.cat_or_dog.data
        )
        db.session.add(result)
        db.session.commit()
        flash('Thanks for registering')
        return render_template('added.html', result=result)
    return render_template('index.html', form=form)



if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
