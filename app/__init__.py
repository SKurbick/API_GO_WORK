# """Main factory builder of ``FastAPI`` server."""
#
from fastapi import Depends, FastAPI
# from fastapi.middleware.cors import CORSMiddleware
#
from app.configuration.server import Server

# from app.internal.pkg.middlewares.x_auth_token import get_x_token_key
#
from app.configuration import __containers__

from fastapi import FastAPI, Request

import time

def create_app() -> FastAPI:
    app = FastAPI(
        # dependencies=[Depends(get_x_token_key)]
    )
    # app.add_middleware(
    #     CORSMiddleware,
    #     allow_origins=["*"],
    #     allow_methods=["*"],
    #     allow_headers=["*"],
    #     allow_credentials=False,
    # )
    __containers__.allocate_packages(app=app)

    # @app.middleware("/head")
    # async def add_process_time_header(request: Request, call_next):
    #     start_time = time.time()
    #     response = await call_next(request)
    #     # print(response)
    #     process_time = time.time() - start_time
    #     response.headers["X-Process-Time"] = str(process_time)
    #     print(process_time)
    #     return response
    return Server(app).get_app()





