from flask import Flask, render_template, request,url_for,flash,redirect
import os, datetime
import sqlite3
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message

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
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(40), nullable = False)
    email = db.Column(db.String(40), nullable = False)
    cpf = db.Column(db.String(40), nullable = False)
    senha = db.Column(db.String(40), nullable = False)

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

    user = Usuario.query.filter_by(nome=usuario, senha=senha).first()
    
    if user:
        return redirect(url_for('pagina_inicial')) 
    else:
        return render_template('site.html', error="Usuário ou senha incorretos!")

@app.route('/pinicial')
def pagina_inicial():
    return render_template('pinicial.html')

@app.route('/perfil_usuario')
def perfil_usuario():
    return render_template('perfil-usuario.html')

@app.route('/cadastrar_familiares')
def cadastrar_familiares():
    return render_template('cadastrar_familiares.html')

@app.route('/cadastrar_convidados')
def cadastrar_convidados():
    return render_template('cadastrar_convidados.html')

if __name__ == '__main__':
    app.run(debug=True)
