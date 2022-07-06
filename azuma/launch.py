# Azuma - Discord Bot
# Copyright (C) 2022 VincentRPS
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
import asyncio
import logging
import os

import disnake
from disnake.ext import commands
from dotenv import load_dotenv

from azuma.database import Guild, Prefix, connect
from azuma.utils import get_prefix

load_dotenv()

intents = disnake.Intents.default()
intents.message_content = True

bot = commands.Bot(intents=intents, case_insensitive=True, reload=True)
bot.load_extensions('azuma/extensions')
FIRST_READY: bool = True

# remove annoying cassanda debugging
logging.getLogger('cassandra.cluster').disabled = True
logging.getLogger('cassandra.connection').disabled = True
logging.getLogger('cassandra.policies').disabled = True


@bot.listen('on_ready')
async def on_ready():
    global FIRST_READY
    if FIRST_READY:
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, connect)
        FIRST_READY = False


@bot.listen('on_guild_join')
async def guild_join(guild: disnake.Guild):
    Guild.create(id=guild.id)


@bot.listen('on_guild_leave')
async def guild_leave(guild: disnake.Guild):
    # delete guild configs and remove prefixes
    guild: Guild = Guild.objects(Guild.id == guild.id).get()
    guild.delete()

    prefixes: list[Prefix] = Prefix.objects(Prefix.guild_id == guild.id).all()

    for prefix in prefixes:
        prefix.delete()


bot.get_prefix = get_prefix

bot.run(os.getenv('TOKEN'))
