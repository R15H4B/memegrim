import os

from utils import default
from utils.data import Bot, HelpFormat

print("Logging in...")

bot = Bot(
    command_prefix=os.environ['prefix'],
    prefix=os.environ['prefix'],
    command_attrs=dict(hidden=True),
    help_command=HelpFormat()
)

for file in os.listdir("cogs"):
    if file.endswith(".py"):
        name = file[:-3]
        bot.load_extension(f"cogs.{name}")

try:
    bot.run(os.environ['token'])
except Exception as e:
    print(f'Error when logging in: {e}')
