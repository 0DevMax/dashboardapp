import psycopg2
import os
from dotenv import load_dotenv
from flask import Flask, render_template, jsonify, request
import datetime


# Carregar as credenciais nas variáveis de ambiente
load_dotenv()

# Conexão com o banco de dados
conn = psycopg2.connect(
    database=os.getenv("NAME"),
    user=os.getenv("USER"),
    password=os.getenv("PASSWORD"),
    port=os.getenv("PORT"),
    host=os.getenv("HOST")
)
cursor = conn.cursor()


app = Flask(__name__, static_folder="static")

# Rota inicial
@app.route('/')
def index():
    return render_template("dashboard.html")

# Função para retornar os dados
def obter_dados_dashboard():
    dados_retornados_completo = {}

    
    with conn.cursor() as cur:
        # Consulta de vendas por categoria
        query_vendas_categoria = """
                            SELECT P.categoria, SUM(v.quantidade) AS total_vendido
                            FROM vendas v
                            JOIN produtos p ON v.produto_id = p.id
                            GROUP BY p.categoria
                            ORDER BY total_vendido DESC
                    """
        cur.execute(query_vendas_categoria)
        dash1 = {}
        for row in cur.fetchall():
            categoria, total_vendido = row
            dash1[categoria] = total_vendido
        dados_retornados_completo['dadosPorCategoria'] = dash1
        
        # Consulta de vendas por dia
        query_vendas_dia = """
                        SELECT data, SUM(quantidade) AS total_quantidade
                        FROM vendas
                        GROUP by data
                        ORDER by data
        """
        cur.execute(query_vendas_dia)
        dash2 = {}
        for row in cur.fetchall():
            data, total_quantidade = row
            data_str = data.strftime('%Y-%m-%d') if isinstance(data, datetime.date) else str(data)
            dash2[data_str] = total_quantidade
        dados_retornados_completo['dadosPorDia'] = dash2

        return dados_retornados_completo


@app.route('/api/dashboard', methods=['GET'])
def dashboard_dados():
    try:
        dados = obter_dados_dashboard()
        return jsonify(dados)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(port=7000, debug=True)
