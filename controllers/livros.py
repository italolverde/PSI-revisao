from flask import Blueprint, request, render_template, url_for, redirect, flash
from flask_login import login_user, current_user, logout_user, login_required
from database import session #Importando do arquivo INIT da pasta database, por isso não preciso especificar arquivo
from models.livros import Livros #importando classe livros do arquivo models/livros

livros_bp = Blueprint(name='livros', #Valores explicados no arquivo mvc.md
                        import_name=__name__,
                        template_folder="templates",
                        url_prefix="/livros")

@livros_bp.route('/cadastro_livro', methods=['GET', 'POST'])
@login_required
def cadastro_livro():
    if request.method == 'POST':
        nome_livro = request.form.get('nome')

        if not nome_livro:
            flash("O nome do livro é obrigatório!", "danger")
            return redirect(url_for('livros.cadastro_livro'))

        novo_livro = Livros(nome=nome_livro)
        session.add(novo_livro)
        session.commit()

        flash("Livro cadastrado com sucesso!", "success")
        return redirect(url_for('livros.cadastro_livro'))

    return render_template('livros/cadastro_livro.html')