# Delivery Intelligence

Sistema de Machine Learning para estimar o risco de atraso na entrega de pedidos de e-commerce, com disponibilização das previsões por meio de uma API REST.

## Sobre o projeto

O Delivery Intelligence é um projeto de Machine Learning desenvolvido com Python a partir do conjunto público de dados Brazilian E-Commerce Public Dataset by Olist.

O objetivo é investigar se informações disponíveis no momento da finalização do pedido podem ajudar a identificar pedidos com maior risco de atraso.

O projeto contempla exploração e preparação de dados, engenharia de atributos, treinamento e avaliação de modelos, além de uma API para disponibilizar previsões.

**Importante:** o conjunto de dados representa entregas de e-commerce entre 2016 e 2018. Ele não representa operações de delivery de restaurantes ou entregas em tempo real.

## Problema e definição do alvo

Um pedido é classificado como atrasado quando sua data efetiva de entrega ao cliente é posterior à data estimada de entrega.

- `is_late = 1`: pedido entregue após a data estimada.
- `is_late = 0`: pedido entregue até a data estimada.

Foram considerados pedidos com status `delivered` e com data efetiva de entrega conhecida, totalizando 96.470 pedidos.

O cenário de previsão considerado é o momento do checkout, após a composição do carrinho. Por isso, informações que só seriam conhecidas depois da entrega não são utilizadas como atributos do modelo.

## Dados e atributos

**Fonte:** [Brazilian E-Commerce Public Dataset by Olist — Kaggle](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce).

Os atributos utilizados incluem:

| Grupo | Atributos |
|---|---|
| Localização | Estado do cliente |
| Pedido | Quantidade de itens e quantidade de vendedores |
| Valores | Valor dos produtos e valor do frete |
| Vendedores | Quantidade de estados dos vendedores, vendedor no mesmo estado do cliente e múltiplos vendedores |
| Tempo | Dia da semana, hora e mês da compra |
| Prazo | Prazo estimado em dias |

Foram utilizados 12 atributos no total.

**Prevenção de vazamento de dados:** datas efetivas de entrega, diferença entre entrega real e estimada e a variável-alvo não foram utilizadas como entradas do modelo.

## Metodologia

O desenvolvimento foi organizado nas seguintes etapas:

1. Exploração e análise dos dados.
2. Tratamento e integração das tabelas.
3. Engenharia e seleção de atributos.
4. Separação cronológica entre treino e teste.
5. Pré-processamento e treinamento dos modelos.
6. Avaliação e seleção do limiar de classificação.
7. Disponibilização do modelo por API REST.
8. Testes automatizados da API.

## Treinamento e avaliação

Foram comparados dois algoritmos:

- Regressão Logística.
- Random Forest.

A Regressão Logística com balanceamento de classes foi selecionada para a versão final.

O limiar de classificação de 0,6 foi escolhido com base no F1-score da classe positiva em uma validação temporal realizada dentro dos dados de treinamento.

O pré-processamento utiliza:

- `StandardScaler` para atributos numéricos.
- `OneHotEncoder` para o estado do cliente.
- Pipeline do Scikit-learn para integrar pré-processamento e modelo.

A divisão dos dados foi cronológica, mantendo os pedidos mais recentes para teste:

| Conjunto | Pedidos | Período | Taxa de atraso |
|---|---:|---|---:|
| Treino | 77.176 | 15/09/2016 a 26/05/2018 | 8,82% |
| Teste | 19.294 | 26/05/2018 a 29/08/2018 | 5,29% |

A diferença entre as taxas de atraso evidencia uma mudança na distribuição temporal dos dados, que deve ser considerada na interpretação dos resultados.

## Resultados

Avaliação do modelo final no conjunto de teste, utilizando o limiar de classificação de 0,6:

| Métrica | Resultado |
|---|---:|
| Precisão (Precision) — classe atrasado | 0,10 |
| Revocação (Recall) — classe atrasado | 0,52 |
| F1-score — classe atrasado | 0,17 |
| Acurácia geral | 0,73 |
| ROC-AUC | 0,72 |

### Matriz de confusão

| | Previsto: não atrasado | Previsto: atrasado |
|---|---:|---:|
| Real: não atrasado | 13.564 | 4.709 |
| Real: atrasado | 494 | 527 |

O modelo identificou aproximadamente 52% dos pedidos atrasados no conjunto de teste. Entretanto, sua precisão foi baixa: apenas cerca de 10% das previsões positivas correspondiam a pedidos realmente atrasados.

Isso significa que o modelo consegue sinalizar parte dos pedidos que atrasariam, mas também gera muitos falsos positivos.

O F1-score caiu de aproximadamente 0,275 na validação para 0,17 no teste. Essa diferença reforça a necessidade de avaliar a generalização temporal e investigar mudanças na distribuição dos dados.

O ROC-AUC de aproximadamente 0,72 indica que o modelo apresenta capacidade de discriminação entre as classes superior à de uma classificação aleatória, embora ainda tenha limitações.

Os resultados são experimentais. O modelo não deve ser considerado pronto para uso em produção.

## API REST

O modelo treinado pode ser acessado por uma API desenvolvida com FastAPI.

### Endpoints

| Método | Rota | Descrição |
|---|---|---|
| GET | `/` | Verifica se a API está funcionando |
| POST | `/prever` | Recebe os atributos de um pedido e retorna a previsão |

A resposta da previsão contém:

- Classificação de risco de atraso.
- Probabilidade estimada de atraso.
- Limiar utilizado na classificação.

A documentação interativa fica disponível em `/docs`.

## Tecnologias

- Python
- Pandas
- NumPy
- Scikit-learn
- Matplotlib
- Seaborn
- Jupyter Notebook
- FastAPI
- Uvicorn
- Joblib
- Pytest

## Estrutura do projeto

```text
delivery-intelligence/
├── models/
│   ├── configuracao.pkl
│   └── modelo_atraso.pkl
├── notebooks/
│   └── 01_exploracao_e_modelagem.ipynb
├── src/
│   └── api/
│       └── main.py
├── tests/
│   └── test_api.py
├── data/
│   └── raw/              # Dados originais, não versionados
├── reports/
├── .gitignore
├── requirements.txt
└── README.md
```

## Como executar

### 1. Clonar o repositório

```bash
git clone https://github.com/Maria-Fernanda-Bronzoni/delivery-intelligence.git
cd delivery-intelligence
```

### 2. Criar e ativar o ambiente virtual

No Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Instalar as dependências

```bash
python -m pip install -r requirements.txt
```

### 4. Executar a API

```bash
python -m uvicorn src.api.main:app --reload
```

A API estará disponível em:

`http://127.0.0.1:8000`

Documentação interativa:

`http://127.0.0.1:8000/docs`

Os arquivos do modelo já estão incluídos no repositório, portanto a API pode ser executada sem baixar novamente os dados originais.

### 5. Executar os testes

```bash
python -m pytest tests/ -v
```

Os testes automatizados verificam o funcionamento da rota inicial, a previsão e a validação de entrada.

## Reproduzir a análise

Os arquivos originais do Olist não são armazenados neste repositório. Para executar o notebook desde o início, baixe o conjunto de dados na fonte indicada e coloque os arquivos CSV em `data/raw/`.

## Limitações e próximos passos

- Os dados são históricos e abrangem o período de 2016 a 2018.
- O contexto é de e-commerce, não de delivery de restaurantes.
- A baixa precisão indica uma quantidade elevada de falsos positivos.
- A mudança na taxa de atraso entre treino e teste pode afetar a generalização.
- O modelo ainda não foi validado em uma operação real.

Possíveis evoluções incluem avaliação com dados mais recentes, calibração de probabilidades, monitoramento de desempenho e integração com sistemas operacionais de logística.

---

Projeto de portfólio — Machine Learning e desenvolvimento de APIs com Python.