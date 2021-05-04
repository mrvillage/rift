from ..data import get


async def get_applicants(*, alliance_id: int = None):
    return await get.get_applicants(alliance_id=alliance_id)
