from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from dotenv import load_dotenv
import os

load_dotenv()

# region Whitelist
WHITELIST = {
    int(os.getenv("ID_USERS"))
}
# endregion


# region Utilidades
def sanitize(text):
    """Limpia el texto para evitar que rompa el formato Markdown de Telegram."""
    if text is None:
        return "N/A"
    # Escapamos los caracteres que tienen significado especial en Markdown (V1)
    # _, *, ` y [ son los caracteres más problemáticos reservados en Markdown.
    caracteres_especiales = ['_', '*', '`', '[']
    resultado = str(text)
    for char in caracteres_especiales:
        resultado = resultado.replace(char, f"\\{char}")
    return resultado
# endregion


# region Funcion de comandos
async def say_hello(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat = update.effective_chat
    msg = update.effective_message

    # region Verificar whitelist
    if user.id not in WHITELIST:
        print(f"{user.id} (@{user.username})")
        return
    # endregion
# endregion

    # region Preparar el mensaje para el usuario
    info = (
        f"👤 *Información del Usuario*\n"
        f"• ID: `{user.id}`\n"
        f"• Nombre: {sanitize(user.first_name)}\n"
        f"• Apellido: {sanitize(user.last_name)}\n"
        f"• Username: @{sanitize(user.username)}\n"
        f"• Es bot: {user.is_bot}\n"
        f"• Idioma: {sanitize(user.language_code)}\n"
        f"• Premium: {getattr(user, 'is_premium', False)}\n"
        f"\n💬 *Información del Chat*\n"
        f"• Chat ID: `{chat.id}`\n"
        f"• Tipo: {sanitize(chat.type)}\n"
        f"• Título: {sanitize(getattr(chat, 'title', None))}\n"
        f"\n📩 *Información del Mensaje*\n"
        f"• Mensaje ID: `{msg.message_id}`\n"
        f"• Fecha: {msg.date}\n"
        f"• Texto: {sanitize(msg.text)}\n"
    )
    # endregion

    # region Guardar la información en el archivo local
    with open("usuarios.txt", "a", encoding="utf-8") as archivo:
        archivo.write(info + "\n" + "="*50 + "\n\n")
    
    # endregion

    # region Responder al usuario
    await context.bot.send_message(
        chat_id=chat.id,
        text=info,
        parse_mode="Markdown"
    )
    # endregion


# region Configuracion del bot y comandos
if __name__ == '__main__':
    application = ApplicationBuilder().token(os.getenv("BOT_TOKEN")).build()
    application.add_handler(CommandHandler("start", say_hello))
    
    print("Bot encendido y recolectando datos...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

# endregion