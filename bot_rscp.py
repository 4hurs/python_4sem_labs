from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import random
import os

stats = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Я бот для игры в камень, ножницы, бумага.\n"
        "Используй /play чтобы начать игру.\n"
        "/stats покажет твою статистику."
    )


async def play(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton("Камень", callback_data="rock"),
            InlineKeyboardButton("Ножницы", callback_data="scissors"),
            InlineKeyboardButton("Бумага", callback_data="paper"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Выбери свой ход:", reply_markup=reply_markup)


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_choice = query.data
    bot_choice = random.choice(["rock", "scissors", "paper"])

    result = determine_winner(user_choice, bot_choice)
    user_id = query.from_user.id

    if user_id not in stats:
        stats[user_id] = {"wins": 0, "losses": 0, "draws": 0}

    stats[user_id][result] += 1

    await query.edit_message_text(
        f"Твой выбор: {translate_choice(user_choice)}\n"
        f"Мой выбор: {translate_choice(bot_choice)}\n"
        f"Результат: {translate_result(result)}"
    )


def determine_winner(user, bot):
    if user == bot:
        return "draws"
    if (user == "rock" and bot == "scissors") or \
            (user == "scissors" and bot == "paper") or \
            (user == "paper" and bot == "rock"):
        return "wins"
    return "losses"


def translate_choice(choice):
    return {"rock": "Камень", "scissors": "Ножницы", "paper": "Бумага"}[choice]


def translate_result(result):
    return {"wins": "Победа!", "losses": "Поражение!", "draws": "Ничья!"}[result]


async def show_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if user_id not in stats:
        await update.message.reply_text("Вы еще не играли!")
        return

    s = stats[user_id]
    await update.message.reply_text(
        f"Ваша статистика:\n"
        f"Побед: {s['wins']}\n"
        f"Поражений: {s['losses']}\n"
        f"Ничьих: {s['draws']}"
    )


BOT1_TOKEN="7196555525:AAEMQeWYsIYD2PExeIM5fJmdtfeKgjLramk"

if __name__ == "__main__":
    app = Application.builder().token(BOT1_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("play", play))
    app.add_handler(CommandHandler("stats", show_stats))
    app.add_handler(CallbackQueryHandler(button))
    app.run_polling()