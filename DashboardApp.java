package com.extensao.dashboardapp;

import io.javalin.Javalin; // Importa a biblioteca Javalin para criar o servidor web
import java.sql.Connection; // Importa a classe Connection para gerenciar a conexão com o banco de dados
import java.sql.DriverManager; // Importa DriverManager para criar a conexão com o banco de dados
import java.sql.ResultSet; // Importa ResultSet para manipular os resultados de consultas SQL
import java.sql.SQLException; // Importa SQLException para tratar erros de SQL
import com.google.gson.JsonObject; // Importa JsonObject para criar e manipular objetos JSON
import io.github.cdimascio.dotenv.Dotenv; // Importa a biblioteca Dotenv para carregar variáveis de ambiente
import java.nio.file.Files; // Importa a classe Files para trabalhar com arquivos
import java.nio.file.Paths; // Importa a classe Paths para manipular caminhos de arquivos

public class DashboardApp {

    // Carrega as variáveis de ambiente do arquivo .env usando a biblioteca Dotenv
    private static final Dotenv dotenv = Dotenv.configure().load();
    
    // Recupera as credenciais do banco de dados a partir das variáveis de ambiente
    private static final String DB_URL = dotenv.get("DATABASE_URL");
    private static final String DB_USER = dotenv.get("USER");
    private static final String DB_PASSWORD = dotenv.get("PASSWORD");

    public static void main(String[] args) {
        // Inicializa o servidor Javalin, configurando para servir arquivos estáticos da pasta "public"
        Javalin app = Javalin.create(config -> {
            config.staticFiles.add("/public"); // Adiciona o diretório de arquivos estáticos (HTML, CSS, JS)
        }).start(7000); // Inicia o servidor na porta 7000
        
        // Define a rota principal ("/") que serve o arquivo HTML do dashboard
        app.get("/", ctx -> {
            ctx.contentType("text/html"); // Define o tipo de conteúdo como HTML
            ctx.result(Files.readString(Paths.get("src/main/resources/public/dashboard.html"))); // Carrega o HTML
        });
        
        // Rota que retorna dados do dashboard em formato JSON
        app.get("/api/dashboard", ctx -> {
            try {
                String data = getDashboardData(); // Chama a função que busca os dados do banco de dados
                ctx.json(data); // Retorna os dados no formato JSON
            } catch (Exception e) {
                e.printStackTrace(); // Imprime o erro no console
                ctx.status(500).result("Erro ao acessar o banco de dados: " + e.getMessage()); // Retorna erro HTTP 500
            }
        });

        // Rota de teste para verificar a conexão com o banco de dados
        app.get("/test-db", ctx -> {
            try {
                testDatabaseConnection(); // Chama a função que testa a conexão com o banco de dados
                ctx.result("Conexão com o banco de dados bem-sucedida!"); // Se funcionar, retorna essa mensagem
            } catch (Exception e) {
                e.printStackTrace(); // Imprime o erro no console
                ctx.status(500).result("Erro na conexão com o banco de dados: " + e.getMessage()); // Retorna erro 500 se falhar
            }
        });
    }

    // Função que testa a conexão com o banco de dados
    private static void testDatabaseConnection() throws SQLException, ClassNotFoundException {
        // Carrega o driver do PostgreSQL
        Class.forName("org.postgresql.Driver");
        // Tenta estabelecer a conexão com o banco de dados usando as credenciais fornecidas
        try (Connection connection = DriverManager.getConnection(DB_URL, DB_USER, DB_PASSWORD)) {
            System.out.println("Conexão de teste bem-sucedida!"); // Exibe no console se a conexão for bem-sucedida
        }
    }

    // Função que busca os dados do dashboard no banco de dados
    private static String getDashboardData() throws SQLException, ClassNotFoundException {
        // Carrega o driver do PostgreSQL
        Class.forName("org.postgresql.Driver");
        
        // Cria um objeto JSON que será retornado com os dados do dashboard
        JsonObject jsonResponse = new JsonObject();
        
        // Estabelece a conexão com o banco de dados usando a URL e as credenciais
        try (Connection connection = DriverManager.getConnection(DB_URL)) {
            System.out.println("Conexão bem-sucedida!"); // Exibe no console se a conexão for bem-sucedida
            
            // Query SQL para obter a soma das vendas por categoria
            String queryVendas = "SELECT p.categoria, SUM(v.quantidade) AS total_vendido " +
                                 "FROM vendas v " +
                                 "JOIN produtos p ON v.produto_id = p.id " +
                                 "GROUP BY p.categoria ORDER BY total_vendido DESC";
            
            // Executa a query e armazena o resultado
            try (ResultSet resultadoVendas = connection.createStatement().executeQuery(queryVendas)) {
                JsonObject dadosVendas = new JsonObject(); // Cria um objeto JSON para armazenar os dados de vendas
                
                // Percorre o resultado da query e adiciona ao objeto JSON
                while(resultadoVendas.next()) {
                    dadosVendas.addProperty(resultadoVendas.getString("categoria"), resultadoVendas.getInt("total_vendido"));
                }
                
                jsonResponse.add("dadosVendas", dadosVendas); // Adiciona os dados de vendas ao objeto JSON de resposta
            }
        }
        
        // Retorna o JSON como uma string
        return jsonResponse.toString();
    }
}
