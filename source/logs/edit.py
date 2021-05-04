from ..data.db import execute_query


async def edit_log(time, message_id, channel_id, guild_id, author_id, message_content, qualified_name, success=None, errormessage=None):
    await execute_query("""
        UPDATE commandlogs
        SET
            success = $8,
            errormessage =  $9
        WHERE
            datetime = $1 AND
            messageid = $2 AND
            channelid = $3 AND
            guildid = $4 AND
            authorid = $5 AND
            messagecontent = $6 AND
            qualifiedname = $7;
        """, time, message_id, channel_id, guild_id, author_id, message_content, qualified_name, success, errormessage)