import logging
import random
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Configuración de registros
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# !!! REEMPLAZA ESTO CON TU TOKEN REAL DE BOTFATHER !!!
TOKEN = "7694591269:AAE59T0wJ_6l_lSD8XaWU29X1KeOPw4gDTE"

def cargar_datos():
    poblaciones = []
    # Cargar poblaciones y sus comarcas correctas
    with open('poblaciones.txt', 'r', encoding='utf-8') as f:
        for linea in f:
            if ',' in linea:
                pob, com = linea.strip().split(',', 1)
                poblaciones.append((pob.strip(), com.strip()))
                
    # Cargar el listado general de todas las comarcas disponibles
    with open('comarcas.txt', 'r', encoding='utf-8') as f:
        todas_comarcas = [linea.strip() for linea in f if linea.strip()]
        
    return poblaciones, todas_comarcas

POBLACIONES, TODAS_COMARCAS = cargar_datos()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "¡Bienvenido al juego de Geografía Valenciana! 🎭\n\n"
        "Te diré un municipio y tendrás que adivinar cuál es su comarca correcta entre 4 opciones.\n"
        "Escribe /jugar para empezar una nueva pregunta."
    )

async def jugar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Elegir una población al azar
    poblacion, comarca_correcta = random.choice(POBLACIONES)
    
    # Filtrar las comarcas para obtener las incorrectas
    comarcas_incorrectas = [c for c in TODAS_COMARCAS if c != comarca_correcta]
    
    # Elegir 3 falsas al azar
    opciones_falsas = random.sample(comarcas_incorrectas, 3)
    
    # Juntar la correcta con las falsas y mezclarlas
    opciones = opciones_falsas + [comarca_correcta]
    random.shuffle(opciones)
    
    # Guardar la respuesta correcta en el contexto del usuario para comprobarla luego
    context.user_data['correcta'] = comarca_correcta
    
    # Crear los botones del teclado (2 filas de 2 botones)
    teclado = [
        [opciones[0], opciones[1]],
        [opciones[2], opciones[3]]
    ]
    reply_markup = ReplyKeyboardMarkup(teclado, one_time_keyboard=True, resize_keyboard=True)
    
    await update.message.reply_text(
        f"¿A qué comarca pertenece el municipio de *{poblacion}*? 🤔",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

async def comprobar_respuesta(update: Update, context: ContextTypes.DEFAULT_TYPE):
    respuesta_usuario = update.message.text
    respuesta_correcta = context.user_data.get('correcta')
    
    if not respuesta_correcta:
        await update.message.reply_text("Escribe /jugar para empezar una partida.")
        return

    if respuesta_usuario == respuesta_correcta:
        await update.message.reply_text(
            "¡Correcto! 🎉 ¡Eres un experto de la Comunitat! Escribe /jugar para la siguiente.",
            reply_markup=ReplyKeyboardRemove()
        )
    else:
        await update.message.reply_text(
            f"¡Fallaste! ❌ La comarca correcta era: *{respuesta_correcta}*.\n¡Sigue intentándolo! Escribe /jugar.",
            reply_markup=ReplyKeyboardRemove(),
            parse_mode="Markdown"
        )
    
    # Limpiar la respuesta guardada
    context.user_data['correcta'] = None

def main():
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("jugar", jugar))
    
    # Escucha las respuestas de texto que no sean comandos para comprobar el resultado
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, comprobar_respuesta))

    # Inicia el Bot
    application.run_polling()

if __name__ == '__main__':
    main()
