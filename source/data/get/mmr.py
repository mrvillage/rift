from ..db import execute_query, execute_read_query

async def get_mmr(*, alliance_id:int=None, mmr_id=None):
    if alliance_id is not None:
        return (await execute_read_query(f"""
            SELECT * FROM mmr
            WHERE alliance = $1;
        """, alliance_id))
    elif mmr_id is not None:
        return (await execute_read_query(f"""
            SELECT * from mmr
            WHERE id = $1;
        """),mmr_id)[0]