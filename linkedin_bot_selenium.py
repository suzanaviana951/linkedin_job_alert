from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import os
import json
import requests
from datetime import datetime

# CONFIGURAÇÕES DO TELEGRAM
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
TELEGRAM_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

# LINKS DE BUSCA PERSONALIZADOS
urls = {
    "Analista de Logística": "https://www.linkedin.com/jobs/search/?currentJobId=4264608623&f_E=4&f_PP=104746682%2C102043228%2C103501557%2C105742718%2C105159580%2C104730895%2C103451405%2C105132905%2C105900002%2C102620040&f_T=1657%2C2055%2C8787%2C6511%2C504%2C12%2C113%2C5046&f_TPR=r604800&keywords=Analista%20de%20Logistica&origin=JOB_SEARCH_PAGE_JOB_FILTER&sortBy=DD&spellCorrectionEnabled=true"
}

ARQUIVO_HISTORICO = "vagas_filtradas.json"

def carregar_historico():
    if os.path.exists(ARQUIVO_HISTORICO):
        with open(ARQUIVO_HISTORICO, "r") as f:
            return json.load(f)
    return []

def salvar_historico(historico):
    with open(ARQUIVO_HISTORICO, "w") as f:
        json.dump(historico, f)

def enviar_telegram(mensagem):
    payload = {
        'chat_id': CHAT_ID,
        'text': mensagem,
        'parse_mode': 'Markdown'
    }
    requests.post(TELEGRAM_URL, data=payload)

def vaga_tem_ingles(driver):
    try:
        descricao = driver.find_element(By.CLASS_NAME, 'description__text').text.lower()
        if "inglês avançado" in descricao or "ingles avançado" in descricao or "fluente em inglês" in descricao:
            print("❌ Vaga com exigência de inglês detectada.")
            return True
        return False
    except:
        return False

def rodar_bot():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')

    driver = webdriver.Chrome(options=options)
    historico = carregar_historico()
    mensagem = "🔍 *Novas vagas LinkedIn sem exigência de inglês:*\n\n"

    for cargo, url in urls.items():
        driver.get(url)
        time.sleep(5)
        vagas = driver.find_elements(By.CLASS_NAME, 'base-card__full-link')

        for vaga in vagas:
            link = vaga.get_attribute("href")
            if link in historico:
                continue

            driver.get(link)
            time.sleep(3)

            if vaga_tem_ingles(driver):
                continue

            mensagem += f"🔹 *{cargo}*\n[Ver vaga]({link})\n\n"
            historico.append(link)

    if mensagem.strip() != "🔍 *Novas vagas LinkedIn sem exigência de inglês:*":
        mensagem += f"_Varredura: {datetime.now().strftime('%H:%M:%S - %d/%m/%Y')}_"
        enviar_telegram(mensagem)
        salvar_historico(historico)
    else:
        print("🟢 Sem vagas novas ou todas com exigência de inglês.")

    driver.quit()

if __name__ == "__main__":
    rodar_bot()
