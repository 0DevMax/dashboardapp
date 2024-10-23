import psycopg2
import os
from dotenv import load_dotenv
from flask import Flask, render_template, jsonify, Blueprint
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

# Rotas

## 1. Início
@app.route('/')
def index():
    return render_template("dashboard.html")

## 2. Encomendas
@app.route('/encomendas')
def rota_encomendas():
    return render_template("encomendas.html")


## 3. Catálogo
@app.route('/catalogo')
def rota_catalogo():
    return render_template("catalogo.html")


## 4. Estoques
@app.route('/estoques')
def rota_produtos():
    return render_template("estoques.html")

## 5. Vendas
@app.route('/vendas')
def rota_vendas():
    return render_template("vendas.html")


## 6. Relatórios
@app.route('/relatorios')
def rota_relatorios():
    return render_template("relatorios.html")



# Função para retornar os dados dos relatórios
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


#Função para retornar os dados do catálogo
def obter_dados_catalogo():
    dados_retornados_catalogo = []

    with conn.cursor() as cur:
        query_produtos = "SELECT id, nome_produto, preco, quantidade, categoria FROM produtos;"
        cur.execute(query_produtos)
        for row in cur.fetchall():
            id, nome_produto, preco, quantidade, categoria = row
            dados_retornados_catalogo.append({
                'id': id,
                'nome_produto': nome_produto,
                'preco': float(preco),
                'quantidade': quantidade,
                'categoria': categoria
            })
    return dados_retornados_catalogo

api = Blueprint('api', __name__)

@api.route('/dashboard', methods=['GET'])
def dashboard_dados():
    try:
        dados = obter_dados_dashboard()
        return jsonify(dados)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@api.route('/catalogo', methods=['GET'])
def catalogo_dados():
    try:
        dados = obter_dados_catalogo()
        return jsonify(dados)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

app.register_blueprint(api, url_prefix='/api')

if __name__ == '__main__':
    app.run(port=7000, debug=True)
