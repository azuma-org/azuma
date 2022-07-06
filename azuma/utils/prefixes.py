import disnake

from azuma.database import Guild, Prefix

async def get_prefix(message: disnake.Message, other_type: bool = False) -> list[str] | str:
    guild: Guild = Guild.objects(Guild.id == message.guild.id).get()

    prefixes = Prefix.objects(Prefix.guild_id == message.guild.id).all()

    pre = [p.prefix for p in prefixes]

    if guild.default_prefix:
        pre.append('!')

    if other_type:
        ret = ''
        for v in pre:
            ret += v

        return ret
    return pre
