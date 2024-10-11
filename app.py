import psycopg2
import os
import json
from dotenv import load_dotenv
from flask import Flask, render_template, jsonify, request


# Carregar as variáveis de ambiente (credenciais)
load_dotenv()

# Conexão com o banco de dados
def conexao_db():
    conn = psycopg2.connect(
        database=os.getenv("NAME"),
        user=os.getenv("USER"),
        password=os.getenv("PASSWORD"),
        port=os.getenv("PORT"),
        host=os.getenv("HOST")
    )
    return conn

app = Flask(__name__, statics="public")

# Rota principal
@app.route('/')
def index():
    return render_template("dashboard.html")

# Rota para retornar os dados usados no dashboard
def dashboard_dados():
    try:
        dados = get_dashboard_dados()
        return jsonify(dados)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
def get_dashboard_dados():
    dados_retornados = {}

    with get_conexao_db() as conn:
        with conn.cursor() as cur:
            # Consulta de vendas por categoria
            query_vendas = """
                              SELECT P.categoria, SUM(v.quantidade) AS total_vendido
                              FROM vendas v
                              JOIN produtos p ON v.produto_id = p.id
                              GROUP BY p.categoria
                              ORDER BY  total_vendido DESC
                        """
            cur.execute(query_vendas)
            dados_vendas = {}
            for row in cur.fetchall():
                categoria, total_vendido = row
                dados_vendas[categoria] = total_vendido
            dados_retornados['dadosVendas'] = dados_vendas
            
            # Consulta de vendas por dia
            query_vendas_dia = """
                            SELECT data, SUM(quantidade) AS total_quantidade
                            FROM vendas
                            GROUP by data
                            ORDER by data
            """


# Consulta
cursor.execute("SELECT * FROM vendas")

rows = cursor.fetchmany(3)

for row in rows:
    print(row)

conn.close()



####

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("dashboard.html")

if __name__ == "__main__":
    app.run(debug=True)