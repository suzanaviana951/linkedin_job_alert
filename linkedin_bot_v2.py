import requests
import json
import os
from datetime import datetime

# CONFIGURAÇÕES DO TELEGRAM
BOT_TOKEN = "8002177542:AAGgQ3_QzbC2JMalg1QQtsw18h_sRKuu8RI"
CHAT_ID = "824040117"
TELEGRAM_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

# LINKS PERSONALIZADOS COM FILTRO DE LOCALIZAÇÃO: BRASIL
urls_linkedin = {
    "Especialista de Logística": "https://www.linkedin.com/jobs/search/?keywords=Especialista%20de%20Log%C3%ADstica&location=Brasil",
    "Analista de Logística": "https://www.linkedin.com/jobs/search/?keywords=Analista%20de%20Log%C3%ADstica&location=Brasil",
    "Analista de Logística Florestal": "https://www.linkedin.com/jobs/search/?keywords=Analista%20de%20Log%C3%ADstica%20Florestal&location=Brasil",
    "Especialista de Logística Florestal": "https://www.linkedin.com/jobs/search/?keywords=Especialista%20de%20Log%C3%ADstica%20Florestal&location=Brasil",
    "Analista de Custos": "https://www.linkedin.com/jobs/search/?keywords=Analista%20de%20Custos&location=Brasil",
    "Controller Industrial": "https://www.linkedin.com/jobs/search/?keywords=Controller%20Industrial&location=Brasil",
    "Analista de Controladoria": "https://www.linkedin.com/jobs/search/?keywords=Analista%20de%20Controladoria&location=Brasil",
    "Analista de Planejamento Financeiro": "https://www.linkedin.com/jobs/search/?keywords=Analista%20de%20Planejamento%20Financeiro&location=Brasil",
    "Especialista de Custos": "https://www.linkedin.com/jobs/search/?keywords=Especialista%20de%20Custos&location=Brasil",
    "Especialista de Suprimentos": "https://www.linkedin.com/jobs/search/?keywords=Especialista%20de%20Suprimentos&location=Brasil",
    "Analista de Gestão de Contratos": "https://www.linkedin.com/jobs/search/?keywords=Analista%20de%20Gest%C3%A3o%20de%20Contratos&location=Brasil",
    "Especialista de Gestão de Contratos": "https://www.linkedin.com/jobs/search/?keywords=Especialista%20de%20Gest%C3%A3o%20de%20Contratos&location=Brasil",
    "Especialista em Controladoria Florestal": "https://www.linkedin.com/jobs/search/?keywords=Especialista%20em%20Controladoria%20Florestal&location=Brasil",
    "Analista de Transporte": "https://www.linkedin.com/jobs/search/?keywords=Analista%20de%20Transporte&location=Brasil",
    "Analista de Planejamento Logístico": "https://www.linkedin.com/jobs/search/?keywords=Analista%20de%20Planejamento%20Log%C3%ADstico&location=Brasil"
}

# Arquivo local para armazenar histórico de vagas
ARQUIVO_HISTORICO = "vagas_enviadas.json"

def carregar_historico():
    if os.path.exists(ARQUIVO_HISTORICO):
        try:
            with open(ARQUIVO_HISTORICO, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            print("⚠️ Histórico corrompido. Reiniciando...")
            return []
    return []

def salvar_historico(vagas):
    with open(ARQUIVO_HISTORICO, "w") as f:
        json.dump(vagas, f)

def enviar_telegram(mensagem):
    payload = {
        'chat_id': CHAT_ID,
        'text': mensagem,
        'parse_mode': 'Markdown'
    }
    response = requests.post(TELEGRAM_URL, data=payload)
    if not response.ok:
        print("❌ Falha no envio:", response.text)

def rodar_bot():
    historico = carregar_historico()
    novas_vagas = []

    for cargo, url in urls_linkedin.items():
        if url not in historico:
            novas_vagas.append((cargo, url))
            historico.append(url)

    if novas_vagas:
        mensagem = "🔍 *Novas buscas LinkedIn detectadas!*\n\n"
        for cargo, url in novas_vagas:
            mensagem += f"🔹 *{cargo}*\n[Ver vagas no LinkedIn]({url})\n\n"
        mensagem += f"_Varredura realizada às {datetime.now().strftime('%H:%M:%S - %d/%m/%Y')}_"

        enviar_telegram(mensagem)
        salvar_historico(historico)
    else:
        print("🟢 Nenhuma nova vaga encontrada.")

if __name__ == "__main__":
    rodar_bot()
