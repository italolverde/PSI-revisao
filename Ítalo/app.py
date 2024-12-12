from flask import Flask, render_template, redirect, url_for
from controllers import users, books


# importar o bluprint e o login manager (PROVA)
from auth import bp
from auth.bp import login_manager

app = Flask(__name__)

# configurar secret key (PROVA)
app.config['SECRET_KEY'] = 'SEGREDO'
# inicializar o app no login manager (PROVA)
login_manager.init_app(app)
# registrando o blueprint (PROVA)


app.register_blueprint(users.bp)
app.register_blueprint(books.bp)
app.register_blueprint(bp.bp)

@app.route('/')
def index():
    return redirect(url_for('users.register'))