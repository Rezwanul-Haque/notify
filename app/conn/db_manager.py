from sqlalchemy import Table, select
from sqlalchemy.dialects.mysql import insert

from app.conn.db import database


async def save(tbl: Table, values):
    stmt = __upsert(tbl, values)

    last_record_id = await database.execute(stmt)

    return last_record_id


async def get_tokens(tbl: Table, user_id):
    query = select([tbl.c.token]).where(tbl.c.user_id == user_id)

    return await database.fetch_all(query=query)


def __upsert(tbl: Table, values):
    insert_stmt = insert(tbl).values(
        user_id=values.user_id,
        token=values.token,
        device_info=values.device_info)

    on_duplicate_key_stmt = insert_stmt.on_duplicate_key_update(
        device_info=insert_stmt.inserted.device_info
    )

    return on_duplicate_key_stmt
