# wajaw-discord-bot
my own retarded discord bot

## Dependencies
1. Python
2. Python libraries as stated in `requirements.txt`

### Installation
Install required libraries by using this command
`pip install -r requirements.txt`

## Usage
1. Edit `secrets.json` as you please. (TOKEN, and PREFIX required)
2. Run `main.py` (`python3 main.py`)
3. Suffer!

## Adding custom commands
1. Create new python file in `commands/`
2. Use this template for the python file
```python
from discord.ext import commands

# REPLACE `command_name` to your preferences

# Command
@commands.command()
async def command_name(ctx, *):
	# Your code here
	pass

# Command error handling
@command_name.error
async def command_name_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        # This means that the arguments gave by the user is wrong
        pass
    else:
        pass

def setup(bot):
    bot.add_command(command_name);
```
