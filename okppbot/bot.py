import discord
import os
import re
import lemminflect

bot = discord.Client()

from .words import WORDS, sanitize


def should_delete(content):
    content = sanitize(content)
    for word in re.split(r'\s+', content):
        if word.isdigit():
            continue
        if word in WORDS:
            continue
        inflections = (v for vs in lemminflect.getAllLemmas(word).values() for v in vs)
        if not any(inflection in WORDS for inflection in inflections):
            return True
    return False


async def process_message(channel_id, message_id, content):
    if not should_delete(content):
        return
    await bot.http.delete_message(channel_id, message_id, reason='ok pp head')


@bot.event
async def on_message(message):
    await process_message(message.channel.id, message.id, message.content)


@bot.event
async def on_raw_message_edit(payload):
    await process_message(payload.channel_id, payload.message_id, payload.data['content'])


def main(token=os.getenv('OKPPBOT_TOKEN')):
    bot.run(token)
