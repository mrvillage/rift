from ..data.db import execute_query


async def insert_log(
    time,
    message_id,
    channel_id,
    guild_id,
    author_id,
    message_content,
    qualified_name,
    args,
    kwargs,
    success=None,
    errormessage=None,
):
    await execute_query(
        """
        INSERT INTO commandlogs (datetime, messageid, channelid, guildid, authorid, messagecontent, qualifiedname, args, kwargs, success, errormessage)
        VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11);
        """,
        time,
        message_id,
        channel_id,
        guild_id,
        author_id,
        message_content,
        qualified_name,
        args,
        kwargs,
        success,
        errormessage,
    )
