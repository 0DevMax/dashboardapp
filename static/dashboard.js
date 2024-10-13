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
