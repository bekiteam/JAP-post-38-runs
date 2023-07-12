import telebot
import requests
from environs import Env

env = Env()
env.read_env()
#env file get
CHANNEL_USERNAME = env.str("CHANNEL_USERNAME")
BOT_TOKEN = env.str("BOT_TOKEN")
JAP_API_KEY = env.str("JAP_API_KEY")

# admin chat -id
admin = 5808244662

# Create the bot object
bot = telebot.TeleBot(token=BOT_TOKEN)

# Define the command handler for the /start command
@bot.message_handler(commands=['start'])
def send_channel_link(message):
     channel_link = f"https://t.me/{CHANNEL_USERNAME}"
     bot.reply_to(message, f"авто постинг контент активно работает в канале : {channel_link}\n @force700")
@bot.message_handler(commands=['start'])
def help_msg_say(message):
     bot.reply_to(message, "нету комманды для улучшения, бот может только контролировать контент отправки")

# Define the message handler to save new post IDs to the list
@bot.channel_post_handler(content_types=['text','photo','audio','video','document'])
def save_new_post_id(message):
    messageid = message.message_id
    message_url = f"https://t.me/{CHANNEL_USERNAME}/{messageid}"
         
         # Send the message URL to the JAP API
    jap_api_url = 'https://justanotherpanel.com/api/v2'
    order_data = {'service': 7939, 'link': message_url, 'quantity': 10, 'runs': 38, 'interval': 65}
    post_data = {'key': JAP_API_KEY, 'action': 'add'}
    post_data.update(order_data)
    try:
        response = requests.post(jap_api_url, data=post_data).text
        if response:
            bot.send_message(admin, f"✅ Order {response} is done!")
        else:
            bot.send_message(admin, "Failed to place order")
    except Exception as e:
        print(f"Failed to place order: {e}")
        bot.send_message(admin, "Failed to send order to JAP.")
     
     # If there are not 3 message IDs in the list yet, continue waiting for more
    else:
             bot.send_message(admin, "The message IDs list is empty.")

     # Send a message to the specified chat ID when a message ID is added to the list
    bot.send_message(admin, f"Added message ID {message.message_id}")

# Start the bot
bot.polling()
