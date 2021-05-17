import os
from pathlib import Path
os.chdir(str(Path(__file__).parent))
import source.bot  # pylint: disable=wrong-import-position disable=unused-import
