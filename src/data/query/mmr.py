from ..db import execute_read_query


async def get_mmr(*, mmr_id=None, alliance_id=None):
    if mmr_id is not None:
        return (
            await execute_read_query(
                """
            SELECT * FROM mmr
            WHERE id = $1;
        """,
                mmr_id,
            )
        )[0]
