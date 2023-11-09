import uvicorn

from app import app
from db import init


init(app)


if __name__ == '__main__':
    uvicorn.run(app)