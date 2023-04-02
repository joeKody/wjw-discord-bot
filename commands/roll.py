from discord.ext import commands
import random


@commands.command()
async def roll(ctx, stop:int = 99, start:int=0):
    if (stop < start):
        tmp = stop;
        stop = start;
        start = tmp;

    rolled = random.randrange(start, stop);
    await ctx.send("Rolled {0}!".format(rolled));

@roll.error
async def roll_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        await ctx.send("I can only roll intergers...");

def setup(bot):
    bot.add_command(roll);
