# Order Chatbot

Order Chatbot is a Telegram bot that allows users to place food orders from a menu and manage their cart. The bot uses the `telegram` and `pymongo` Python libraries to interact with Telegram API and MongoDB database.

## Features

- View menu: Users can use the `/menu` command to view the available menu items with their prices.
- Place order: Users can use the `/order [foodName]` command to add a food item to their cart.
- View cart: Users can use the `/cart` command to view the items in their cart and the total price.
- Submit order: Users can use the `/submit` command to submit their order, which will store the order details in the MongoDB.
- Help: Users can use the `/help` command to view the available commands and get help.

## Prerequisites

- Python 3.7 or above
- `python-telegram-bot` library
- `pymongo` library
- MongoDB database

## Installation

1. Clone the repository: `git clone https://github.com/yourusername/order-chatbot.git`
2. Install the required libraries: `pip install -r requirements.txt`
3. Set up MongoDB: Make sure you have a MongoDB database up and running, and update the MongoDB connection details in the code.
4. Set up Telegram bot: Create a bot on Telegram using the BotFather, obtain the API token, and set it as an environment variable `ACCESS_TOKEN` or update it in the code.
5. Start the bot: Run `python main.py` to start the bot.

## Usage

- Start the bot on Telegram.
- Send commands to the bot to interact with it, such as `/help` to view available commands, `/menu` to view the menu, `/order [food name]` to place an order, `/cart` to view the cart, and `/submit` to submit the order.
- The bot will respond to your commands and perform the corresponding actions.