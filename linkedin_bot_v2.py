import requests
from datetime import datetime

# CONFIGURAÇÕES DO TELEGRAM
BOT_TOKEN = "8002177542:AAGgQ3_QzbC2JMalg1QQtsw18h_sRKuu8RI"
CHAT_ID = "824040117"
TELEGRAM_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

# URLs dos filtros de cargos no LinkedIn
urls_linkedin = [
    "https://www.linkedin.com/jobs/search/?keywords=Especialista%20de%20Log%C3%ADstica",
    "https://www.linkedin.com/jobs/search/?keywords=Analista%20de%20Log%C3%ADstica",
    "https://www.linkedin.com/jobs/search/?keywords=Analista%20de%20Log%C3%ADstica%20Florestal",
    "https://www.linkedin.com/jobs/search/?keywords=Especialista%20de%20Log%C3%ADstica%20Florestal",
    "https://www.linkedin.com/jobs/search/?keywords=Analista%20de%20Custos",
    "https://www.linkedin.com/jobs/search/?keywords=Controller%20Industrial",
    "https://www.linkedin.com/jobs/search/?keywords=Analista%20de%20Controladoria",
    "https://www.linkedin.com/jobs/search/?keywords=Analista%20de%20Planejamento%20Financeiro",
    "https://www.linkedin.com/jobs/search/?keywords=Especialista%20de%20Custos",
    "https://www.linkedin.com/jobs/search/?keywords=Especialista%20de%20Suprimentos",
    "https://www.linkedin.com/jobs/search/?keywords=Analista%20de%20Gest%C3%A3o%20de%20Contratos",
    "https://www.linkedin.com/jobs/search/?keywords=Especialista%20de%20Gest%C3%A3o%20de%20Contratos",
    "https://www.linkedin.com/jobs/search/?keywords=Especialista%20em%20Controladoria%20Florestal",
    "https://www.linkedin.com/jobs/search/?keywords=Analista%20de%20Transporte",
    "https://www.linkedin.com/jobs/search/?keywords=Analista%20de%20Planejamento%20Log%C3%ADstico"
]

def enviar_telegram(mensagem):
    payload = {
        'chat_id': CHAT_ID,
        'text': mensagem,
        'parse_mode': 'Markdown'
    }
    try:
        response = requests.post(TELEGRAM_URL, data=payload)
        if response.ok:
            print("✅ Alerta enviado ao Telegram!")
        else:
            print(f"❌ Erro ao enviar alerta: {response.text}")
    except Exception as e:
        print(f"❌ Erro: {e}")

def rodar_bot():
    for url in urls_linkedin:
        mensagem = (
            f"🔍 *Nova varredura LinkedIn!*\n\n"
            f"[Clique para abrir a busca personalizada]({url})\n"
            f"_Hora da varredura:_ {datetime.now().strftime('%H:%M:%S - %d/%m/%Y')}"
        )
        enviar_telegram(mensagem)

if __name__ == "__main__":
    rodar_bot()
