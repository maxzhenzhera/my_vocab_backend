from fastapi import FastAPI


app = FastAPI()


if __name__ == '__main__':
    import uvicorn

    uvicorn.run('main:app')
