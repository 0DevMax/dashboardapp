import psycopg2
import os
import datetime
import logging
import traceback
from dotenv import load_dotenv
from flask import Flask, render_template, jsonify, Blueprint, request

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    filename='application_debug.log')

# Carregar as credenciais nas variáveis de ambiente
load_dotenv()

# Função de conexão com o banco de dados
def conexao_db():
    conn = psycopg2.connect(
        database=os.getenv("NAME"),
        user=os.getenv("USER_DB"),
        password= os.getenv("PASSWORD"),
        port=os.getenv("PORT"),
        host=os.getenv("HOST")
    )
    return conn

app = Flask(__name__, static_folder="static")

@app.after_request
def add_security_headers(response):
    response.headers['Content-Security-Policy'] = (
        "default-src 'self'; "
        "script-src 'self' 'unsafe-inline' 'unsafe-eval' "
        "https://code.jquery.com https://cdn.datatables.net https://cdn.jsdelivr.net; "
        "script-src-elem 'self' https://code.jquery.com https://cdn.datatables.net https://cdn.jsdelivr.net; "
        "style-src 'self' 'unsafe-inline' https://cdn.datatables.net https://fonts.googleapis.com; "
        "style-src-elem 'self' https://fonts.googleapis.com; "
        "img-src 'self' data:; "
        "font-src 'self' data:; "
        "connect-src 'self'; "
    )
    return response


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
def rota_estoques():
    return render_template("estoques.html")

@app.route('/estoques/novo-item')
def rota_novo_produto():
    return render_template("estoques-novo-item.html")

@app.route('/estoques-produtos')
def rota_produtos():
    return render_template("estoques-produtos.html")

@app.route('/estoques-materiais')
def rota_materiais():
    return render_template("estoques-materiais.html")   # Estudar meio de reduzir /estoques/ a uma única página dinâmica

## 5. Vendas
@app.route('/vendas')
def rota_vendas():
    return render_template("vendas.html")

@app.route('/vendas-registros')
def rota_vendas_registros():
    return render_template("vendas-registros.html")

@app.route('/vendas-registrar')
def rota_vendas_registrar():
    return render_template("vendas-registrar.html")

## 6. Relatórios
@app.route('/relatorios')
def rota_relatorios():
    return render_template("relatorios.html")



# Função para retornar os dados dos relatórios
def obter_dados_dashboard():
    dados_retornados_completo = {}

    conn = conexao_db()
    cur = conn.cursor()
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
    conn = None
    cur = None

    try:
        conn = conexao_db()
        if not conn:
            raise Exception("Falha ao estabelecer conexão com o banco de dados")
        
        cur = conn.cursor()
        if not cur:
            raise Exception("Falha ao criar cursor do banco de dados")
        
        query_produtos = "SELECT id, nome_produto, preco, quantidade, categoria FROM produtos;"
        cur.execute(query_produtos)
        resultados = cur.fetchall()
        if not resultados:
            logging.warning("Nenhuym resultado encontrado na consulta de produtos")

        for row in resultados:
            try:
                id, nome_produto, preco, quantidade, categoria = row

                dados_retornados_catalogo.append({
                    'id': id,
                    'nome_produto': nome_produto,
                    'preco': float(preco),
                    'quantidade': quantidade,
                    'categoria': categoria
                })
            except Exception as row_error:
                logging.error(f"Erro ao processar linha: {row}. Erro: {row_error}")

        return dados_retornados_catalogo
    
    except psycopg2.Error as db_error:
        logging.error(f"Erro de banco de dados: {db_error}")
        logging.error(f"Código de erro: {db_error.pgcode}")
        logging.error(f"Detalhe do erro: {db_error.pgerror}")
        raise
    
    except Exception as e:
        logging.error(f"Erro inesperado: {e}")
        logging.error(traceback.format_exc())
        raise

    finally:
        try:
            if cur:
                cur.close()
            if conn:
                conn.close()
        except Exception as close_error:
            logging.error(f"Erro ao fechar conexão: {close_error}")

#Função para retornar os dados das vendas
def obter_dados_vendas():
    dados_retornados_vendas = []

    conn = conexao_db()
    cur = conn.cursor()
    query_vendas = "SELECT id, TO_CHAR(data, 'dd/mm/yyyy'), produto_id, quantidade FROM vendas;"
    cur.execute(query_vendas)
    for row in cur.fetchall():
        id, data, produto_id, quantidade = row
        dados_retornados_vendas.append({
            'id': id,
            'data': data,
            'produto_id': produto_id,
            'quantidade': quantidade
        })
    return dados_retornados_vendas


#Função para retornar os dados das encomendas
def obter_dados_encomendas():
    dados_retornados_encomendas = []

    conn = conexao_db()
    cur = conn.cursor()
    query_encomendas = "SELECT id, cliente, contato, produto, observações, qtd FROM encomendas;"
    cur.execute(query_encomendas)
    for row in cur.fetchall():
        id, cliente, contato, produto, observações, qtd = row
        dados_retornados_encomendas.append({
            'id': id,
            'cliente': cliente,
            'contato': contato,
            'produto': produto,
            'observações': observações,
            'qtd': qtd
        })
    return dados_retornados_encomendas
    
# Função para retornar os dados dos produtos
def obter_dados_produtos():
    dados_retornados_produtos = []

    conn = conexao_db()
    cur = conn.cursor()
    query_produtos = "SELECT id, nome_produto, preco, quantidade, categoria FROM produtos;"
    cur.execute(query_produtos)
    for row in cur.fetchall():
        id, nome_produto, preco, quantidade, categoria = row
        dados_retornados_produtos.append({
            'id': id,
            'nome_produto': nome_produto,
            'preco': preco,
            'quantidade': quantidade,
            'categoria': categoria
        })
    return dados_retornados_produtos


# Função para retornar dados dos materiais
def obter_dados_materiais():
    dados_retornados_materiais = []

    conn = conexao_db()
    cur = conn.cursor()
    query_materiais = "SELECT id, nome_material, fornecedor, qtd, preco, custo_total,data FROM materiais;"
    cur.execute(query_materiais)
    for row in cur.fetchall():
        id, nome_material, fornecedor, qtd, preco, custo_total, data = row
        dados_retornados_materiais.append({
            'id': id,
            'nome_material': nome_material,
            'fornecedor': fornecedor,
            'qtd': qtd,
            'preco': preco,
            'custo_total': custo_total,
            'data': data,
        })
    return dados_retornados_materiais


# API

api = Blueprint('api', __name__)

@api.route('/dashboard', methods=['GET'])
def dashboard_dados():
    try:
        dados = obter_dados_dashboard()
        return jsonify(dados)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@api.route('/catalogo')
def catalogo_dados():
    try:
        dados =obter_dados_catalogo()
        return jsonify(dados)
    
    except psycopg2.Error as db_error:
        return jsonify({
            'error': 'Erro de banco de dados',
            'details': str(db_error),
            'error_code': getattr(db_error, 'pgcode', 'Unknown')
        }), 500
    
    except Exception as e:
        logging.error(f"Erro na rota de catálogo: {traceback.format_exc()}")
        return jsonify({
            'error': 'Erro interno do servido',
            'details': str(e)
        }), 500
    
@api.route('/vendas-registros')
def vendas_dados():
    try:
        dados = obter_dados_vendas()
        return jsonify(dados)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@api.route('/encomendas')
def encomendas_dados():
    try:
        dados = obter_dados_encomendas()
        return jsonify(dados)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@api.route('/encomendas/adicionar', methods=['POST'])
def adicionar_encomenda():
    try:
        dados = request.get_json()

        # Desempacotar dados
        cliente = dados['cliente']
        contato = dados['contato']
        produto = dados['produto']
        observacoes = dados['observacoes']
        qtd = dados['quantidade']


        conn = conexao_db()
        cur = conn.cursor()

        query = """
            INSERT INTO encomendas (cliente, contato, produto, observações, qtd) 
            VALUES (%s, %s, %s, %s, %s);
        """
        cur.execute(query, (cliente, contato, produto, observacoes, qtd))
        conn.commit()           

        cur.close()
        conn.close()

        return jsonify({'message': 'Encomenda adicionada com sucesso'}), 201
    
    except Exception as e:
        print(f"Erro ao adicionar encomenda: {str(e)}")
        return jsonify({'error': str(e)}), 500
    
@api.route('/estoques-produtos')
def produtos_dados():
    try:
        dados = obter_dados_produtos()
        return jsonify(dados)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@api.route('/estoques-materiais')
def materiais_dados():
    try:
        dados = obter_dados_materiais()
        return jsonify(dados)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

app.register_blueprint(api, url_prefix='/api')

if __name__ == '__main__':
    app.run(port=7000, debug=True)
