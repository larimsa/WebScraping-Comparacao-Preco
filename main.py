import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#Função para criar um navegador Chrome com opções específicas
def make_chrome_browser(driver_path: str, *options: str) -> webdriver.Chrome:
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    if options:
        for option in options:
            chrome_options.add_argument(option)
    chrome_service = Service(executable_path=driver_path)
    #Inicializa o navegador Chrome com o serviço e as opções especificadas
    browser = webdriver.Chrome(service=chrome_service, options=chrome_options)
    return browser

#Verifica se um captcha está presente na página
def is_captcha_present(browser):
    try:
        browser.find_element(By.ID, "captchacharacters")
        return True
    except:
        return False

#Função para obter dados de produtos na Amazon
def get_data_amazon(product, limit = int) -> list:
    url = "https://www.google.com.br/"

    driver_path = r"" #Coloque o caminho do seu chromedriver aqui
    browser = make_chrome_browser(driver_path)
    browser.get(url)

    #Aguarda até que o campo de pesquisa esteja presente na página
    search_input = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "gLFyf"))
    )
    #Preenche o campo de pesquisa com o termo "amazon"
    search_input.send_keys("amazon")
    search_input.send_keys(Keys.RETURN)
    
    #Aguarda até que o elemento com ID "search" esteja presente na página
    WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, "search"))
    )
    #Analisa o conteúdo da página do Google para obter os resultados
    soup = BeautifulSoup(browser.page_source, 'html.parser')

    results = []
    for item in soup.select('.g'):
        link = item.select_one('.yuRUbf a')['href'] if item.select_one('.yuRUbf a') else None
        if link:
            results.append({'link': link})

    products = []
    if results:
        #Obtém o link do segundo resultado (assumindo que o primeiro seja um anúncio)
        first_result_link = results[1]['link']
        try:
            browser.get(first_result_link)

            while is_captcha_present(browser):
                print("CAPTCHA detectado, recarregando a página...")
                browser.refresh()
                time.sleep(5)

            #Preenche o campo de pesquisa na página da Amazon com o produto fornecido
            search_input_amazon = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.ID, "twotabsearchtextbox"))
            )
            search_input_amazon.send_keys(product)
            search_input_amazon.send_keys(Keys.RETURN)

            #Aguarda até que os resultados de pesquisa estejam presentes na página
            WebDriverWait(browser, 10).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "div.s-main-slot div[data-component-type='s-search-result']"))
            )

            new_soup = BeautifulSoup(browser.page_source, 'html.parser')
            items = new_soup.select("div.s-main-slot div[data-component-type='s-search-result']")

            #Extrai informações de cada item de produto na página de resultados
            for item in items[:limit]:
                product_data = {}
                product_data["titulo"] = item.find(class_="a-size-base-plus a-color-base a-text-normal").get_text(strip=True)
                product_data["preco"] = item.find(class_="a-offscreen").get_text(strip=True)
                product_data["avaliacao"] = item.find(class_="a-icon-alt").get_text(strip=True)
                product_data["link"] = item.find("a", class_="a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal")['href']

                products.append(product_data)

        except Exception as e:
            print("Erro ao acessar a página:", e)

    browser.quit()
    return products

#Função para obter dados de produtos no Mercado Livre
def get_data_mercadolivre(product, limit= int):
    url = "https://lista.mercadolivre.com.br/"

    #Substitui espaços no nome do produto por hífens para formar a URL do Mercado Livre
    produto = product.replace(" ", "-")
    url2 = url + produto

    classes = {
        "preco": "ui-search-price__part",
        "titulo": "ui-search-item__title",
        "avaliacao": "ui-search-reviews__rating-number",
    }

    dados = []
    response = requests.get(url2)

    if response.status_code == 200:
        doc = response.text
        soup = BeautifulSoup(doc, 'html.parser')

        #Encontra todos os itens de produto na página do Mercado Livre
        items = soup.find_all("li", class_="ui-search-layout__item")

        for item in items[:limit]:
            product_data = {}
            for key, value in classes.items():
                info = item.find(class_=value)
                if info:
                    product_data[key] = info.get_text(strip=True)

            link_element = item.find("a", class_="ui-search-link")
            if link_element:
                product_data["link"] = link_element["href"]

            dados.append(product_data)

    return dados

print("Por favor, digite um produto: ")
produto = input()
dados_mercadolivre = get_data_mercadolivre(produto, limit=5) #Escolha o limite do numero de resultados
for i, product in enumerate(dados_mercadolivre, start=1):
    print(f"Produto {i} no Mercado Livre:")
    for key, value in product.items():
        print(f"{key.capitalize()}: {value}")
    print("\n")


dados_amazon = get_data_amazon(produto, limit=5) #Escolha o limite do numero de resultados
for i, product in enumerate(dados_amazon, start=1):
    print(f"Produto {i} na Amazon:")
    for key, value in product.items():
        if key == "link":
            print(f"{key.capitalize()}: https://www.amazon.com.br{value}")
        else:
            print(f"{key.capitalize()}: {value}")
    print("\n")

def compare_prices(dados_mercadolivre, dados_amazon):
    menor_preco_mercadolivre = float('inf')
    menor_preco_amazon = float('inf')
    link_mercadolivre = None
    link_amazon = None

    for product in dados_mercadolivre:
        if 'preco' in product:
            preco = float(product['preco'].replace('R$', '').replace('.', '').replace(',', '.'))
            if preco < menor_preco_mercadolivre:
                menor_preco_mercadolivre = preco
                link_mercadolivre = product.get('link', None)

    for product in dados_amazon:
        if 'preco' in product:
            preco = float(product['preco'].replace('R$', '').replace('.', '').replace(',', '.'))
            if preco < menor_preco_amazon:
                menor_preco_amazon = preco
                link_amazon = product.get('link', None)

    return {'menor_preco_mercadolivre': menor_preco_mercadolivre, 'link_mercadolivre': link_mercadolivre, 
            'menor_preco_amazon': menor_preco_amazon, 'link_amazon':link_amazon}

resultado_comparacao = compare_prices(dados_mercadolivre, dados_amazon)

print("MENORES PREÇOS DE CADA SITE:\n")
print("Menor Preço no Mercado Livre: R$", resultado_comparacao['menor_preco_mercadolivre'])
print("Link do Produto no Mercado Livre:", resultado_comparacao['link_mercadolivre'])
print("\n")
print("Menor Preço na Amazon: R$", resultado_comparacao['menor_preco_amazon'])
print("Link do Produto na Amazon: https://www.amazon.com.br" + resultado_comparacao['link_amazon'])
