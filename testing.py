import random
from telegram import Update
from telegram.ext import filters, ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler

# Dictionary to hold the game's state




async def new_game(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if context.args:
        word = context.args[0].lower()
        if len(word) != 5:
            await context.bot.send_message(
                chat_id = update.effective_chat.id, 
                text = "Please provide a 5-letter word.")
            return
    else:
        await context.bot.send_message(
                chat_id = update.effective_chat.id, 
                text = "No word provided. Starting with a random word.")
        word = random.choice(['apple', 'grape', 'peach', 'berry', 'mango'])

    
    await context.bot.send_message(
                chat_id = update.effective_chat.id, 
                text = "New game started! Guess the 5-letter word.")

async def guess(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    if chat_id not in games:
        await context.bot.send_message(
                chat_id = update.effective_chat.id, 
                text = "Start a new game with /newgame")
        return

    guess_word = context.args[0].lower() if context.args else ""
    game = games[chat_id]

    if len(guess_word) != 5:
        await context.bot.send_message(
                chat_id = update.effective_chat.id, 
                text = "Please guess a 5-letter word.")
        return

    game['attempts'].append(guess_word)

    if guess_word == game['word']:
        attempts = len(game['attempts'])
        await context.bot.send_message(
                chat_id = update.effective_chat.id, 
                text = f"Congratulations! You've guessed the word in {attempts} attempts!")
        update_leaderboard(update.message.from_user.username, attempts)
        del games[chat_id]  # Remove the game
    else:
        feedback = get_feedback(game['word'], guess_word)
        await context.bot.send_message(
                chat_id = update.effective_chat.id, 
                text = f"Incorrect guess! Feedback: {feedback}")

def get_feedback(correct_word, guessed_word):
    feedback = []
    for i, letter in enumerate(guessed_word):
        if letter == correct_word[i]:
            feedback.append('🟩')  # Green for correct letter and position
        elif letter in correct_word:
            feedback.append('🟨')  # Yellow for correct letter, wrong position
        else:
            feedback.append('⬛️')  # Black for wrong letter
    return ''.join(feedback)

def update_leaderboard(username, attempts):
    if username in leaderboard:
        leaderboard[username].append(attempts)
    else:
        leaderboard[username] = [attempts]

async def show_leaderboard(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not leaderboard:
        await context.bot.send_message(
                chat_id = update.effective_chat.id, 
                text = "Leaderboard is empty.")
        return

    leaderboard_text = "Leaderboard:\n"
    for user, attempts in leaderboard.items():
        average_attempts = sum(attempts) / len(attempts)
        leaderboard_text += f"{user}: {average_attempts:.2f} average attempts\n"
    await context.bot.send_message(
                chat_id = update.effective_chat.id, 
                text = leaderboard_text)

def main() -> None:
    # Replace 'YOUR_TOKEN' with your bot's API token
    application = ApplicationBuilder().token("7668496772:AAHmSQv1O8cHgw2ZtXospyq1vrMSfuZTXSE").build()

    # Register handlers
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('newgame', new_game))
    application.add_handler(CommandHandler('guess', guess))
    application.add_handler(CommandHandler('leaderboard', show_leaderboard))

    # Start the bot
    application.run_polling()

if __name__ == "__main__":
    main()