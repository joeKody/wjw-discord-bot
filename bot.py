import discord
import os
import json
from discord.ext import commands, tasks
from itertools import cycle
from importlib import import_module

current_dir = os.getcwd();
with open(os.path.join(current_dir, "secret.json"), 'r') as f:
        secret = json.load(f);
# Client set up
PREFIX = secret["PREFIX"];
intents = discord.Intents.all();

client = commands.Bot(command_prefix=PREFIX, intents=intents, help_command=None);

# Load other commands
cwd = os.getcwd();
cmd_d = os.path.join(cwd, "commands");
cmd_files = [f for f in os.listdir(cmd_d) if f.endswith('.py')];
print(f'\nLoading {len(cmd_files)} commands from the commands directory...');
for file in cmd_files:
    filename = file[:-3];
    command_module = import_module("commands." + filename)
    command_module.setup(client);
    print("Loaded : " + filename);
print("");

# BASIC COMMANDS
@client.command()
async def help(ctx, * args):
    len_arg = len(args)
    # no args, all commands
    if (len_arg == 0):
        embed = discord.Embed(title="Help", description="type `;help command` for more info on a command".format(PREFIX), color=discord.Color.red());

        formatted_commands = [];
        for command in client.commands:
            formatted_commands.append("`{0}`".format(command.name));

        embed.add_field(name="Commands", value=", ".join(formatted_commands));
    elif(len_arg == 1):
        cmd = arg[0].lower();
        if cmd[0] == ";":
            cmd = cmd[1:];

    return await ctx.send(embed=embed);

@client.command()
async def ping(ctx):
    await ctx.send(f"Latency : {client.latency}ms");

@client.event 
async def on_command_error(ctx, error): 
    pass
    #if isinstance(error, commands.CommandNotFound): 
    #print(str(ctx.author) + " made an error : " + str(error));

status = cycle([f"{PREFIX}help", f"my prefix is `{PREFIX}`"]);
@tasks.loop(seconds=8)
async def change_status():
    await client.change_presence(activity=discord.Game(next(status)));

@client.event
async def on_ready():
    change_status.start();
    print(f"\nRunning as {client.user} and Ready!\n");

# Run in main
def run_bot(token):
    client.run(token);

