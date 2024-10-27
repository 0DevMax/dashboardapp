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

// Função para preencher o catálogo de produtos no DOM
function preencherCatalogo(dados) {
    const catalogoContainer = document.getElementById('grid-catalogo');
    catalogoContainer.innerHTML = '';

    dados.forEach(produto => {
        const card = document.createElement('div');
        card.className = 'grid-card-catalogo';
        card.innerHTML = `
            <h5 class="produto-nome">${produto.nome_produto}</h5>
            <p class="produto-preco">R$ ${produto.preco.toFixed(2)}</p>
            <p class="produto-quantidade">Quantidade: ${produto.quantidade}</p>
            <p class="produto-categoria">${produto.categoria}</p>
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

// Função para buscar dados de vendas
async function fetchData() {
    try {
        const response = await fetch('/api/vendas');
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Erro ao buscar dados:', error);
        return [];
    }
}

// Função para preencher a tabela de vendas com dados recebidos
function criarTabela(data) {
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
async function initialize() {
    const data = await fetchData();
    criarTabela(data);
}

document.addEventListener('DOMContentLoaded', initialize);
