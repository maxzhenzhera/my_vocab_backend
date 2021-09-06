from fastapi import FastAPI

from app.core.config import uvicorn_config


app = FastAPI()


if __name__ == '__main__':
    import uvicorn

    uvicorn.run('main:app', **uvicorn_config)
