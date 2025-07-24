
from linkedin_scraper import extrair_vagas
from telegram_bot import enviar_mensagem

def main():
    vagas = extrair_vagas()
    if vagas["remoto"]:
        enviar_mensagem("🚀 Vagas Remotas\n" + "="*30)
        for titulo, link in vagas["remoto"]:
            mensagem = f"🟢 {titulo}\n{link}\n" + "📌" * 10
            enviar_mensagem(mensagem)

    if vagas["presencial"]:
        enviar_mensagem("🏢 Vagas Presenciais\n" + "="*30)
        for titulo, link in vagas["presencial"]:
            mensagem = f"🔵 {titulo}\n{link}\n" + "📌" * 10
            enviar_mensagem(mensagem)

    if not vagas["remoto"] and not vagas["presencial"]:
        enviar_mensagem("Nenhuma vaga nova encontrada.")

if __name__ == "__main__":
    main()
