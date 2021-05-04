import discord, json, os, asyncio, random, time, datetime
from dotenv import load_dotenv
from discord.ext import commands
import aiosqlite
from discord.ext.commands import MemberConverter
from .core import * # pylint: disable=unused-wildcard-import
from ..data.db.sql import * # pylint: disable=unused-wildcard-import

def key0(item):
    return item[0]

def key1(item):
    return item[1]

# Link Management


# Data Management
nation_columns = ['nation_id','nation','leader','continent','war_policy','domestic_policy','color','alliance_id','alliance','alliance_position','cities','offensive_wars','defensive_wars','score','v_mode','v_mode_turns','beige_turns','last_active','founded','soldiers','tanks','aircraft','ships','missiles','nukes']

async def get_nation(connection,nation_id):
    return (await execute_read_query(f"""
        SELECT * FROM nations
        WHERE nation_id = {nation_id};
    """))[0]

async def get_nation_name(connection,nation):
    return (await execute_read_query(f"""
        SELECT * FROM nations
        WHERE LOWER(nation) = LOWER('{nation}');
    """))[0]

async def get_nations(connection):
    return (await execute_read_query(f"""
        SELECT last_active,v_mode FROM nations;
    """))

async def get_alliance(connection,alliance_id):
    return (await execute_read_query(f"""
        SELECT * FROM alliances
        WHERE id = {alliance_id};
    """))[0]

async def get_alliance_name(connection,alliance):
    return (await execute_read_query(f"""
        SELECT * FROM alliances
        WHERE LOWER(name) = LOWER('{alliance}');
    """))[0]

async def get_alliance_members(connection,alliance_id):
    return await execute_read_query(f"""
        SELECT * FROM nations
        WHERE alliance_id = {alliance_id} AND alliance_position != 1 AND v_mode = 'False';
    """)

async def calculate_alliance_members(connection,alliance_id):
    return await execute_read_query(f"""
        SELECT score FROM nations
        WHERE alliance_id = {alliance_id} AND alliance_position != 1 AND v_mode = 'False';
    """)

async def calculate_vm_alliance_members(connection,alliance_id):
        return await execute_read_query(f"""
        SELECT score FROM nations
        WHERE alliance_id = {alliance_id} AND alliance_position != 1 AND v_mode = 'True';
    """)

async def add_target(connection,nation_id,old_color,owner,channels,roles,members):
    await execute_query(f"""
        INSERT INTO targets
        (id,oldcolor,owner,channels,roles,members)
        VALUES ({nation_id},{old_color},'{str(owner)}','{str(channels)}','{str(roles)}','{str(members)}');
    """)

async def remove_target(connection,target_id):
    await execute_query(f"""
        DELETE FROM targets
        WHERE targetid = {target_id};
    """)

async def get_target(connection,target_id):
    return (await execute_read_query(f"""
        SELECT * FROM targets
        WHERE targetid = {target_id};
    """))[0]

async def get_targets(connection):
    return await execute_read_query(f"""
        SELECT * FROM targets;
    """)

async def get_targets_owner(connection,owner):
    return await execute_read_query(f"""
        SELECT * FROM targets
        WHERE owner = {owner};
    """)

async def update_target_color(connection,nation_id,color):
    await execute_query(f"""
        UPDATE targets
        SET oldcolor = {color}
        WHERE id = {nation_id};
    """)

def get_alliance_id(id):
    if id == 0:
        return "None"
    else:
        return id

def get_nation_militarization(nation):
    militarization = {
        "soldiers": nation[19]/(nation[10]*15000),
        "tanks": nation[20]/(nation[10]*1250),
        "aircraft": nation[21]/(nation[10]*75),
        "ships": nation[22]/(nation[10]*15)
    }
    militarization['total'] = sum(militarization.values())/4
    return militarization