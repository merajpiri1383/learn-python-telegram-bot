from telegram import Update,ReplyKeyboardMarkup
from telegram.ext import (ApplicationBuilder,ContextTypes,ConversationHandler,
            CommandHandler,MessageHandler,filters)
import os
from dotenv import load_dotenv

load_dotenv()

# states for converation 
SIZE,TOPPING = range(2)

# start getting order 
async def order (update : Update , context : ContextTypes.DEFAULT_TYPE) : 
    keyboards = [["Small","Medium","Large"]]
    await update.message.reply_text(
        text="Welcome to PizzaBot! 🍕 What size pizza would you like?",
        reply_markup=ReplyKeyboardMarkup(keyboard=keyboards,one_time_keyboard=True)
    )
    return SIZE

# get size of order 

async def get_size (update : Update , context : ContextTypes.DEFAULT_TYPE) : 
    # check if the message is correct 
    if update.message.text in ["Small","Medium","Large"] : 
        context.user_data["SIZE"] = update.message.text
        await update.message.reply_text("What toppings do you want ?")
        return TOPPING
    else : 
        await update.message.reply_text("Invalid Text")
        return SIZE
    

# get Topping 

async def get_topping (update : Update , context : ContextTypes.DEFAULT_TYPE) : 
    topping = update.message.text
    size = context.user_data["SIZE"]
    await update.message.reply_text(f"✅ Order received!\n\nSize: {size}\nTopping: {topping}\n\nThank you!")
    return ConversationHandler.END


# cancel handler 

async def cancel_conversation (update : Update, context : ContextTypes.DEFAULT_TYPE) : 
    await update.message.reply_text("Conversation Canceled .")
    return ConversationHandler.END




# config conversation steps 
conversation_handler = ConversationHandler(
    # define the start of converation 
    entry_points=[CommandHandler("order",order)],
    # define states
    states={
        SIZE : [MessageHandler(filters=filters.TEXT & ~filters.COMMAND,callback=get_size)],
        TOPPING : [MessageHandler(filters=filters.TEXT & ~filters.COMMAND,callback=get_topping)],
    },
    fallbacks=[CommandHandler(command="cancel",callback=cancel_conversation)]
)

app = ApplicationBuilder().token(os.getenv("API_KEY")).build()
app.add_handler(conversation_handler)
app.run_polling()