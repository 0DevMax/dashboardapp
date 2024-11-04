// DASHBOARD
// Função para buscar e exibir gráficos do dashboard da página inicial
fetch('/api/dashboard')
    .then(response => response.json())
    .then(data => {
        console.log("Dados recebidos da API:", data);

        // Gráfico de Vendas por Categoria
        const dadosPorCategoria = data.dadosPorCategoria;
        if (dadosPorCategoria && Object.keys(dadosPorCategoria).length > 0) {
            const ctxVendas = document.getElementById('VendasCategoria').getContext('2d');
            const labelsVendas = Object.keys(dadosPorCategoria);
            const valoresVendas = Object.values(dadosPorCategoria);

            new Chart(ctxVendas, {
                type: 'bar',
                data: {
                    labels: labelsVendas,
                    datasets: [{
                        data: valoresVendas,
                        backgroundColor: [
                            'rgba(255, 99, 132, 0.2)',
                            'rgba(54, 162, 235, 0.2)',
                            'rgba(255, 206, 86, 0.2)',
                        ],
                        borderColor: [
                            'rgba(255, 99, 132, 1)',
                            'rgba(54, 162, 235, 1)',
                            'rgba(255, 206, 86, 1)',
                        ],
                        borderWidth: 1,
                        barPercentage: 0.5
                    }]
                },
                options: {
                    plugins: {
                        legend: {
                            display: false
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    }
                }
            });
        } else {
            console.error("dadosPorCategoria está vazio ou undefined");
            document.getElementById('VendasCategoria').insertAdjacentHTML('afterend', '<p>Não há dados disponíveis para o gráfico de vendas por categoria.</p>');
        }

        // Gráfico de Vendas por Dia
        const dadosPorPorDia = data.dadosPorDia;
        if (dadosPorPorDia && Object.keys(dadosPorPorDia).length > 0) {
            const ctxVendasPorDia = document.getElementById('VendasDia').getContext('2d');
            const labelsVendasPorDia = Object.keys(dadosPorPorDia);
            const valoresVendasPorDia = Object.values(dadosPorPorDia);

            new Chart(ctxVendasPorDia, {
                type: 'line',
                data: {
                    labels: labelsVendasPorDia,
                    datasets: [{
                        label: 'Vendas por Dia',
                        data: valoresVendasPorDia,
                        backgroundColor: 'rgba(153, 102, 255, 0.2)',
                        borderColor: 'rgba(153, 102, 255, 1)',
                        borderWidth: 1
                    }]
                },
                options: {
                    plugins: {
                        legend: {
                            display: false
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    }
                }
            });
        } else {
            console.error("dadosPorDataPorDia está vazio ou undefined");
            document.getElementById('VendasDia').insertAdjacentHTML('afterend', '<p>Não há dados disponíveis para o gráfico de vendas por dia.</p>');
        }
    })
    .catch(error => {
        console.error('Erro ao buscar dados:', error);
    });


// CATÁLOGO
// Função para preencher o catálogo de produtos
function preencherCatalogo(dados) {
    const catalogoContainer = document.getElementById('grid-catalogo');
    catalogoContainer.innerHTML = '';

    dados.forEach(produto => {
        const card = document.createElement('div');
        card.className = 'grid-card-catalogo';
        card.innerHTML = `
            <img src="/static/imagens/mochila.png">
            <p class="produto-nome">${produto.nome_produto}</p>
            <p class="produto-preco">R$ ${produto.preco.toFixed(2)}</p>
        `;
        catalogoContainer.appendChild(card);
    });
}

// Busca e exibe os dados do catálogo de produtos
fetch('/api/catalogo')
    .then(response => response.json())
    .then(data => {
        console.log("Dados recebidos da API:", data);
        preencherCatalogo(data);
    })
    .catch(error => {
        console.error('Erro ao buscar dados do catálogo:', error);
    });


// ESTOQUES / Produtos
// Função para buscar dados dos produtos
async function fetchProdutosData() {
    try {
        const response = await fetch('/api/estoques-produtos');
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Erro ao buscar dados:', error)
        return [];
    }
}

//Função para preencher a tabela de produtos com dados recebidos
function criarTabelaProdutos(data) {
    const tbody = document.querySelector('#tabelaProdutos tbody');
    tbody.innerHTML = '';

    data.forEach(item => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td data-title="ID">${item.id}</td>
            <td data-title="Produto">${item.nome_produto}</td>
            <td data-title="Preço">${item.preco}</td>
            <td data-title="Qtd">${item.quantidade}</td>
            <td data-title="Categoria">${item.categoria}</td>
        `;
        tbody.appendChild(row);
    });
}

// Inicialização da tabela de produtos ao carregar a página
async function initializeProdutos() {
    const data = await fetchProdutosData();
    criarTabelaProdutos(data);
}

document.addEventListener('DOMContentLoaded', initializeProdutos);

// Estoques / Materiais
//Função para buscar dados dos materiais com a API
async function fetchMateriaisData() {
    try {
        const response = await fetch('/api/estoques-materiais');
        const data = await response.json();
        return data;
    } catch (error){
        console.error('Erro ao buscar os dados:', error)
        return [];
    }
}

//Desempacotamento de 'data' e iteração para criar tabela
function criarTabelaMateriais(data) {
    const tbody = document.querySelector('#tabelaMateriais tbody');
    tbody.innerHTML = '';

    data.forEach(item => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td data-title="ID">${item.id}</td>
            <td data-title="nome_material">${item.nome_material}</td>
            <td data-title="fornecedor">${item.fornecedor}</td>
            <td data-title="qtd">${item.qtd}</td>
            <td data-title="preco">${item.preco}</td>
            <td data-title="custo_total">${item.custo_total}</td>
            <td data-title="data">${item.data}</td>
        `;
        tbody.append(row);
    });
}

async function initializeMateriais() {
    const data = await fetchMateriaisData();
    criarTabelaMateriais(data);
}

document.addEventListener('DOMContentLoaded', initializeMateriais);

// VENDAS
// Função para buscar dados de vendas
async function fetchVendasData() {
    try {
        const response = await fetch('/api/vendas-registros');
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Erro ao buscar dados:', error);
        return [];
    }
}

// Função para preencher a tabela de vendas com dados recebidos
function criarTabelaVendas(data) {
    const tbody = document.querySelector('#tabelaVendas tbody');
    tbody.innerHTML = '';

    data.forEach(item => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td data-title="ID">${item.id}</td>
            <td data-title="Data">${item.data}</td>
            <td data-title="Produto">${item.produto_id}</td>
            <td data-title="Qtd">${item.quantidade}</td>
        `;
        tbody.appendChild(row);
    });
}

// Inicialização da tabela de vendas ao carregar a página
async function initializeVendas() {
    const data = await fetchVendasData();
    criarTabelaVendas(data);
}

document.addEventListener('DOMContentLoaded', initializeVendas);


// ENCOMENDAS
// Função para buscar dados de encomendas
async function fetchEncomendasData() {
    try {
        const response = await fetch('/api/encomendas');
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Erro ao buscar dados:', error);
        return [];
    }
}

 //Função para preencher a tabela de encomendas com dados recebidos
 function criarTabelaEncomendas(data) {
    const tbody = document.querySelector('#tabelaEncomendas tbody');
    tbody.innerHTML = '';

    data.forEach(item => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td data-title="ID">${item.id}</td>
            <td data-title="Cliente">${item.cliente}</td>
            <td data-title="Contato">${item.contato}</td>
            <td data-title="Produto">${item.produto}</td>
            <td data-title="Observações">${item.observações}</td>
            <td data-title="Qtd">${item.qtd}</td>
        `;
        tbody.appendChild(row);
    });
 }

 // Inicialização da tabela de encomendas ao carregar a página
 async function initializeEncomendas() {
    const data = await fetchEncomendasData();
    criarTabelaEncomendas(data);
 }

 document.addEventListener('DOMContentLoaded', initializeEncomendas);

