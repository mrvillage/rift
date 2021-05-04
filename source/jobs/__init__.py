from .applicants import *
from .recruitment import *
from .target import *

async def run_loops():
    await target_check()
    await applicant_messages(alliance_id=8246) # THE ABYSS FUNCTIONALITY ONLY