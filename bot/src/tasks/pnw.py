from __future__ import annotations

import datetime

from .. import utils
from .common import CommonTask

__all__ = ("PnWDataTask",)


class PnWDataTask(CommonTask):
    async def before_task(self) -> None:
        next_run = utils.utcnow()
        # set next run equal to the next multiple of four minutes
        next_run = next_run.replace(
            minute=(next_run.minute // 4) * 4, second=0, microsecond=0
        ) + datetime.timedelta(minutes=4)
        await utils.sleep_until(next_run.timestamp())

    async def task(self) -> None:
        ...
