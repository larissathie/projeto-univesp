from flask import Flask, render_template, request,url_for,flash,redirect
import os, datetime
import sqlite3
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from flask import session

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
    __tablename__ = 'moradores'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    cpf = db.Column(db.String(14), unique=True, nullable=False)
    apartamento = db.Column(db.String(10), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)

    usuario = db.relationship('Usuario', backref=db.backref('familiares', lazy=True))

class VisitanteApartamento(db.Model):
    __tablename__ = 'visitantes_apartamento'
    cpf_visitante = db.Column(db.Integer, primary_key=True)
    cpf_morador = db.Column(db.Integer, db.ForeignKey('moradores.cpf'), nullable=False)
    nome = db.Column(db.String(50))
    apartamento = db.Column(db.String(10))


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
        return redirect(url_for('pagina_inicial')) 
    else:
        return render_template('site.html', error="Usuário ou senha incorretos!")

@app.route('/pinicial')
def pagina_inicial():
    nome_usuario = session.get('usuario_nome')
    return render_template('pinicial.html', nome=nome_usuario)

@app.route('/perfil_usuario')
def perfil_usuario():
    return render_template('perfil-usuario.html')

@app.route('/cadastrar_familiares', methods=['GET', 'POST'])
def cadastrar_familiares():
    if 'usuario_id' not in session:
        return redirect(url_for('index'))

    usuario_id = session['usuario_id']
    familiares = Familiar.query.filter_by(usuario_id=usuario_id).all()

    familiar_editado = None
    if request.method == 'POST':
        nome = request.form['nome']
        familiar_id = request.form.get('familiar_id')

        if familiar_id:
            familiar_editado = Familiar.query.get(familiar_id)
            if familiar_editado and familiar_editado.usuario_id == usuario_id:
                familiar_editado.nome = nome
                db.session.commit()
        else:
            novo_familiar = Familiar(nome=nome, usuario_id=usuario_id)
            db.session.add(novo_familiar)
            db.session.commit()

        return redirect(url_for('cadastrar_familiares'))

    edit_id = request.args.get('edit')
    if edit_id:
        familiar_editado = Familiar.query.get(edit_id)
        if familiar_editado and familiar_editado.usuario_id != usuario_id:
            familiar_editado = None

    return render_template('cadastrar_familiares.html', familiares=familiares, familiar_editado=familiar_editado)

@app.route('/excluir_familiar/<int:id>', methods=['POST'])
def excluir_familiar(id):
    familiar = Familiar.query.get_or_404(id)
    if familiar.usuario_id != session.get('usuario_id'):
        return redirect(url_for('cadastrar_familiares'))

    db.session.delete(familiar)
    db.session.commit()
    return redirect(url_for('cadastrar_familiares'))


@app.route('/cadastrar_convidados')
def cadastrar_convidados():
    return render_template('cadastrar_convidados.html')

if __name__ == '__main__':
    app.run(debug=True)
