from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from pymongo import MongoClient

import configparser
import logging
import os

cart = []

telegram_api_token = os.environ.get('ACCESS_TOKEN')

def main():
# Load your token and create an Updater for your Bot

    config = configparser.ConfigParser()
    config.read('config.ini')
    updater = Updater(token=telegram_api_token, use_context=True)
    dispatcher = updater.dispatcher

    client = MongoClient('mongodb://124.71.84.38:27017/')
    db = client['chatbot']
    global menu_collection 
    global orders_collection 
    menu_collection = db['food']
    orders_collection = db["orders"]

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - % (message)s', level=logging.INFO)

    # register a dispatcher to handle message: here we register an echo dispatcher
    echo_handler = MessageHandler(Filters.text & (~Filters.command), echo) 
    dispatcher.add_handler(echo_handler)

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("help", help))
    dispatcher.add_handler(CommandHandler("menu", show_menu))
    dispatcher.add_handler(CommandHandler("order", place_order))
    dispatcher.add_handler(CommandHandler("cart", show_cart))
    dispatcher.add_handler(CommandHandler("submit", submit_order))

    # To start the bot:
    updater.start_polling()
    updater.idle()

def echo(update, context):
    user_id = update.message.from_user.id
    update.message.reply_text(f'Welcome to use order chatbot, your user_id is: {user_id}\n\n' + 'Please input /help to get more commands.')
    
# 展示菜单
def show_menu(update: Update, context: CallbackContext) -> None:
    # 查询 MongoDB 中的菜单信息
    menu_list = []
    for dish in menu_collection.find():
        menu_list.append(f"{dish['name']}: ${dish['price']}")
    menu_list = "\n".join(menu_list)

    update.message.reply_text(f"Hello, this is our menu:\n{menu_list}\n\n" + "Please use /order [food name] to add food!")

# 添加商品到购物车
def place_order(update: Update, context: CallbackContext) -> None:
    dish = context.args[0]
    # 在菜单集合中查询是否存在该菜品
    menu_item = menu_collection.find_one({'name': dish})

    if menu_item:
        price = menu_item['price']
        user_id = update.message.from_user.id
        cart.append({'user_id': user_id, 'name': dish, 'price': price})
        total_price = sum(int(item['price']) for item in cart)
        update.message.reply_text(f"You added {dish} to your cart. The price is ${price}.")
        update.message.reply_text(f"Total price: ${total_price}")
    else:
        update.message.reply_text("Sorry, this food doesn't exist!")

# 查看帮助
def help(update: Update, context: CallbackContext) -> None:
    "help message"
    help_text = "Welcome to use order chatbot！\n\n"
    help_text += "These are commands\n"
    help_text += "/help - help information\n"
    help_text += "/order - /order [food name] to order a item\n"
    help_text += "/menu - read menu\n"
    help_text += "/cart - show your cart\n"
    help_text += "/submit - submit your order\n"
    update.message.reply_text(help_text)

# 展示购物车
def show_cart(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    user_cart = [item for item in cart if item['user_id'] == user_id]

    if user_cart:
        cart_list = "\n".join([f"{item['name']}: ${item['price']}" for item in user_cart])
        total_price = sum(int(item['price']) for item in user_cart)
        update.message.reply_text(f"Your Cart:\n{cart_list}")
        update.message.reply_text(f"Total price: ${total_price}")
    else:
        update.message.reply_text("Your cart is empty.")

# 提交订单
def submit_order(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    user_cart = [item for item in cart if item['user_id'] == user_id]

    if user_cart:
        # 将购物车中的菜品信息插入到 orders 表中 
        for item in user_cart:
            order = {"user_id": item['user_id'], "name": item['name'], "price": item['price']}
            orders_collection.insert_one(order)

        cart.clear()

        update.message.reply_text("Order submitted successfully.")
    else:
        update.message.reply_text("Your cart is empty.")

if __name__ == '__main__': 
    main()
