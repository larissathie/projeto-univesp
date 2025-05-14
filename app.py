from flask import Flask, render_template, request,url_for,flash,redirect
import os, datetime
import sqlite3
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from flask import session
from datetime import datetime
from werkzeug.exceptions import abort

cpfUsuario = 0
project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir,"database.db"))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'
app.config['SQLALCHEMY_DATABASE_URI'] = database_file
db = SQLAlchemy(app)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'grupopiunivespsala6grupo7@gmail.com'  
app.config['MAIL_PASSWORD'] = 'xxhchiyjtzalvbgs'  
app.config['MAIL_DEFAULT_SENDER'] = 'grupopiunivespsala6grupo7@gmail.com'

mail = Mail(app)

@app.route('/ajuda', methods=['GET', 'POST'])
def ajuda():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        telefone = request.form['telefone']
        mensagem = request.form['mensagem']

        msg = Message(subject='Nova mensagem do sistema de ajuda',
                      recipients=['grupopiunivespsala6grupo7@gmail.com'],  # E-mail de destino
                      body=f'Nome: {nome}\nEmail: {email}\nTelefone: {telefone}\n\nMensagem:\n{mensagem}')
        mail.send(msg)

        flash('Mensagem enviada com sucesso!', 'success')
        return redirect(url_for('ajuda'))
    return render_template('ajuda.html') 

class Usuario(db.Model):
    __tablename__ = 'moradores'
    cpf = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    apartamento = db.Column(db.String(10), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    senha = db.Column(db.String(100), nullable=False)

class Familiar(db.Model):
    __tablename__ = 'visitantes_apartamento'
    cpf_visitante = db.Column(db.Integer, primary_key=True)
    cpf_morador = db.Column(db.Integer, db.ForeignKey('moradores.cpf'), nullable=False)
    nome = db.Column(db.String(50), nullable=False)
    apartamento = db.Column(db.String(10), nullable=False)

    morador = db.relationship('Usuario', backref=db.backref('familiares', lazy=True))

class ConvidadoEvento(db.Model):
    __tablename__ = 'visitantes_eventos'
    cpf_visitante = db.Column(db.Integer, primary_key=True)
    cpf_morador = db.Column(db.Integer, db.ForeignKey('moradores.cpf'), nullable=False)
    nome = db.Column(db.String(50), nullable=False)
    apartamento = db.Column(db.String(10), nullable=False)

    morador = db.relationship('Usuario', backref=db.backref('convidados_eventos', lazy=True))


class Espaco(db.Model):
    __tablename__ = 'agendamento_evento'
    id = db.Column(db.Integer, primary_key=True)
    cpf_morador = db.Column(db.Integer, nullable=False)
    data = db.Column(db.DateTime, nullable = False)
    local = db.Column(db.Integer)
    ambientes = db.Column(db.String(50), nullable=False)
    apartamento = db.Column(db.String(10), nullable=False)
   



####### FUNÇÕES
### FUNÇÃO GET FAMILIAR
def get_familiar(familiar_cpf):
    familiar = Familiar.query.filter_by(cpf_visitante = familiar_cpf ).first()
    if familiar is None:
        abort(484)
    return familiar



#########  ROTAS
@app.route('/')
def index():
    return render_template('site.html')

@app.route('/criar_conta.html')
def criarconta():
    return render_template('criar_conta.html')

@app.route('/login', methods=['POST'])
def login():
    usuario = request.form['usuario']
    senha = request.form['senha']
    if not usuario or not senha:
        return render_template('site.html', error="Por favor, preencha usuário e senha!")
    user = Usuario.query.filter_by(email=usuario, senha=senha).first()
    if user:
        session['usuario_cpf'] = user.cpf
        session['usuario_nome'] = user.nome
        session['usuario_apartamento'] = user.apartamento #apresenta o nome do usuário no lado direito da tela
        return redirect(url_for('pagina_inicial')) 
    else:
        return render_template('site.html', error="Usuário ou senha incorretos!")

@app.route('/pinicial')
def pagina_inicial():
    cpfUsuario = session.get('usuario_cpf')
    nome_usuario = session.get('usuario_nome')
    usuario_cpf = session.get('usuario_cpf')
    usuario_apartamento = session.get('usuario_apartamento')
    return render_template('pinicial.html', nome=nome_usuario , cpf = usuario_cpf , apartamento = usuario_apartamento)

@app.route('/perfil_usuario')
def perfil_usuario():
    return render_template('perfil-usuario.html')

@app.route('/cadastrar_convidados', methods=['GET', 'POST'])
def cadastrar_convidados():
    if 'usuario_cpf' not in session:
        return redirect(url_for('index'))
    cpf_morador = session['usuario_cpf']
    convidados = ConvidadoEvento.query.filter_by(cpf_morador=cpf_morador).all()
    convidado_editado = None
    if request.method == 'POST':
        nome = request.form['nome']
        cpf_visitante = request.form.get('cpf_visitante')
        apartamento = request.form.get('apartamento')
        if cpf_visitante:
            convidado_editado = ConvidadoEvento.query.get(cpf_visitante)
            if convidado_editado and convidado_editado.cpf_morador == cpf_morador:
                convidado_editado.nome = nome
                convidado_editado.apartamento = apartamento
                db.session.commit()
        else:
            novo_convidado = ConvidadoEvento(
                nome=nome,
                apartamento=apartamento,
                cpf_morador=cpf_morador,
                cpf_visitante=datetime.datetime.now().timestamp()  # Simula ID único
            )
            db.session.add(novo_convidado)
            db.session.commit()

        return redirect(url_for('cadastrar_convidados'))

    return render_template('cadastrar_convidados.html', convidados=convidados, convidado_editado=convidado_editado)

@app.route('/excluir_convidado/<int:cpf_visitante>', methods=['POST'])
def excluir_convidado(cpf_visitante):
    convidado = ConvidadoEvento.query.get_or_404(cpf_visitante)
    if convidado.cpf_morador != session.get('usuario_cpf'):
        return redirect(url_for('cadastrar_convidados'))
    db.session.delete(convidado)
    db.session.commit()
    return redirect(url_for('cadastrar_convidados'))


##
### METODO PARA CRIAR USUÁRIOS / MORADORES
##
@app.route('/criar' , methods=['GET','POST'])
def cadastrar_usuario():
    print('entrou na função')
    if request.method == 'POST':
      print('deu o IF')
      form_nome = request.form['nome']
      form_email = request.form['email']
      form_cpf = request.form['cpf']
      form_ap = request.form['ap']
      form_senha = request.form['password']
      confirmaSenha = request.form['confirm-password']
    if not form_nome:
            print('deu o IFNOT')
            flash('O título é obrigatório!')
    else: 
          print('tentou cadastrar no banco')
          user = Usuario(cpf = form_cpf, nome = form_nome , apartamento = form_ap ,email = form_email, senha = form_senha)
          db.session.add(user)
          db.session.commit()
          print('cadastrou')
          return redirect(url_for('criarconta'))      
    return render_template('criarconta')


##
### ROTA PARA TELA DE CADASTRAR FAMILIARES
##
@app.route('/cadastrar_familiares', methods=['GET', 'POST'])
def cadastrar_familiares():
    cpf_morador = session.get('usuario_cpf')
    familiares = Familiar.query.all()
    return render_template('cadastrar_familiares.html', familiares=familiares)

##
### ROTA PARA TELA DE CADASTRAR EVENTOS
##
@app.route('/cadastro_evento', methods=['GET', 'POST'])
def evento():
    nome_usuario = session.get('usuario_nome')
    cpf_morador = session.get('usuario_cpf')
    ap_morador = session.get('usuario_apartamento')
    eventos = Espaco.query.filter_by(cpf_morador=cpf_morador).all()

    return render_template('cadastrar_evento.html', nome=nome_usuario , cpf = cpf_morador , apartamento = ap_morador , eventos = eventos)



##
### ROTA PARA ADICIONAR FAMILIAR
##
@app.route('/addFamiliar' , methods=['GET','POST'])
def adicionarFamiliar():
    print('entrou na função')   
   
    if request.method == 'POST':
     print('deu o IF')
     form_nome = request.form['nome']
     form_cpf = request.form['cpf']
     form_cpfMorador = session.get('usuario_cpf')
     form_ap = session.get('usuario_apartamento')
   
    if not form_nome:
      print('deu o IFNOT')
      flash('O título é obrigatório!')
    else: 
      print(cpfUsuario)
      print('tentou cadastrar no banco')
      familiar = Familiar(nome = form_nome ,cpf_morador = form_cpfMorador ,cpf_visitante = form_cpf , apartamento = form_ap)
      db.session.add(familiar)
      db.session.commit()
      print('cadastrou')
      return redirect(url_for('cadastrar_familiares'))         
    return render_template('cadastrar_familiares')

##
### ROTA PARA DELETAR UM FAMILIAR
##
@app.route('/<int:cpf>/delete', methods=('POST',))
def delete(cpf):
    familiarExcluido = get_familiar(cpf)
    db.session.delete(familiarExcluido)
    db.session.commit()    
    return redirect(url_for('cadastrar_familiares'))

 ### ROTA PARA CADASTRAR CONVIDADOS CHURRASQUEIRA

@app.route('/cadastrar_convidados_churrasqueira', methods=['GET', 'POST'])
def cadastrar_convidados_churrasqueira():
    if 'usuario_cpf' not in session:
        return redirect(url_for('index'))

    cpf_morador = session.get('usuario_cpf')
    apartamento = session.get('usuario_apartamento')

    if request.method == 'POST':
        nome = request.form['nome']
        cpf = request.form['cpf']
        data_uso = request.form['data_uso']

        novo_convidado = ConvidadoEvento(
            nome=nome,
            cpf_morador=cpf_morador,
            apartamento=apartamento,
            cpf_visitante=int(datetime.datetime.now().timestamp()),  # ID simulado
            data_uso=data_uso
        )
        db.session.add(novo_convidado)
        db.session.commit()

        flash('Convidado adicionado com sucesso!', 'success')
        return redirect(url_for('cadastrar_convidados_churrasqueira'))

    convidados = ConvidadoEvento.query.filter_by(cpf_morador=cpf_morador).all()
    return render_template('cadastrar_convidados_churrasqueira.html', convidados=convidados) 

@app.route('/cadastrar_convidados_salao')
def cadastrar_convidados_salao():
    return render_template('cadastrar_convidados_salao.html')





##
### ROTA PARA ADICIONAR FAMILIAR
##
@app.route('/addEvento' , methods=['GET','POST'])
def adicionarEvento():
    print('entrou na função')   
   
    if request.method == 'POST':
     print('deu o IF')
     form_nome =session.get('usuario_nome')
     form_cpf = session.get('usuario_cpf')     
     form_ap = session.get('usuario_apartamento')
     form_data = request.form['data_uso']
     form_espaco = request.form['select']

     data_obj = datetime.strptime(form_data, '%Y-%m-%d').date()
   
    if not form_nome:
      print('deu o IFNOT')
      flash('O título é obrigatório!')

    else: 
      
      espaco = Espaco(cpf_morador = form_cpf, data = data_obj , local = 1 , ambientes = form_espaco , apartamento = form_ap)
      db.session.add(espaco)
      db.session.commit()
      print('cadastrou')
      return redirect(url_for('evento'))         
    return render_template('cevento')















if __name__ == '__main__':
    app.run(debug=True)
