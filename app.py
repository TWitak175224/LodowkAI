import os

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session
)

from flask_sqlalchemy import SQLAlchemy

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

app = Flask(__name__)
app.secret_key = 'super_secret_key_change_this'


basedir = os.path.abspath(os.path.dirname(__file__))

DB_FOLDER = os.path.join(basedir, 'baza')
UPLOAD_FOLDER = os.path.join(basedir, 'static', 'uploads')

os.makedirs(DB_FOLDER, exist_ok=True)
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


app.config['SQLALCHEMY_DATABASE_URI'] = (
    'sqlite:///' + os.path.join(DB_FOLDER, 'lodowka.db')
)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(300), nullable=False)


class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    ingredients = db.Column(db.Text, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


with app.app_context():
    db.create_all()


@app.route('/', methods=['GET', 'POST'])
def index():

    uploaded_image = None

    current_user = None

    if 'user_id' in session:
        current_user = User.query.get(session['user_id'])

    user_recipes = Recipe.query.all()

    if request.method == 'POST':


        if 'photo' in request.files:

            file = request.files['photo']

            if file.filename != '':

                path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
                file.save(path)

                uploaded_image = 'uploads/' + file.filename


        if 'recipe_name' in request.form:

            if 'user_id' not in session:
                return redirect(url_for('index'))

            new_recipe = Recipe(
                name=request.form.get('recipe_name'),
                ingredients=request.form.get('ingredients'),
                user_id=session['user_id']
            )

            db.session.add(new_recipe)
            db.session.commit()

            return redirect(url_for('index'))

    return render_template(
        'index.html',
        uploaded_image=uploaded_image,
        user_recipes=user_recipes,
        current_user=current_user
    )



@app.route('/register', methods=['POST'])
def register():

    email = request.form.get('email')
    password = request.form.get('password')

    if User.query.filter_by(email=email).first():
        return redirect(url_for('index'))

    user = User(
        email=email,
        password=generate_password_hash(password)
    )

    db.session.add(user)
    db.session.commit()

    session['user_id'] = user.id

    return redirect(url_for('index'))



@app.route('/login', methods=['POST'])
def login():

    email = request.form.get('email')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first()

    if user and check_password_hash(user.password, password):
        session['user_id'] = user.id

    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))



if __name__ == '__main__':
    app.run(debug=True)