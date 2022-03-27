from __future__ import annotations

import datetime

from .. import utils
from .common import CommonTask

__all__ = ("PnWDataTask",)


class PnWDataTask(CommonTask):
    def __init__(self) -> None:
        super().__init__(interval=300)

    async def before_task(self) -> None:
        next_run = utils.utcnow()
        # set next run equal to the next multiple of four minutes
        next_run = next_run.replace(
            minute=(next_run.minute // 5) * 5, second=0, microsecond=0
        ) + datetime.timedelta(minutes=5)
        await utils.sleep_until(next_run.timestamp())

    async def task(self) -> None:
        ...
