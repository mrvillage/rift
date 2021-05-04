from .. import query
from .. import classes

async def get_applicants(*, alliance_id:int):
    applicants = await query.get_applicants(alliance_id=alliance_id)
    return [classes.Nation(data=i) for i in applicants]