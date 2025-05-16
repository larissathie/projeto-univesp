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
    admin = db.Column(db.String(3), nullable=False)

class Familiar(db.Model):
    __tablename__ = 'visitantes_apartamento'
    cpf_visitante = db.Column(db.Integer, primary_key=True)
    cpf_morador = db.Column(db.Integer, db.ForeignKey('moradores.cpf'), nullable=False)
    nome = db.Column(db.String(50), nullable=False)
    apartamento = db.Column(db.String(10), nullable=False)

    morador = db.relationship('Usuario', backref=db.backref('familiares', lazy=True))

class ConvidadoEvento(db.Model):
    __tablename__ = 'visitantes_eventos'
    id_visitante = db.Column(db.Integer, primary_key=True)
    id_agendamento = db.Column(db.Integer, db.ForeignKey('agendamento_evento.id'), nullable=False)   
    nome = db.Column(db.String(50), nullable=False)
    apartamento = db.Column(db.String(10), nullable=False)

class Espaco(db.Model):
    __tablename__ = 'agendamento_evento'
    id = db.Column(db.Integer, primary_key=True)
    cpf_morador = db.Column(db.Integer, nullable=False)
    data = db.Column(db.DateTime, nullable = False)
    local = db.Column(db.Integer)
    ambientes = db.Column(db.String(50), nullable=False)
    apartamento = db.Column(db.String(10), nullable=False)
    convidados = db.relationship('ConvidadoEvento', backref='evento', cascade='all, delete-orphan')
   

####### FUNÇÕES
### FUNÇÃO GET FAMILIAR
def get_familiar(familiar_cpf):
    familiar = Familiar.query.filter_by(cpf_visitante = familiar_cpf ).first()
    if familiar is None:
        abort(484)
    return familiar

### FUNÇÃO GET EVENTOS
def get_eventos(id):
    eventos = Espaco.query.filter_by(id = id).first()
    if eventos is None:
        abort(484)
    return eventos

### FUNÇÃO GET CONVIDADOS   
def get_convidados(id_agendamento):
    convidados = ConvidadoEvento.query.filter_by(id_agendamento = id_agendamento).all()
    if convidados is None:
        abort(484)
    return convidados

### FUNÇÃO GET CONVIDADO UNICO  
def get_convidado_unico(idConvidado):
    convidadoUnico = ConvidadoEvento.query.filter_by(id_visitante = idConvidado).first()
    if convidadoUnico is None:
        abort(484)
    return convidadoUnico


#########  ROTAS
@app.route('/')
def index():
    return render_template('site.html')

@app.route('/criar_conta.html')
def criarconta():
    return render_template('criar_conta.html')

@app.route('/pesquisa_acesso.html', methods=['GET','POST'])
def pesquisaEntrada():
    return render_template('pesquisa_acesso.html')

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
        session['usuario_admin'] = user.admin
        return redirect(url_for('pagina_inicial')) 
    else:
        return render_template('site.html', error="Usuário ou senha incorretos!")

@app.route('/pinicial')
def pagina_inicial():
    cpfUsuario = session.get('usuario_cpf')
    nome_usuario = session.get('usuario_nome')
    usuario_cpf = session.get('usuario_cpf')
    usuario_apartamento = session.get('usuario_apartamento')
    usuario_admin = session.get('usuario_admin')
    return render_template('pinicial.html', nome=nome_usuario , cpf = usuario_cpf , apartamento = usuario_apartamento, admin = usuario_admin)

@app.route('/perfil_usuario')
def perfil_usuario():
    return render_template('perfil-usuario.html')

##
### METODO PARA CRIAR USUÁRIOS / MORADORES
##
@app.route('/criar' , methods=['GET','POST'])
def cadastrar_usuario():
    print('entrou na função')
    if request.method == 'POST':
      form_nome = request.form['nome']
      form_email = request.form['email']
      form_cpf = request.form['cpf']
      form_ap = request.form['ap']
      form_senha = request.form['password']
      form_Admin = request.form['selectUser']
    if not form_nome:   
            flash('O nome é obrigatório!')
    else: 
          user = Usuario(cpf = form_cpf, nome = form_nome , apartamento = form_ap ,email = form_email, senha = form_senha, admin = form_Admin)
          db.session.add(user)
          db.session.commit()          
          return redirect(url_for('criarconta'))      
    return render_template('criarconta')

##
### ROTA PARA TELA DE CADASTRAR FAMILIARES
##
@app.route('/cadastrar_familiares', methods=['GET', 'POST'])
def cadastrar_familiares():
    cpf_morador = session.get('usuario_cpf')
    familiares = Familiar.query.filter_by(cpf_morador = cpf_morador).all()
    return render_template('cadastrar_familiares.html', familiares=familiares)

##
### ROTA PARA ADICIONAR FAMILIAR
##
@app.route('/addFamiliar' , methods=['GET','POST'])
def adicionarFamiliar():      
   
    if request.method == 'POST':     
     form_nome = request.form['nome']
     form_cpf = request.form['cpf']
     form_cpfMorador = session.get('usuario_cpf')
     form_ap = session.get('usuario_apartamento')
   
    if not form_nome:      
      flash('O título é obrigatório!')
    else: 
      print(form_cpfMorador)     
      familiar = Familiar(nome = form_nome ,cpf_morador = form_cpfMorador ,cpf_visitante = form_cpf , apartamento = form_ap)
      db.session.add(familiar)
      db.session.commit()      
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

##
### ROTA PARA TELA DE CADASTRAR EVENTOS
##
@app.route('/cadastro_evento', methods=['GET', 'POST'])
def evento():
    nome_usuario = session.get('usuario_nome')
    cpf_morador = session.get('usuario_cpf')
    ap_morador = session.get('usuario_apartamento')
    eventos = Espaco.query.filter_by(cpf_morador=cpf_morador).all()
    todosEventos = Espaco.query.all()

    return render_template('cadastrar_evento.html', nome=nome_usuario , cpf = cpf_morador , apartamento = ap_morador , eventos = eventos , todosEventos = todosEventos)

##
### ROTA PARA ADICIONAR EVENTO
##
@app.route('/addEvento' , methods=['GET','POST'])
def adicionarEvento():
    if request.method == 'POST':
     form_nome =session.get('usuario_nome')
     form_cpf = session.get('usuario_cpf')     
     form_ap = session.get('usuario_apartamento')
     form_data = request.form['data_uso']
     form_espaco = request.form['select']

     data_obj = datetime.strptime(form_data, '%Y-%m-%d').date()
  
    if not form_nome:      
      flash('O Nome é obrigatório!')
    else:       
      espaco = Espaco(cpf_morador = form_cpf, data = data_obj , local = 1 , ambientes = form_espaco , apartamento = form_ap)
      db.session.add(espaco)
      db.session.commit()      
      return redirect(url_for('evento'))         
    return render_template('evento')


#
## ROTA PARA DELETAR EVENTO
#
@app.route('/<int:id>/deleteEvento', methods=('POST',))
def deleteEvento(id):   
    EventoExcluido = get_eventos(id)       
    db.session.delete(EventoExcluido)
    db.session.commit()
    return redirect(url_for('evento'))


#
## Rota para tela de visitantes
#
@app.route('/cadastrar_visitantes_Evento.html/<int:id>')
def cadastrar_visitantes_Evento(id):
    eventoCarregado = get_eventos(id) 
    convidadosCarregados = get_convidados(id)
    return render_template('cadastrar_visitantes_Evento.html', evento = eventoCarregado , convidados = convidadosCarregados)

#
## Rota para adicionar visitantes ao evento
#
@app.route('/addVisitante/<int:id>' , methods=['GET','POST'])
def adicionarVisitante(id):
    if request.method == 'POST':
     
     eventoAtual = get_eventos(id)
     idEvento =  eventoAtual.id
     form_nome = request.form['nome_convidado']
     apartamento = eventoAtual.apartamento
     
    if not form_nome:      
      flash('O Nome é obrigatório!')
    else: 
           
      convidado = ConvidadoEvento(id_agendamento = idEvento, nome = form_nome , apartamento = apartamento)
      db.session.add(convidado)
      db.session.commit()
      return redirect(url_for('cadastrar_visitantes_Evento', id = idEvento))         
    return render_template('cadastrar_visitantes_Evento.html')

#
## ROTA PARA DELETAR CONVIDADO
#
@app.route('/<int:id>/deleteConvidado', methods=('POST',))
def deleteConvidado(id):
    convidadoExcluido = get_convidado_unico(id)    
    idEvento = convidadoExcluido.id_agendamento 
    db.session.delete(convidadoExcluido)
    db.session.commit()
    
    return redirect(url_for('cadastrar_visitantes_Evento', id = idEvento))


#
## ROTA PARA PESQUISAR ACESSO
#
@app.route('/pesquisaNome' , methods=['GET','POST'])
def pesquisaAcesso():    
    if request.method == 'POST':
     form_nome = request.form['nome'].strip()
     familiar = Familiar.query.filter_by(nome = form_nome ).all()        
    if familiar:                
        tipoDeAcesso = 'Familiar'
        return render_template('pesquisa_acesso.html', pessoa = familiar , tipoDePessoa = tipoDeAcesso )              
    else:
        print('Não achou na familia')
        convidado = ConvidadoEvento.query.filter_by(nome = form_nome).all()
    if convidado:        
        tipoDeAcesso = 'Convidado'
        convidadoEncontrado = ConvidadoEvento.query.filter_by(nome = form_nome).first()
        eventoEncontrado = Espaco.query.filter_by(id = convidadoEncontrado.id_agendamento).first()
        
        return render_template('pesquisa_acesso.html', pessoa = convidado , tipoDePessoa = tipoDeAcesso , evento = eventoEncontrado)              
        
    else:        
        return render_template('pesquisa_acesso.html', nome=form_nome)

if __name__ == '__main__':
    app.run(debug=True)
