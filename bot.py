import os
import random
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Configuració de logs per a veure errors si cal
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

TOKEN = os.environ.get("TOKEN_TELEGRAM")

def carregar_dades():
    poblacions = []
    comarques_set = set()
    
    # Llegim el fitxer de poblacions (poblacio, comarca)
    with open('poblacions.txt', 'r', encoding='utf-8') as f:
        for linia in f:
            linia = linia.strip()
            if not linia or ',' not in linia:
                continue
            pob, com = linia.split(',', 1)
            poblacions.append((pob.strip(), com.strip()))
            comarques_set.add(com.strip())
            
    return poblacions, list(comarques_set)

# Carreguem les dades a l'inici
POBLACIONS, COMARQUES = carregar_dades()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comanda inicial /start"""
    await update.message.reply_text(
        "👋 Benvingut/da al Joc de les Comarques Valencianes!\n"
        "Escriu /jugar per a començar una partida."
    )

async def enviar_pregunta(update: Update, context: ContextTypes.DEFAULT_TYPE, message_obj):
    """Genera una pregunta aleatòria i envia els botons"""
    # Triem una població a l'atzar
    poblacio, comarca_correcta = random.choice(POBLACIONS)
    
    # Generem 3 respostes incorrectes falses
    altres_comarques = [c for c in COMARQUES if c != comarca_correcta]
    opcions_falses = random.sample(altres_comarques, 3)
    
    # Juntem i barregem les 4 opcions
    opcions = opcions_falses + [comarca_correcta]
    random.shuffle(opcions)
    
    # Creem els botons interactius (InlineKeyboard)
    # Guardem en 'callback_data' si és la correcta (C) o incorrecta (I) i el nom de la correcta
    keyboard = []
    for opcio in opcions:
        es_correcta = "C" if opcio == comarca_correcta else "I"
        # callback_data màxim 64 bytes: codifiquem tipus i la resposta correcta per a comprovar desprès
        keyboard.append([InlineKeyboardButton(opcio, callback_data=f"{es_correcta}|{comarca_correcta}")])
        
    reply_markup = InlineKeyboardMarkup(keyboard)
    text_pregunta = f"❓ **De quina comarca és la població de:**\n👉 *{poblacio}*?"
    
    if update.message:
        await update.message.reply_text(text_pregunta, reply_markup=reply_markup, parse_mode="Markdown")
    else:
        await message_obj.reply_text(text_pregunta, reply_markup=reply_markup, parse_mode="Markdown")

async def jugar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comanda /jugar"""
    await enviar_pregunta(update, context, update.message)

async def responder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Gestiona el clic de l'usuari en els botons"""
    query = update.callback_query
    await query.answer()
    
    # Recuperem les dades del botó
    dades = query.data.split('|')
    es_correcta = dades[0]
    comarca_correcta = dades[1]
    
    # Modifiquem el missatge original per a mostrar el resultat i traure els botons
    if es_correcta == "C":
        text_resultat = f"{query.message.text}\n\n🌟 **CORRECTE!** Enhorabona. 🎉"
    else:
        text_resultat = f"{query.message.text}\n\n❌ **INCORRECTE...** La resposta correcta era **{comarca_correcta}**."
        
    await query.edit_message_text(text=text_resultat, parse_mode="Markdown")
    
    # Envia automàticament la següent pregunta
    await enviar_pregunta(update, context, query.message)

def main():
    # Creem l'aplicació del bot amb el Token de l'entorn
    application = Application.builder().token(TOKEN).build()

    # Handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("jugar", jugar))
    application.add_handler(CallbackQueryHandler(responder))

    # El bot es queda escoltant contínuament (ideal per a un bot interactiu)
    application.run_polling()

if __name__ == '__main__':
    main()
