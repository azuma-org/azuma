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
import disnake
from disnake.ext import commands
from azuma.launch import get_prefix

class Settings(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.group('settings', invoke_without_command=True)
    async def settings(self, ctx: commands.Context):
        await ctx.send('this command is still in development.')

    @settings.group('prefix', invoke_without_command=True)
    async def prefixes(self, ctx: commands.Context):
        prefixes = await get_prefix(ctx.message, True)
        insert = prefixes.replace('', '\n')
        value = f'```{insert}```'

        embed = disnake.Embed(
            color=disnake.Color.dark_theme()
        )

        embed.add_field(f'Prefix\'s for {ctx.guild.name}', value)

        await ctx.reply(embed=embed)

def setup(bot: commands.Bot):
    bot.add_cog(Settings(bot=bot))
