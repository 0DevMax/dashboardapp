fetch('/api/dashboard')
    .then(response => response.json())
    .then(data => {
        console.log("Dados recebidos da API:", data);

        // Gráfico de Vendas por Categoria
        const dadosVendas = data.dadosVendas;
        if (dadosVendas && Object.keys(dadosVendas).length > 0) {
            const ctxVendas = document.getElementById('graficoVendas').getContext('2d');
            const labelsVendas = Object.keys(dadosVendas);
            const valoresVendas = Object.values(dadosVendas);

            new Chart(ctxVendas, {
                type: 'bar',
                data: {
                    labels: labelsVendas,
                    datasets: [{
                        label: 'Vendas por Categoria',
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
                        borderWidth: 1
                    }]
                },
                options: {
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    }
                }
            });
        } else {
            console.error("dadosVendas está vazio ou undefined");
            document.getElementById('graficoVendas').insertAdjacentHTML('afterend', '<p>Não há dados disponíveis para o gráfico de vendas por categoria.</p>');
        }

        // Gráfico de Vendas por Dia
        const dadosVendasPorDia = data.dadosVendasPorDia;
        if (dadosVendasPorDia && Object.keys(dadosVendasPorDia).length > 0) {
            const ctxVendasPorDia = document.getElementById('graficoVendasPorDia').getContext('2d');
            const labelsVendasPorDia = Object.keys(dadosVendasPorDia);
            const valoresVendasPorDia = Object.values(dadosVendasPorDia);

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
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    }
                }
            });
        } else {
            console.error("dadosVendasPorDia está vazio ou undefined");
            document.getElementById('graficoVendasPorDia').insertAdjacentHTML('afterend', '<p>Não há dados disponíveis para o gráfico de vendas por dia.</p>');
        }
    })
    .catch(error => {
        console.error('Erro ao buscar dados:', error);
    });