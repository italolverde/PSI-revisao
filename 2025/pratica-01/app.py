from flask import Flask, url_for, render_template, request, redirect, make_response

app = Flask(__name__)

@app.route('/') #Página inicial
def index(): #Chame a função da rota "/" de "index" por boa prática
    #Essa rota não precisa de métodos por que não tem nenhum formulário
    return render_template("index.html")

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'GET':
        return render_template("cadastro.html")
    
    else: #(Método POST) para receber os dados do form
        nome = request.form['nome'] 
        genero_favorito = request.form['genero_favorito']

        notificacoes = 'notificacoes' in request.form  # checkbox retorna se existe ou não
        #precisa ser desse jeito por que caso só dê o request.form e o checkbox estiver desmarcado, 
        #ele não vai retornar nada, resultando em um erro de chave não encontrada

        # Cria resposta com redirecionamento
        response = make_response(redirect(url_for('preferencias')))

        # Define cookies com validade de 7 dias (7*24*60*60 segundos)
        # O max_age é o tempo **EM SEGUNDOS** que o cookie vai durar
        response.set_cookie('nome', nome, max_age=7*24*60*60)
        response.set_cookie('genero_favorito', genero_favorito, max_age=7*24*60*60)
        response.set_cookie('notificacoes', str(notificacoes), max_age=7*24*60*60)

        return response


@app.route('/preferencias')
def preferencias():
    # Lê os cookies
    nome = request.cookies.get('nome')
    preferencia = request.cookies.get('genero_favorito')
    notificacoes = request.cookies.get('notificacoes')

    #Retorna a página de preferências com os dados do cookie
    return render_template("preferencias.html", nome=nome, preferencia=preferencia, notificacoes=notificacoes)

@app.route('/recomendar')
def recomendar():
    #Pega a consulta "genero" da URL
    genero = request.args.get('genero')

    #Criação da lista de filmes por gênero fixa
    filmes = {
        'acao': ['Mad Max: Estrada da Fúria', 'John Wick', 'Duro de Matar'],
        'comedia': ['Superbad', 'Apertem os Cintos... O Piloto Sumiu!', 'Os Caça-Fantasmas'],
        'drama': ['O Poderoso Chefão', 'Forrest Gump', 'Clube da Luta'],
        'terror': ['O Exorcista', 'A Noite dos Mortos-Vivos', 'O Iluminado'],
        'ficcao': ['Blade Runner', 'A Origem', 'Matrix'],
    }

    return render_template("recomendar.html", genero=genero, filmes=filmes.get(genero, []))

