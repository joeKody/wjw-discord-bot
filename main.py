import bot
import os
import json

current_dir = os.getcwd();
with open(os.path.join(current_dir, "secret.json"), 'r') as f:
        secret = json.load(f);

TOKEN = secret["TOKEN"];

if __name__ == "__main__":
    bot.run_bot(TOKEN);
