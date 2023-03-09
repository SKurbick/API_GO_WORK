# """Main factory builder of ``FastAPI`` server."""
#
from fastapi import Depends, FastAPI
# from fastapi.middleware.cors import CORSMiddleware
#
# from app.configuration import __containers__
from app.configuration.server import Server


# from app.internal.pkg.middlewares.x_auth_token import get_x_token_key
#
#
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
    # __containers__.allocate_packages(app=app)

    return Server(app).get_app()
