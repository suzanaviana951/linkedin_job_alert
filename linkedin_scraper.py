
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
from pathlib import Path

HISTORICO_PATH = Path("historico_vagas.json")
COOKIES_PATH = Path("linkedin_cookies.json")

def carregar_historico():
    if HISTORICO_PATH.exists():
        with open(HISTORICO_PATH, "r") as f:
            return set(json.load(f).get("enviadas", []))
    return set()

def salvar_historico(historico):
    with open(HISTORICO_PATH, "w") as f:
        json.dump({"enviadas": list(historico)}, f, indent=4)

def carregar_cookies(driver):
    if COOKIES_PATH.exists():
        with open(COOKIES_PATH, "r") as f:
            cookies = json.load(f)
        for cookie in cookies:
            if 'sameSite' in cookie and cookie['sameSite'] == 'None':
                cookie['sameSite'] = 'Strict'
            driver.add_cookie(cookie)
        driver.refresh()
        time.sleep(5)

def extrair_vagas():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')

    driver = webdriver.Chrome(options=options)
    driver.get("https://www.linkedin.com/jobs/search/?keywords=controller")

    time.sleep(5)
    carregar_cookies(driver)

    vagas = {"remoto": [], "presencial": []}
    historico = carregar_historico()
    novos_links = set()

    links = driver.find_elements(By.CLASS_NAME, 'base-card__full-link')

    for i, link in enumerate(links[:10]):
        try:
            link_url = link.get_attribute('href')
            if link_url in historico:
                continue

            driver.execute_script("window.open(arguments[0]);", link_url)
            driver.switch_to.window(driver.window_handles[1])

            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'description__text'))
            )
            conteudo = driver.page_source.lower()

            if "inglês avançado" in conteudo or "advanced english" in conteudo:
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
                continue

            titulo = driver.title.split(" | ")[0]
            modalidade = "remoto" if "remote" in conteudo else "presencial"
            vagas[modalidade].append((titulo, link_url))
            novos_links.add(link_url)

            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            time.sleep(4)

        except Exception as e:
            print(f"Erro na vaga {i}: {e}")
            if len(driver.window_handles) > 1:
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
            continue

    driver.quit()
    salvar_historico(historico.union(novos_links))
    return vagas
