from flask import Flask, request, jsonify
from database import criar_tabelas, conectar_banco

app = Flask(__name__)

# Cria as tabelas ao iniciar
criar_tabelas()

# 1. Rota Principal (Para testar no navegador)
@app.route("/")
def inicio():
    return "<h1>Sistema de Gerenciamento Escolar Ativo!</h1><p>Acesse /alunos para ver a lista.</p>"

# 2. Rota para LISTAR os alunos no navegador (GET)
@app.route("/alunos", methods=["GET"])
def listar_alunos():
    conexao = conectar_banco()
    cursor = conexao.execute("SELECT * FROM alunos")
    alunos = [dict(linha) for linha in cursor.fetchall()]
    conexao.close()
    return jsonify(alunos), 200

# 3. Rota para CADASTRAR alunos (POST)
@app.route("/alunos", methods=["POST"])
def cadastrar_aluno():
    dados = request.get_json()

    nome = dados.get("nome")
    email = dados.get("email")
    idade = dados.get("idade")

    conexao = conectar_banco()
    try:
        conexao.execute(
            "INSERT INTO alunos (nome, email, idade) VALUES (?, ?, ?)",
            (nome, email, idade)
        )
        conexao.commit()
        conexao.close()
        return jsonify({"mensagem": "Aluno cadastrado com sucesso!"}), 201
    except Exception as e:
        conexao.close()
        return jsonify({"erro": str(e)}), 400

if __name__ == "__main__":
    app.run(debug=True)