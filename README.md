# WebScraping-Comparacao-Preco
Este repositório contém um script em Python para comparar preços de produtos entre o Mercado Livre e a Amazon. Ele utiliza técnicas de web scraping para reunir informações do produto nos respectivos sites.

## Recursos
- Obtém dados do produto do Mercado Livre e da Amazon.
- Compara preços entre as duas plataformas.
- Fornece links para os produtos com os preços mais baixos em cada plataforma.

## Requisitos
- Python 3.x
- BeautifulSoup (`bs4`)
- Selenium
- Chrome WebDriver

## Como usar

# Requisitos
- Python 3.x
- BeautifulSoup (`bs4`)
- Selenium
- Chrome WebDriver

# Passo a passo
1. Clone ou baixe o repositório.
2. Instale os pacotes Python necessários usando o pip:
    ```
    pip install beautifulsoup4 selenium
    ```
3. Baixe o Chrome WebDriver [aqui](https://chromedriver.chromium.org/downloads) e coloque-o na pasta `drivers`.

## Uso
1. Execute o script.
2. Digite o nome do produto quando solicitado.
3. O script exibirá o preço mais baixo e o link para o produto no Mercado Livre e na Amazon.

## Funções
### `get_data_mercadolivre(produto, limit=1)`
- Obtém dados do produto do Mercado Livre.
- Parâmetros:
    - `produto`: O nome do produto.
    - `limit`: Limite o número de resultados (opcional, o padrão é 1).
- Retorna uma lista de dicionários contendo informações do produto.

### `get_data_amazon(produto, limit=1)`
- Obtém dados do produto da Amazon.
- Parâmetros:
    - `produto`: O nome do produto.
    - `limit`: Limite o número de resultados (opcional, o padrão é 1).
- Retorna uma lista de dicionários contendo informações do produto.

### `compare_prices(dados_mercadolivre, dados_amazon)`
- Compara preços entre o Mercado Livre e a Amazon.
- Parâmetros:
    - `dados_mercadolivre`: Dados do produto do Mercado Livre.
    - `dados_amazon`: Dados do produto da Amazon.
- Retorna um dicionário contendo os preços mais baixos e links para ambas as plataformas.

