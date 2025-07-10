from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from time import sleep
import os
import requests
from datetime import datetime

# Configurações do Telegram
BOT_TOKEN = "8002177542:AAGgQ3_QzbC2JMalg1QQtsw18h_sRKuu8RI"
CHAT_ID = "824040117"
TELEGRAM_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

# URL de exemplo (você pode repetir com outras nos próximos .yml)
URL = "https://www.linkedin.com/jobs/search/?currentJobId=4264608623&f_E=4&f_PP=104746682%2C102043228%2C103501557%2C105742718%2C105159580%2C104730895%2C103451405%2C105132905%2C105900002%2C102620040&f_T=1657%2C2055%2C8787%2C6511%2C504%2C12%2C113%2C5046&f_TPR=r604800&keywords=Analista%20de%20Logistica&origin=JOB_SEARCH_PAGE_JOB_FILTER&sortBy=DD&spellCorrectionEnabled=true"

def enviar_telegram(mensagem):
    payload = {
        'chat_id': CHAT_ID,
        'text': mensagem,
        'parse_mode': 'Markdown'
    }
    r = requests.post(TELEGRAM_URL, data=payload)
    if not r.ok:
        print("❌ Falha ao enviar para o Telegram:", r.text)

def rodar_bot():
    print("🔍 Iniciando varredura...")

    # Headless browser
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(options=chrome_options)
    driver.get(URL)

    sleep(5)  # espera carregar

    vagas = driver.find_elements(By.CLASS_NAME, "base-card")

    mensagem = "🔍 *Vagas filtradas no LinkedIn*\n\n"
    enviou_algo = False

    for vaga in vagas:
        try:
            titulo = vaga.find_element(By.CLASS_NAME, "base-search-card__title").text.strip()
            link = vaga.find_element(By.CLASS_NAME, "base-card__full-link").get_attribute("href")
            descricao = vaga.text.lower()

            if "inglês avançado" in descricao or "english advanced" in descricao:
                print(f"⛔ Ignorada (exige inglês): {titulo}")
                continue

            mensagem += f"🔹 *{titulo}*\n[Ver vaga]({link})\n\n"
            enviou_algo = True

        except Exception as e:
            print("Erro ao processar vaga:", e)

    driver.quit()

    if enviou_algo:
        mensagem += f"_Rodado às {datetime.now().strftime('%H:%M:%S - %d/%m/%Y')}_"
        enviar_telegram(mensagem)
    else:
        print("🟢 Nenhuma vaga relevante encontrada.")

if __name__ == "__main__":
    rodar_bot()

