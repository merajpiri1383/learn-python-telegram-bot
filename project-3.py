from telegram import Update,InlineKeyboardMarkup,InlineKeyboardButton
from telegram.ext import (ApplicationBuilder,ContextTypes,CommandHandler,CallbackQueryHandler)
from dotenv import load_dotenv
import os

# load environment variables
load_dotenv()


# start quize 
async def start_quize (update : Update,context : ContextTypes.DEFAULT_TYPE) : 
    question = "What is the capital of France?"

    # create options
    options = [
        [InlineKeyboardButton(text="Paris",callback_data="correct")],
        [InlineKeyboardButton(text="London",callback_data="wrong")],
        [InlineKeyboardButton(text="Berlin",callback_data="wrong")],
    ]
    # create markup
    inline_markup = InlineKeyboardMarkup(options)
    await update.message.reply_text(
        text=question,
        reply_markup=inline_markup
    )


# handle callback 
async def check_answer (update : Update , context : ContextTypes.DEFAULT_TYPE) : 
    query = update.callback_query
    await query.answer()

    if query.data == "correct" : 
        await query.edit_message_text("✅ Correct! Paris is the capital of France.")
    elif query.data == "wrong" : 
        await query.edit_message_text("❌ Wrong! Try again next time.")


# create application instance 
application = ApplicationBuilder().token(os.getenv("API_KEY")).build()

application.add_handler(CommandHandler("quize",start_quize))
application.add_handler(CallbackQueryHandler(check_answer))

# run application 
application.run_polling()