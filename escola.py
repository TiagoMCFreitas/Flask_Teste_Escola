import psycopg2 as ps
from flask import Flask, render_template, request,redirect

linhas  = []
class Aluno:
    def __init__(self, id:int, nome:str,idade:int,nota1:float,nota2:float,aprovacao_retorno:str):
        self.id = id
        self.nome = nome
        self.idade = idade
        self.nota1 = nota1
        self.nota2 = nota2
        self.aprovacao_retorno = aprovacao_retorno

           
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
        sql =f"""select * from relacao_alunos 
                 order by id"""
        cur.execute(sql)
        linha = cur.fetchall()
        i = 0
        con.commit()
        cur.close()
        return linha


app = Flask(__name__)

@app.route('/')
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
    return redirect(location='/')


app.run(debug = True)



        
