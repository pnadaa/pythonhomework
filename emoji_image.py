from main import *

async def save_image_if_react(payload, bot):
    channel = bot.get_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)
    for attachment in message.attachments:
        if attachment.content_type.startswith("image"):
            await attachment.save(f"images/{attachment.filename}")