from flask import Blueprint, request, render_template, url_for, redirect, flash
from flask_login import login_user, current_user, logout_user, login_required
from database import session #Importando do arquivo INIT da pasta database, por isso não preciso especificar arquivo
from models.emprestimos import Emprestimos #importando classe emprestimos do arquivo models/emprestimos
from models.livros import Livros 

emprestimos_bp = Blueprint(name='emprestimos', #Valores explicados no arquivo mvc.md
                        import_name=__name__,
                        template_folder="templates",
                        url_prefix="/emprestimos")

@emprestimos_bp.route('/cadastro')
@login_required
def cadastro():
    livros = session.query(Livros).all() #SELECT * FROM livros
    return render_template('emprestimos/cadastro.html', livros=livros)

@emprestimos_bp.route('/emprestar/<int:livro_id>')
@login_required
def emprestar_livro(livro_id):
    livro = session.query(Livros).get(livro_id)

    if not livro:
        return redirect(url_for('emprestimos.cadastro'))

    novo_emprestimo = Emprestimos(livro_id=livro.id, usuario_id=current_user.id)
    session.add(novo_emprestimo)
    session.commit()

    flash(f"Empréstimo do livro '{livro.nome}' realizado com sucesso!", "success")
    return redirect(url_for('index'))

