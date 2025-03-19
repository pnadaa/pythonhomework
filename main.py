import discord
from grades_homework import *
from karma import *
from emoji_image import *

# create intents == these are the permissions we want from discord
intents = discord.Intents.default()
# Saying that I want to receive message content from discord messages
intents.message_content = True

# Creating a new discord bot with the permissions we generated earlier
bot = discord.Client(intents=intents)

# Filename for storing all the karma data
karmajson = "karma.json"



@bot.event
async def on_ready():
    print(f"The bot is online with the username {bot.user}")

@bot.event
async def on_message(message: discord.message):
    # This makes sure that if put in message.channel.send, the bot does not ping people. Need to include allowed_mentions = mentions in the command
    mentions = discord.AllowedMentions(everyone=False, users=False, roles=False, replied_user=False)

    # Making sure the bot does not respond to itself
    if message.author.bot:
        return

    # Defining variables regarding the message detail to make it easier for us
    content = message.content
    author = message.author
    user = f"{author}_grades.json"
    channel = message.channel

    # Initialising variables required for karma
    split_by_word = content.split(" ")
    index = 0
    karma_dict = {}
    target = {}
    karma_present = False
    karma_total = 0
    
    #Checks for 1. whether someone is mentioned in discord using the <@ID> denominator and store the number of + and - in the message.
    # 2. if a word is only + or - and calculates the karma sum
    for n in split_by_word:
        result = check_for_mention(split_by_word, target, index)
        if result != None:
            target.update({result: ""})
        number_of_mentions = len(target)
        karma_present = check_for_karma(split_by_word, index)
        if karma_present != None:
            karma_total += karma_present
        index = index + 1
    
    #If one or more user is mentioned, and there are + or - present within the same message, calculate the total karma in the message,
    # load existing karma from the json, update with the new karma, then save and reply with the change to karma 
    if number_of_mentions > 0 and (karma_total > 0 or karma_total < 0):
        karma_to_print = f"Updated Karma!\n"
        karma_to_print = determine_user_karma(number_of_mentions, karmajson, target, karma_dict, karma_total, karma_to_print)
        await message.reply(content = f"{karma_to_print}", allowed_mentions = mentions)

    # Check if there is existing karma, if so, append the karma to a string separated by new line, and send to the channel.
    if content.startswith(">see karma"):
        existing_karma = initialise_and_load(karmajson)
        karma_check = check_for_grades(existing_karma)
        if karma_check == False:
            await message.reply("No one has karma saved yet")
            return
        karma = show_karma(existing_karma)
        await message.channel.send(content = f"Here is everyone's karma:\n{karma}", allowed_mentions = mentions)



## BELOW IS GRADES HW CODE
    if content.startswith(">start"):
        await message.reply(f"Hi {author}! Select a number below to start!\n>1: View all existing grades\n>2: Add new grades\n>3: View the average of your grades\n>4: Show your grades from best to worst\n>5: Show the mark for a particular course\n>6: Clear all my saved results")
    
    if content.startswith(">1"):
        grades = initialise_and_load(user)
        await view_grades(grades, message, 0)
    
    if content.startswith(">2"):
        await message.reply("Type [>add  coursename  grade] to add courses!")
    
    if content.startswith(">add"):
        await add_grades(content, message, user)

    if content.startswith(">3"):
        grades = initialise_and_load(user)
        average = calculate_average(grades)
        await message.reply(f"Your average mark is {average[0]:.2f} over {average[1]} courses")

    if content.startswith(">4"):
        grades = initialise_and_load(user)
        await rank_grades(grades,message)
   
    if content.startswith(">5"):
        await message.reply("Type [>get coursename] to retrieve the mark for your course!")
    
    if content.startswith(">get"):
        grades = initialise_and_load(user)
        course_code = content.split(" ")[1]
        course_code = course_code.upper()
        output = await get_mark(grades, course_code, message)
    
    if content.startswith(">6"):
        await message.reply("Are you sure? Type [>delete ALL] (case sensitive) to confirm")
    
    if content == ">delete ALL":
        await delete_all(message, user)



@bot.event
async def on_raw_reaction_add(payload: discord.RawReactionActionEvent):
    await save_image_if_react(payload, bot)




@bot.event
async def on_message_delete(message: discord.message):
    if message.author.bot:
        return
    content = message.content
    sender = message.author
    await message.channel.send(f"Nice try! {sender}, the message you just deleted was:\n{content}\n<:uggh:910079696199360532>")

# @bot.event
# async def on_message_delete(message: discord.message):
#     if message.author.bot:
#         return
#     content = message.content
#     sender = message.author
#     await message.channel.send(f"Nice try! {sender}, the message you just deleted was:\n{content}\n<:uggh:910079696199360532>")
    
# @bot.event
# async def on_message_edit(before, after):
#     if before.author.bot:
#         return
#     sender = before.author
#     await after.channel.send(f"Nice try! {sender}, the message you just edited was:\n{before.content}\nand was changed to:\n{after.content}")


def main():
    discord_key = initialise_and_load("discord_key.json")
    print(discord_key)
    bot.run(discord_key["discord"])

    
if __name__ == "__main__":
    main()