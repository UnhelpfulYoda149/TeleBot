#packages from python-telegram-bot
from telegram import Update
from telegram.ext import filters, ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler
import logging

from wordle import *

games = {}
leaderboard = {}

TOKEN = "7668496772:AAHmSQv1O8cHgw2ZtXospyq1vrMSfuZTXSE"

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
) #Set up for logging module so we know when and why things don't work

# Update (information that comes from telegram itself)
# Context (Contains information about the library, Bot, Application, job_queue)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    username = update.message.from_user.username
    if username in games:
        await context.bot.send_message(
            chat_id = update.effective_chat.id,
            text = f"Hi {username}! You already have a game started!"
        )
        return

    games[username] = {
        "guesses": [],
        "solved": False
    }
    await context.bot.send_message(
        chat_id = update.effective_chat.id, 
        text = f"Welcome {update.message.from_user.username}! Today's word has {WORD_LENGTH} letters! Type /guess <Your guess> to guess the word")

async def guess(update: Update, context: ContextTypes.DEFAULT_TYPE):
    #Get username from user who sent message
    username = update.message.from_user.username

    #Check if user has a game in progress for today
    if username not in games:
        await context.bot.send_message(
                chat_id = update.effective_chat.id, 
                text = "Start a new game with /start")
        return
    
    #We will update the game associated to the username
    game = games[username]
    
    if game["solved"]:
        await context.bot.send_message(
            chat_id = update.effective_chat.id,
            text = f"You've already solved today's puzzle!\nTo see the leaderboard, please use the /leaderboard command"
        )
        return
    
    if len(game["guesses"]) >= 6:
        await context.bot.send_message(
            chat_id = update.effective_chat.id,
            text = f"You've already reached the maximum number of allowed guesses today! Please try again tomorrow!"
        )
        return
    
    #Sets the user's guess to whatever comes after "/guess"
    guess_word = context.args[0] if context.args else ""

    #Check if guess is the right length
    if len(guess_word) != WORD_LENGTH:
        await context.bot.send_message(
                chat_id = update.effective_chat.id, 
                text = f"Please guess a {WORD_LENGTH}-letter word.")
        return
    
    game['guesses'].append(guess_word)

    if correct_answer(guess_word):
        game["solved"] = True
        attempts = len(game['guesses'])
        await context.bot.send_message(
                chat_id = update.effective_chat.id, 
                text = f"Congratulations! You've guessed today's word in {attempts} attempts!")
        update_leaderboard(update.message.from_user.username, attempts)
        return
    
    await context.bot.send_message(
        chat_id = update.effective_chat.id,
        text = check_guess(guess_word)
    )

def update_leaderboard(username, attempts):
    if username in leaderboard:
        leaderboard[username].append(MAX_POINTS - attempts)
    else:
        leaderboard[username] = [MAX_POINTS - attempts]

async def show_leaderboard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not leaderboard:
        await context.bot.send_message(
                chat_id = update.effective_chat.id, 
                text = "Leaderboard is empty.")
        return

    leaderboard_text = "Leaderboard:\n"
    for user, points in sorted(leaderboard.items(), key = lambda item: -1 * item[1]):
        total_points = sum(points)
        leaderboard_text += f"{user}: {total_points} points\n"
    await context.bot.send_message(
                chat_id = update.effective_chat.id, 
                text = leaderboard_text)

# Handlers
start_handler = CommandHandler("start", start)
reply_handler = CommandHandler("guess", guess)
leaderboard_handler = CommandHandler("leaderboard", show_leaderboard)

if __name__ == "__main__":
    #Application creates Updater, Bot (application.bot / application.updater.bot), BaseRequest
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(start_handler)
    application.add_handler(reply_handler)
    application.add_handler(leaderboard_handler)
    application.run_polling()
