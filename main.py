import requests
from datetime import datetime

# CONFIGURAÇÕES DO TELEGRAM
BOT_TOKEN = "8002177542:AAGgQ3_QzbC2JMalg1QQtsw18h_sRKuu8RI"
CHAT_ID = "824040117"
TELEGRAM_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

# FUNÇÃO SIMULADA: Aqui depois vamos puxar do LinkedIn
def buscar_vagas_linkedin():
    vagas = [
        {
            "titulo": "Especialista de Logística Florestal",
            "empresa": "Bracell",
            "link": "https://www.linkedin.com/jobs/view/9999999999"
        }
    ]
    return vagas

# ENVIA ALERTA PRO TELEGRAM
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

# RODAR O BOT
def rodar_bot():
    vagas = buscar_vagas_linkedin()
    if vagas:
        for vaga in vagas:
            mensagem = (
                f"🔔 *Vaga LinkedIn!*\n\n"
                f"*Cargo:* {vaga['titulo']}\n"
                f"*Empresa:* {vaga['empresa']}\n"
                f"*Link:* {vaga['link']}\n"
                f"_Hora:_ {datetime.now().strftime('%H:%M:%S - %d/%m/%Y')}"
            )
            enviar_telegram(mensagem)
    else:
        print("📭 Nenhuma vaga encontrada.")

if __name__ == "__main__":
    rodar_bot()
