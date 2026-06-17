# CN Serverless Primes

Projeto laboratorial da unidade curricular Computação na Nuvem.

O objetivo deste projeto é implementar e avaliar uma função sem servidor que gera todos os números primos inferiores a um número natural n. A solução foi desenvolvida com AWS Lambda e exposta por HTTP através de Amazon API Gateway.

## Autor

João Mendonça  
Mestrado em Engenharia Informática  
Universidade da Beira Interior

## Arquitetura

A arquitetura implementada é composta por:

- Cliente HTTP local
- Amazon API Gateway
- AWS Lambda
- Amazon CloudWatch

Fluxo geral:

```text
Cliente HTTP
    |
    v
Amazon API Gateway
    |
    v
AWS Lambda
    |
    v
Resposta JSON
```

O cliente envia um pedido POST para o endpoint da API. O API Gateway encaminha o pedido para a função Lambda, que calcula os números primos inferiores a n e devolve uma resposta JSON.

## Estrutura do projeto

```text
.
├── benchmark
│   ├── analyze_results.py
│   ├── coldstart.py
│   ├── concurrency.py
│   ├── concurrency_saturation.py
│   └── latency.py
├── figures
│   └── .gitkeep
├── lambda
│   └── lambda_function.py
├── results
│   └── .gitkeep
├── README.md
└── requirements.txt
```

## Função Lambda

A função principal encontra-se em:
- `lambda/lambda_function.py`

A função recebe um valor n e devolve:
- o valor de n
- a quantidade de números primos encontrados
- a lista de números primos inferiores a n
- o tempo interno de execução da função

Exemplo de resposta para n=100:
```json
{
  "n": 100,
  "prime_count": 25,
  "primes": [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97],
  "execution_time_ms": 0.079
}
```

## Requisitos locais

O projeto foi desenvolvido em WSL com Python 3.12.

Criar ambiente virtual:
```bash
python3 -m venv venv
source venv/bin/activate
```

Instalar dependências:
```bash
pip install -r requirements.txt
```

## Configuração local

Criar um ficheiro .env na raiz do projeto com o endpoint da API:
- `API_URL=https://API_ID.execute-api.eu-west-2.amazonaws.com/prod/primes`

O ficheiro .env não foi colocado no GitHub por questões de segurança, embora basta apenas puxar os pacotes que estão nos `requirements.txt` para replicar a mesma coisa na máquina de outra pessoa.

## Testar a API

Exemplo com curl:
```bash
curl -X POST "$API_URL" -H "Content-Type: application/json" -d '{"n":100}'
```

## Benchmarks

Foram criados scripts para avaliar diferentes aspetos da função serverless.

### Latência sequencial

Executa 100 pedidos sequenciais para n=1000.

- `python benchmark/latency.py`
Gera:
- `results/latency_n1000.csv`

### Concorrência estável

Testa níveis de concorrência 1, 5 e 10.
- `python benchmark/concurrency.py`
Gera:
- `results/concurrency_stable_n1000.csv`

### Saturação

Testa níveis de concorrência 20, 50 e 100.
- `python benchmark/concurrency_saturation.py`
Gera:
- `results/concurrency_saturation_n1000.csv`

Neste projeto, a conta AWS usada tinha limite de 10 execuções concorrentes de Lambda. Por isso, os níveis acima de 10 foram usados para observar o comportamento sob throttling.

### Cold start

Executa cinco rondas. Em cada ronda, espera 900 segundos antes de enviar um pedido cold-start candidate e depois envia um pedido warm follow-up.
- `python benchmark/coldstart.py`
Gera:
- `results/coldstart_n1000.csv`

Durante este teste, o computador não deve entrar em suspensão.

## Análise dos resultados

Depois de executar os benchmarks, gerar tabelas resumo e gráficos com:
- `python benchmark/analyze_results.py`

Este script gera ficheiros CSV de resumo em results/ e gráficos em figures/.

Exemplos de gráficos gerados:
```bash
figures/latency_sequential_n1000.png
figures/latency_boxplot_n1000.png
figures/concurrency_latency_n1000.png
figures/concurrency_success_rate_n1000.png
figures/concurrency_failures_n1000.png
figures/coldstart_line_n1000.png
figures/coldstart_boxplot_n1000.png
figures/coldstart_mean_latency_n1000.png
```

## Resultados principais

Para n=1000, os resultados obtidos foram:
```text
Latência sequencial média: 140.6 ms
Latência sequencial mediana: 123.3 ms
100% de sucesso até 10 pedidos concorrentes
Throttling observado acima de 10 pedidos concorrentes
Latência média cold-start candidate: 478.5 ms
Latência média warm follow-up: 284.6 ms
Penalização média associada ao cold-start candidate: aproximadamente 194 ms
Tempo interno da função: cerca de 0.5 ms
```

A principal conclusão é que a computação dos números primos para n=1000 é muito rápida, mas a latência total observada pelo cliente é dominada pelo overhead da plataforma serverless, rede, API Gateway e cold start.

## Notas

Os diretórios results/ e figures/ são ignorados pelo Git, exceto os ficheiros .gitkeep.

O ficheiro .env também é ignorado, porque pode conter endpoints ou configurações locais.
