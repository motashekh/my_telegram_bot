from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, InputMediaAnimation
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import time

# Constants for game configuration
COOLDOWN_PERIOD = 6  60  60 # 6 hours in seconds
DEFAULT_COAL_PER_CLAIM = 1000

# Task configuration Each task has a name, description, command, and reward points
TASKS = [
    {task_name Join Telegram Group, command join_telegram, description Join our Telegram group @YourGroup, reward 500},
    {task_name Follow on Twitter, command follow_twitter, description Follow us on Twitter @YourTwitter, reward 700},
    {task_name Retweet Post, command retweet_post, description Retweet this post httpstwitter.comYourTweet, reward 600},
]

# Upgrade costs and benefits
UPGRADES = [
    {cost 3000, coal_per_claim 1200},
    {cost 5000, coal_per_claim 1500},
    {cost 7000, coal_per_claim 1900},
    {cost 10000, coal_per_claim 2500}
]

# GIF or Sticker for the furnace animation
FURNACE_GIF_URL = httpsmedia.giphy.commedia3ohzdIuqJoo8QdKlnWgiphy.gif

# Dictionary to store user data (for simulation purposes)
coal_game_data = {}

# Utility functions for common actions
def get_user_data(user_id)
    Fetch or initialize user data.
    if user_id not in coal_game_data
        coal_game_data[user_id] = {
            coal_points 0,
            last_claim_time 0,
            coal_per_claim DEFAULT_COAL_PER_CLAIM,
            upgrade_level 0,
            completed_tasks []
        }
    return coal_game_data[user_id]

def update_coal_points(user_data, points)
    Add coal points to the user's balance.
    user_data[coal_points] += points

def is_in_cooldown(user_data)
    Check if the user is within the cooldown period for claiming coal.
    return time.time() - user_data[last_claim_time]  COOLDOWN_PERIOD

async def start(update Update, context ContextTypes.DEFAULT_TYPE)
    Display the start menu with the furnace and task options.
    user_id = update.effective_chat.id
    user_data = get_user_data(user_id)

    # Send an animated GIF of a furnace and display buttons for game and tasks
    keyboard = [
        [InlineKeyboardButton(🔥 Press the Furnace 🔥, callback_data=claim_coal)],
        [InlineKeyboardButton(📝 Go to Tasks, callback_data=go_to_tasks)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Send GIF and text
    await context.bot.send_animation(
        chat_id=user_id,
        animation=FURNACE_GIF_URL,
        caption=Welcome to the Furnace Game!nnPress the furnace to claim coal, or go to tasks to earn rewards.,
        reply_markup=reply_markup
    )

async def claim_coal(update Update, context ContextTypes.DEFAULT_TYPE)
    Handle the coal claim action and apply cooldown.
    query = update.callback_query
    user_id = query.message.chat.id
    user_data = get_user_data(user_id)

    if is_in_cooldown(user_data)
        remaining_time = int(COOLDOWN_PERIOD - (time.time() - user_data[last_claim_time]))  3600
        await query.answer(fYou need to wait {remaining_time} hours before claiming again.)
    else
        # Claim coal and reset cooldown
        update_coal_points(user_data, user_data[coal_per_claim])
        user_data[last_claim_time] = time.time()
        await query.answer(fYou claimed {user_data['coal_per_claim']} coal points!)
        
        # Update message with the current coal points
        await query.edit_message_caption(
            caption=f🔥 You claimed {user_data['coal_per_claim']} coal points! You now have {user_data['coal_points']} coal points.,
            reply_markup=query.message.reply_markup
        )

async def go_to_tasks(update Update, context ContextTypes.DEFAULT_TYPE)
    Display the task list with their descriptions and rewards.
    query = update.callback_query
    task_messages = nn.join([f{task['task_name']}n{task['description']} for task in TASKS])

    # Show task descriptions and a back button
    keyboard = [[InlineKeyboardButton(🔥 Back to Furnace, callback_data=back_to_furnace)]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(
        f📝 Complete the tasks below to earn coal points!nn{task_messages},
        reply_markup=reply_markup
    )

async def back_to_furnace(update Update, context ContextTypes.DEFAULT_TYPE)
    Return the user to the furnace game.
    await start(update, context)

async def complete_task(update Update, context ContextTypes.DEFAULT_TYPE, task_index int)
    Handle task completion and award the coal points.
    user_id = update.effective_chat.id
    user_data = get_user_data(user_id)

    if task_index in user_data[completed_tasks]
        await update.message.reply_text(You have already completed this task!)
    else
        task = TASKS[task_index]
        user_data[completed_tasks].append(task_index)
        update_coal_points(user_data, task[reward])

        await update.message.reply_text(f✅ Task completed {task['task_name']}!nYou've been awarded {task['reward']} coal points. You now have {user_data['coal_points']} coal points.)

# Task-specific handlers that link to the general task completion function
async def join_telegram(update Update, context ContextTypes.DEFAULT_TYPE)
    await complete_task(update, context, 0)

async def follow_twitter(update Update, context ContextTypes.DEFAULT_TYPE)
    await complete_task(update, context, 1)

async def retweet_post(update Update, context ContextTypes.DEFAULT_TYPE)
    await complete_task(update, context, 2)

async def upgrade_furnace(update Update, context ContextTypes.DEFAULT_TYPE)
    Handle the furnace upgrade logic.
    query = update.callback_query
    user_id = query.message.chat.id
    user_data = get_user_data(user_id)

    current_level = user_data[upgrade_level]
    
    if current_level = len(UPGRADES)
        await query.answer(You have already reached the maximum upgrade level!)
    else
        upgrade_cost = UPGRADES[current_level][cost]
        new_coal_per_claim = UPGRADES[current_level][coal_per_claim]

        if user_data[coal_points] = upgrade_cost
            # Deduct cost and upgrade
            update_coal_points(user_data, -upgrade_cost)
            user_data[coal_per_claim] = new_coal_per_claim
            user_data[upgrade_level] += 1
            await query.answer(fFurnace upgraded! You now collect {new_coal_per_claim} coal points per claim.)
            await query.edit_message_caption(
                caption=f✅ Furnace upgraded! You now collect {new_coal_per_claim} coal points per claim.,
                reply_markup=query.message.reply_markup
            )
        else
            await query.answer(fYou need {upgrade_cost} coal points to upgrade. You currently have {user_data['coal_points']}.)

# Main function to set up the bot
async def main()
    token = 7577515741AAGz9gdXLzPzCmAJmeLEUxHSyKxwHZSbqSE # Your actual bot token
    app = ApplicationBuilder().token(token).build()

    # Start game and task navigation
    app.add_handler(CommandHandler(start, start))

    # Task completion handlers
    app.add_handler(CommandHandler(join_telegram, join_telegram))
    app.add_handler(CommandHandler(follow_twitter, follow_twitter))
    app.add_handler(CommandHandler(retweet_post, retweet_post))

    # Callback handler for claiming coal and upgrading furnace
    app.add_handler(CallbackQueryHandler(claim_coal, pattern=claim_coal))
    app.add_handler(CallbackQueryHandler(go_to_tasks, pattern=go_to_tasks))
    app.add_handler(CallbackQueryHandler(back_to_furnace, pattern=back_to_furnace))
    app.add_handler(CallbackQueryHandler(upgrade_furnace, pattern=upgrade_furnace))

    await app.start_polling()
    await app.idle()

if __name__ == __main__
    import asyncio
    asyncio.run(main())