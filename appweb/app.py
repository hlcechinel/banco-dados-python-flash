from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)

SECRET_KEY = "stringAleatoria"  #proteção contra ataques
app.secret_key = SECRET_KEY

engine = create_engine("sqlite:///lab05-flask.sqlite")
Session = sessionmaker(bind=engine)
Base = automap_base()
Base.prepare(engine,reflect=True)

Pessoa = Base.classes.Pessoa
Telefones = Base.classes.Telefones

@app.route('/listar')
def listar_pessoas():
    id = str(request.args.get('id'))
    sessionSQL = Session()

    if id == 'None':
        pessoas = sessionSQL.query(Pessoa).all()
        sessionSQL.close()
        return render_template('listar.html',lista_pessoas=pessoas)
    else:
       pessoa = sessionSQL.query(Pessoa).filter(Pessoa.idPessoa == id).first()
       if pessoa is not None:
           sessionSQL.delete(pessoa)
           sessionSQL.commit()
           sessionSQL.close()
           return redirect(url_for('listar_pessoas'))

@app.route('/inserir', methods=['GET', 'POST'])
def inserir():
    if request.method == 'GET':
        return render_template('inserir.html')
    else:
        sessionSQL = Session()

        nome = request.form['nome']
        pessoa = Pessoa()
        pessoa.nome = nome

        sessionSQL.add(pessoa)
        sessionSQL.commit()
        sessionSQL.close()

        return redirect(url_for('listar_pessoas'))

@app.route('/index')
@app.route('/')
def hello_world():
    return render_template('index.html',titulo="Título da Página")


if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)  #apache,nginx, GUnicorn na produção   host= para rodar em todas as interfaces, sem roda somente localhost, debug funciona no terminal


