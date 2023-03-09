from dependency_injector import containers, providers

from app.internal.repository.postgresql import Repository
# from .auth import *
# from .email import *
# from .funds import *
# from .funds_users import *
# from .static import *
from .users import *


class Services(containers.DeclarativeContainer):
    repository_container = providers.Container(Repository)

    user = providers.Factory(
        Users,
        repository_container.users,
    )
    #
    # auth = providers.Factory(
    #     Auth,
    #     repository_container.users
    # )
    #
    # fund = providers.Factory(
    #     Funds,
    #     repository_container.funds,
    # )
    #
    # email = providers.Factory(
    #     Emails,
    #     repository_container.email)
    #
    # funds_users = providers.Factory(
    #     FundsUsers,
    #     repository_container.funds_users
    # )
    #
    # static_user = providers.Factory(
    #     StaticUser,
    #     repository_container.static_user
    # )
