import psycopg2 as ps
from flask import Flask, render_template, request,redirect, flash

linhas = []
class Aluno:
    def __init__(self, id:int, nome:str,idade:int,nota1:float,nota2:float,aprovacao_retorno:str):
        self.id = id
        self.nome = nome
        self.idade = idade
        self.nota1 = nota1
        self.nota2 = nota2
        self.aprovacao_retorno = aprovacao_retorno
class Usuario:
    def __init__(self,login,senha,cpf):
        self.login = login
        self.senha = senha
        self.cpf = cpf    
    def setLogin(self,valor):
        self.login = valor
    def getLogin(self):
        return self.login
lista_usuario = []           

class Conexao():
    def getConnection():
        return ps.connect(host='localhost', database='Escola',user='postgres', password='tiago')

class AlunoDao(Conexao): 
    def fazer_media(self,Aluno):
        return (Aluno.nota1 + Aluno.nota2)/2

    def definir_aprovados_e_reprovados(self,Aluno):
        if self.fazer_media(Aluno) < 6:
            return 'Reprovado'
        else:
            return 'Aprovado'

    def insert(self,Aluno):
        con = Conexao.getConnection()
        cur = con.cursor()  
        sql = 'insert into relacao_alunos(nome,idade,nota,aprovacao)values(%s,%s,%s,%s)'
        tupla = (Aluno.nome,Aluno.idade,self.fazer_media(Aluno),self.definir_aprovados_e_reprovados(Aluno))
        cur.execute(sql,tupla)
        con.commit()
        cur.close()

    def select(self):
        con = Conexao.getConnection()
        cur = con.cursor()  
        sql =f"""select * from relacao_alunos order by id"""
        cur.execute(sql)
        linha = cur.fetchall()  
        con.commit()
        cur.close()
        return linha
    
class UsuarioDao(Conexao):
    def criar_usuarios(self,Usuario):
        con = Conexao.getConnection()
        cur = con.cursor()  
        sql = 'insert into usuarios(login,senha,cpf)values(%s,%s,%s)'
        tupla = (Usuario.login,Usuario.senha,Usuario.cpf)
        cur.execute(sql,tupla)
        con.commit()
        cur.close()
    def listar_usuarios(self):
        con = Conexao.getConnection()
        cur = con.cursor()  
        sql =f"""select * from usuarios"""
        cur.execute(sql)
        linha = cur.fetchall()
        i = 0
        for i in range(len(linha)):
            self.login  = linha[i][0] 
            self.senha  = linha[i][1] 
            self.cpf   = linha[i][2] 
            
        con.commit()
        cur.close()
        return linha
    

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
@app.route('/home')
def index():
    select = AlunoDao()
    return render_template('lista.html',titulo='Relacao nota/aluno',linha = select.select())

@app.route('/cadastro')
def tela_cadastro():
    return render_template('aluno_nota.html',titulo = 'Cadastro de notas')

@app.route('/criar',methods = ['POST', ])
def cadastro():
    nome = request.form['nome']
    idade = request.form['idade']
    nota1 = float(request.form['nota1'])
    nota2 = float(request.form['nota2']) 
    alunoDao = AlunoDao()
    aluno = Aluno(0,nome,idade,nota1,nota2,'')
    alunoDao.insert(aluno)
    return redirect(location='/home')

@app.route('/')
def realiza_login():
    return render_template('login.html')

@app.route('/autenticar', methods = ['POST', ])
def autenticar():  
    usuario = request.form['usuario']
    senha = request.form['senha']
    objetoDao = UsuarioDao()
    for i in range(len(objetoDao.listar_usuarios())):
        if usuario == objetoDao.listar_usuarios()[i][0] and senha == objetoDao.listar_usuarios()[i][1]:
            return redirect(location='/home')
    error = 'Usuário ou senha inválidos'
    return render_template('login.html',error=error)
    

        
@app.route('/usuarios')
def tela_usuarios():
    return render_template('cadastrar_usuarios.html')

@app.route('/cadastro_usuarios', methods = ['POST', ])
def cadastrar_usuarios():
    login = request.form['login']
    senha = request.form['senha']
    cpf = request.form['cpf']
    objetoUsuario = Usuario(login,senha,cpf)
    objetoDao = UsuarioDao()
    objetoDao.criar_usuarios(objetoUsuario)
    return redirect(location ='/')
app.run(debug = True)