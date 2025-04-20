from flask import Flask, render_template, request,url_for,flash,redirect
import os, datetime
import sqlite3
from flask_sqlalchemy import SQLAlchemy

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir,"database.db"))


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'
app.config['SQLALCHEMY_DATABASE_URI'] = database_file
db = SQLAlchemy(app)

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

@app.route('/ajuda.html')
def ajuda():
    return render_template('ajuda.html')

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
