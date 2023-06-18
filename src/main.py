from fastapi import FastAPI

from router import api_router

app = FastAPI()
app.include_router(api_router)


@app.get("/heath")
async def health_check():
    return {"status": "ok"}
