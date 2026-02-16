from fastapi import FastAPI
import uvicorn
from api.libraries import router as libraries_router
from api.browse import router as browse_router
from api.comic_info import router as comic_info_router
from api.actions import router as read_status_router

app = FastAPI()
app.include_router(libraries_router)
app.include_router(browse_router)
app.include_router(comic_info_router)
app.include_router(read_status_router)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
