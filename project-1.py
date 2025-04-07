from telegram import Update
from telegram.ext import (ApplicationBuilder,ContextTypes,ConversationHandler,CommandHandler,
        MessageHandler,filters)
from dotenv import load_dotenv
import os

load_dotenv()

# define states 
NAME,AGE = range(2)

async def start (update : Update , context : ContextTypes.DEFAULT_TYPE) :
    await update.message.reply_text("what's your name ?")
    return NAME

async def get_name (update : Update , context : ContextTypes.DEFAULT_TYPE) : 
    context.user_data["Name"] = update.message.text
    await update.message.reply_text(f"Nice To Meet You, {update.message.text}! How Old Are You ?")
    return AGE

async def get_age (update : Update,context : ContextTypes.DEFAULT_TYPE) : 
    age = update.message.text
    name = context.user_data["Name"]
    await update.message.reply_text(f"Got it!, {name} You Are {age} Years Old .")
    return ConversationHandler.END

async def cancel (update : Update , context : ContextTypes.DEFAULT_TYPE) : 
    await update.message.reply_text("Conversation Canceled .")
    return ConversationHandler.END


app = ApplicationBuilder().token(os.getenv("API_KEY")).build()

conv_handler = ConversationHandler(
    entry_points=[CommandHandler("start",start)],
    states={
        NAME : [MessageHandler(filters=filters.TEXT & ~filters.COMMAND,callback=get_name)],
        AGE : [MessageHandler(filters=filters.TEXT & ~filters.COMMAND,callback=get_age)],
    },
    fallbacks=[
        CommandHandler("cancel",cancel)
    ]
)

app.add_handler(conv_handler)

app.run_polling()