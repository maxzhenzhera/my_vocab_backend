from fastapi import FastAPI, Depends
import uvicorn
from dataclasses import dataclass


app = FastAPI()

from pydantic import BaseModel

class Test(BaseModel):
    aaa: int = 1


@dataclass
class B:
    data = Test(aaa=100)


@dataclass
class A:
    b: B


class Marker: pass


app.dependency_overrides[Marker] = lambda: A(B())


@app.post('/aboba', response_model=Test)
def aboba(a: A = Depends()):
    return a.b.data


if __name__ == '__main__':
    uvicorn.run('main:app')
