from fastapi import FastAPI

from app.clients.fcm import fcm_svc
from app.config import get_settings
from app.controllers.notify import notify
from app.conn.db import metadata, database, engine

metadata.create_all(engine)

app = FastAPI(debug=get_settings().debug,
              title=get_settings().app_name,
              version=get_settings().app_version
              )


@app.on_event("startup")
async def startup():
    get_settings()
    fcm_svc.init()
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

app.include_router(notify, prefix="/notify", tags=['notify'])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=get_settings().db_host, port=get_settings().port)
