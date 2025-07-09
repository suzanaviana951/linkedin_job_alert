import requests
from datetime import datetime
from urllib.parse import quote_plus

# CONFIG TELEGRAM
BOT_TOKEN = "8002177542:AAGgQ3_QzbC2JMalg1QQtsw18h_sRKuu8RI"
CHAT_ID = "824040117"
TELEGRAM_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

# FILTRO GOOGLE para vagas no LinkedIn
FILTRO_LINKEDIN = (
    'site:linkedin.com/jobs ("Especialista de Logística" OR "Analista de Logística" OR '
    '"Analista de Logística Florestal" OR "Especialista de Logística Florestal" OR '
    '"Analista de Custos" OR "Controller Industrial" OR "Analista de Controladoria" OR '
    '"Analista de Planejamento Financeiro" OR "Especialista de Custos" OR '
    '"Especialista de Suprimentos" OR "Analista de Gestão de Contratos" OR '
    '"Especialista de Gestão de Contratos" OR "Especialista em Controladoria Florestal" OR '
    '"Analista de Transporte" OR "Analista de planejamento logístico")'
)

# GERAR LINK DE BUSCA
def gerar_link_busca():
    return f"https://www.google.com/search?q={quote_plus(FILTRO_LINKEDIN)}"

# ENVIAR ALERTA PRO TELEGRAM
def enviar_telegram(mensagem):
    payload = {
        'chat_id': CHAT_ID,
        'text': mensagem,
        'parse_mode': 'Markdown'
    }
    try:
        r = requests.post(TELEGRAM_URL, data=payload)
        if r.ok:
            print("✅ Alerta enviado ao Telegram!")
        else:
            print(f"❌ Erro ao enviar alerta: {r.text}")
    except Exception as e:
        print(f"❌ Falha ao enviar alerta: {e}")

# EXECUÇÃO
def rodar_bot_linkedin():
    link = gerar_link_busca()
    mensagem = (
        f"🔎 *Busca automática no LinkedIn!*\n\n"
        f"Acesse o link abaixo para ver as vagas mais recentes com seu filtro personalizado:\n\n"
        f"{link}\n\n"
        f"_Atualizado em:_ {datetime.now().strftime('%d/%m/%Y %H:%M')}"
    )
    enviar_telegram(mensagem)

if __name__ == "__main__":
    rodar_bot_linkedin()
