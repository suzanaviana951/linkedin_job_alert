import requests
from datetime import datetime
import os

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

# Função para carregar histórico de vagas enviadas
def carregar_historico():
    if os.path.exists("vagas_enviadas.txt"):
        with open("vagas_enviadas.txt", "r") as f:
            return set(linha.strip() for linha in f.readlines())
    return set()

# Função para salvar nova vaga no histórico
def salvar_vaga_enviada(link):
    with open("vagas_enviadas.txt", "a") as f:
        f.write(link + "\n")

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
    historico = carregar_historico()

    vagas_enviadas = 0

    for vaga in vagas:
        if vaga["link"] not in historico:
            mensagem = (
                f"🔔 *Vaga LinkedIn!*\n\n"
                f"*Cargo:* {vaga['titulo']}\n"
                f"*Empresa:* {vaga['empresa']}\n"
                f"*Link:* {vaga['link']}\n"
                f"_Hora:_ {datetime.now().strftime('%H:%M:%S - %d/%m/%Y')}"
            )
            enviar_telegram(mensagem)
            salvar_vaga_enviada(vaga["link"])
            vagas_enviadas += 1

    if vagas_enviadas == 0:
        print("📭 Nenhuma nova vaga encontrada.")

if __name__ == "__main__":
    rodar_bot()

