import os
from pathlib import Path

os.chdir(str(Path(__file__).parent))
from src.overrides import override

override()

from src.bot.main import main

main()
